from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.shortcuts import redirect, render
from django.template.defaultfilters import truncatechars
from django.urls import path
from django.utils.html import format_html

from import_export.resources import ModelResource

from prophecies.core.contrib.display import display_json, display_status, display_task_addon, display_task_record_link
from prophecies.core.forms import TaskRecordAssignForm, TaskRecordUploadForm
from prophecies.core.models import TaskRecord, TaskRecordReview
from prophecies.core.admin.filters import DistinctValuesDropdownFilter, ReviewedTaskRecordFilter
from prophecies.core.mixins import ExportWithCsvStreamMixin, ExportCsvGeneratorMixin


class TaskRecordResource(ExportCsvGeneratorMixin, ModelResource):
    class Meta:
        model = TaskRecord


class TaskRecordReviewInline(admin.TabularInline):
    model = TaskRecordReview
    fk_name = "task_record"
    readonly_fields = ['checker', 'note', 'alternative_value', 'choice', 'round', ]

    def status_badge(self, task_record):
        return display_status(task_record.get_status_display())

    status_badge.short_description = "Status"

    def has_add_permission(self, request, _obj=None):
        return False


@admin.register(TaskRecord)
class TaskRecordAdmin(ExportWithCsvStreamMixin, admin.ModelAdmin):
    resource_class = TaskRecordResource
    change_list_template = "admin/task_record_changelist.html"
    actions_on_bottom = True
    ordering = ('-pk',)
    exclude = ['metadata', 'rounds', 'link', 'status']
    readonly_fields = ['round_count', 'status_badge', 'computed_link', 'metadata_json']
    list_display = ['task_record_excerpt', 'original_value', 'task_with_addon', 'round_count', 'status_badge']
    list_filter = [
        AutocompleteFilterFactory('task', 'task'),
        AutocompleteFilterFactory('project', 'task__project'),
        AutocompleteFilterFactory('checkers', 'reviews__checker'),
        'status',
        'rounds',
        ReviewedTaskRecordFilter,
        'priority',
        'has_notes',
        'has_disagreements',
        ('predicted_value', DistinctValuesDropdownFilter),
    ]
    inlines = [TaskRecordReviewInline, ]
    actions = ['assign_action']
    search_fields = ['id', 'uid', 'original_value', 'predicted_value', 'metadata', 'link']

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('task') \
            .prefetch_related('task__project') \
            .prefetch_related('reviews') \
            .prefetch_related('reviews__checker')

    @admin.display(description='Record', ordering='pk')
    def task_record_excerpt(self, task_record):
        record_title = str(task_record)
        checkers = task_record.checkers_pretty
        uid = task_record.uid
        uid_truncated = '' if uid is None else truncatechars(uid, 50)
        context = dict(record_title=record_title, checkers=checkers, uid=uid, uid_truncated=uid_truncated)
        template = """
            <div class="task-record-display">
                <div>{record_title}</div>
                <div title="{uid}" class="font-weight-normal text-quiet text-monospace">{uid_truncated}</div>
                <div class="task-record-display__checkers text-quiet">{checkers}</div>
            </div>
        """
        return format_html(template, **context)

    @admin.display(description='Rounds', ordering='rounds')
    def round_count(self, task_record):
        return f'{task_record.rounds}/{task_record.task.rounds}'

    @admin.display(description='Task', ordering='task__name')
    def task_with_addon(self, task_record):
        return display_task_addon(task_record.task)

    @admin.display(description="Status", ordering='status')
    def status_badge(self, task_record):
        return display_status(task_record.get_status_display())

    @admin.display(description="Metadata")
    def metadata_json(self, task_record):
        return display_json(task_record.metadata)

    @admin.display(description="Link")
    def computed_link(self, task_record):
        return display_task_record_link(task_record)

    def get_urls(self):
        urls = [
            path('upload/', self.upload_view, name='core_taskrecord_upload'),
            path('assign/', self.assign_view, name='core_taskrecord_assign'),
        ]
        return urls + super().get_urls()

    def form_as_adminform(self, form, request):
        prepopulated_fields = self.get_prepopulated_fields(request)
        fields = form.base_fields
        fieldsets = [(None, {'fields': fields})]
        return AdminForm(form, fieldsets, prepopulated_fields)

    def build_intermediate_form_context(self, request, form, title):
        adminform = self.form_as_adminform(form, request)
        return dict(self.admin_site.each_context(request),
                    form=form, adminform=adminform,
                    opts=TaskRecord._meta, # pylint: disable=protected-access
                    original=title, title=title,
                    has_change_permission=self.has_change_permission(request),
                    has_view_permission=self.has_view_permission(request))

    @admin.action(description='Assign to a checker')
    def assign_action(self, request, queryset):
        extra_context = {'task_records': queryset}
        return self.assign_form_view(request, extra_context)

    def assign_view(self, request):
        if request.method == "POST":
            # Handle the request in a separated method
            return self.assign_form_handler(request)
        # Or redirect to the list, nothing to do
        return redirect("..")

    def assign_form_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        form = extra_context.get('form', TaskRecordAssignForm(initial=extra_context))
        title = 'Assign task records'
        context = self.build_intermediate_form_context(request=request, form=form, title=title)
        return render(request, "admin/task_record_assign_form.html", context)

    def assign_form_handler(self, request):
        form = TaskRecordAssignForm(request.POST)
        if form.is_valid():
            # The save method will take care of performing the review
            n = len(form.save())
            checker = form.cleaned_data["checker"]
            self.message_user(request, f"{n} task record(s) assignd to {checker}.", messages.INFO)
            # Everything is fine, go back to the list of task records
            return redirect("..")
        self.message_user(request, "Unable to assign the task records", messages.ERROR)
        # Call the same view with the received form
        return self.assign_form_view(request, extra_context={'form': form})

    def upload_view(self, request):
        if request.method == "POST":
            # Handle the request in a separated method
            return self.upload_form_handler(request)
        # Or display the upload form
        return self.upload_form_view(request)

    def upload_form_view(self, request, extra_context=None):
        task = request.GET.get('task')
        extra_context = extra_context or {}
        form = extra_context.get('form', TaskRecordUploadForm(initial={'task': task}))
        title = 'Upload task records'
        context = self.build_intermediate_form_context(request=request, form=form, title=title)
        return render(request, "admin/upload_form.html", context)

    def upload_form_handler(self, request):
        form = TaskRecordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # The save method will take care of handling the CSV and creating/updating task records
            form.save()
            self.message_user(request, "Your csv file has been imported", messages.INFO)
            # Everything is fine, go back to the list of task records
            return redirect("..")
        self.message_user(request, "Unable to import the task records", messages.ERROR)
       # Call the same view with the received form
        return self.upload_form_view(request, extra_context={'form': form})
