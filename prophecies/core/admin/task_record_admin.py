import json

from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html
from prophecies.core.forms import TaskRecordUploadForm
from prophecies.core.models import TaskRecord


@admin.register(TaskRecord)
class TaskRecordAdmin(admin.ModelAdmin):
    change_list_template = "admin/task_record_changelist.html"
    exclude = ['metadata']
    readonly_fields = ['uid', 'rounds', 'original_value', 'suggested_value', 'status', 'metadata_json_preview']
    list_display = ('__str__', 'task', 'rounds', 'status')


    def metadata_json_preview(self, task_record):
        if task_record.metadata is None:
            return '-'
        metadata_pretty = json.dumps(task_record.metadata, indent=2)
        return format_html('<pre class="m-0 p-0"><code class="language-json">{0}</code></pre>', metadata_pretty)

    metadata_json_preview.short_description = "Metadata"


    def get_urls(self):
        urls = [ path('upload/', self.upload_view, name='core_taskrecord_upload') ]
        return urls + super().get_urls()


    def form_as_adminform(self, form, request):
        prepopulated_fields = self.get_prepopulated_fields(request)
        fields = form.base_fields
        fieldsets = [(None, { 'fields': fields })]
        return AdminForm(form, fieldsets, prepopulated_fields)


    def upload_view(self, request):
        if request.method == "POST":
            # Handle the request in a separated method
            return self.handle_upload(request)
        # Or display the upload form
        return self.upload_form_view(request)


    def upload_form_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        task = request.GET.get('task')
        form = extra_context.get('form', TaskRecordUploadForm(initial={'task': task}))
        adminform = self.form_as_adminform(form, request)
        context = dict(self.admin_site.each_context(request),
                      form=form,
                      adminform=adminform,
                      opts=TaskRecord._meta,
                      has_change_permission=self.has_change_permission(request),
                      has_view_permission=self.has_view_permission(request),
                      original='Upload task records',
                      title='Upload task records')
        return render(request, "admin/task_record_upload_form.html", context)


    def handle_upload(self, request):
        form = TaskRecordUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # The save method will take care of handling the CSV and creating/updating task records
            form.save()
            self.message_user(request, "Your csv file has been imported", messages.INFO)
            # Everything is fine, go back to the list of task records
            return redirect("..")
        else:
            self.message_user(request, "Unable to import the task records", messages.ERROR)
            # Call the same view with the received form
            return self.upload_form_view(request, extra_context={ 'form': form })
