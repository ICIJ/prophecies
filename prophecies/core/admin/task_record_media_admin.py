from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import truncatechars
from admin_auto_filters.filters import AutocompleteFilterFactory
from prophecies.core.models import TaskRecordMedia
from prophecies.core.forms import TaskRecordMediaUploadForm


@admin.register(TaskRecordMedia)
class TaskRecordMediaAdmin(admin.ModelAdmin):
    search_fields = [
        "file",
        "task_record__original_value",
        "task_record__predicted_value",
    ]
    list_display = ["preview", "display", "created_at"]
    list_display_links = ["preview", "display"]
    list_filter = [
        AutocompleteFilterFactory("task", "task"),
        AutocompleteFilterFactory("project", "task__project"),
    ]
    change_list_template = "admin/task_record_media_changelist.html"

    def get_fields(self, request, obj=None):
        if obj:
            return [
                "task",
                "task_record",
                "uid",
                "file",
                "mime_type",
                "height",
                "width",
            ]
        return ["task", "file"]

    def has_change_permission(self, request, obj=None):
        return obj is None

    @admin.display(description=_("Preview"), ordering="pk")
    def preview(self, media: TaskRecordMedia, width: int = 60):
        src = media.file_preview_url
        src = (
            src
            if src
            else f"https://placehold.co/{width}x{width}/235B59/FFF?text=No%20preview"
        )
        # Preview the file with a square image
        return format_html(
            f'<img src="{src}" width="{width}" height="{width}" style="object-fit: cover" border="0" />'
        )

    @admin.display(description=_("UID"), ordering="uid")
    def display(self, media: TaskRecordMedia):
        context = dict(
            uid=media.uid,
            uid_truncated=truncatechars(media.uid, 50),
            task_record=media.task_record,
        )
        template = """
            <div class="task-record-media-display">
                <div class="font-weight-bold" title="{uid}">{uid_truncated}</div>
                <div class="font-weight-light text-quiet">{task_record}</div>
            </div>
        """
        return format_html(template, **context)

    @admin.action(description="Import Task Records Medias")
    def import_action(self, request, queryset):
        extra_context = {"task_records": queryset}
        return self.assign_form_view(request, extra_context)

    def get_urls(self):
        urls = [
            path("upload/", self.upload_view, name="core_taskrecordmedia_upload"),
        ]
        return urls + super().get_urls()

    def form_as_adminform(self, form, request):
        prepopulated_fields = self.get_prepopulated_fields(request)
        fields = form.base_fields
        fieldsets = [(None, {"fields": fields})]
        return AdminForm(form, fieldsets, prepopulated_fields)

    def build_intermediate_form_context(self, request, form, title):
        adminform = self.form_as_adminform(form, request)
        return dict(
            self.admin_site.each_context(request),
            form=form,
            adminform=adminform,
            opts=TaskRecordMedia._meta,  # pylint: disable=protected-access
            original=title,
            title=title,
            has_change_permission=self.has_change_permission(request),
            has_view_permission=self.has_view_permission(request),
        )

    def upload_view(self, request):
        if request.method == "POST":
            # Handle the request in a separated method
            return self.upload_form_handler(request)
        # Or display the upload form
        return self.upload_form_view(request)

    def upload_form_view(self, request, extra_context=None):
        task = request.GET.get("task")
        extra_context = extra_context or {}
        initial = {
            "task": task,
            "unique": True,
            "media_types": TaskRecordMedia.MediaType.values,
        }
        form = extra_context.get("form", TaskRecordMediaUploadForm(initial=initial))
        title = "Upload task record medias"
        context = self.build_intermediate_form_context(
            request=request, form=form, title=title
        )
        return render(request, "admin/upload_form.html", context)

    def upload_form_handler(self, request):
        form = TaskRecordMediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # The save method will take care of handling the zip and upload task record medias
            created, updated, ignored = form.save()
            self.message_user(
                request,
                f"Your zip file has been imported: {created} created, {updated} updated and {ignored} ignored.",
                messages.INFO,
            )
            # Everything is fine, go back to the list of task record medias
            return redirect("..")
        self.message_user(
            request, "Unable to import the task record medias", messages.ERROR
        )
        # Call the same view with the received form
        return self.upload_form_view(request, extra_context={"form": form})
