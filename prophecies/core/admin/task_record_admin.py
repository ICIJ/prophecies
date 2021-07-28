from django.contrib import admin
from django.contrib.admin.helpers import AdminForm
from django.shortcuts import redirect, render
from django.urls import path
from prophecies.core.forms import TaskRecordUploadForm
from prophecies.core.models import TaskRecord


@admin.register(TaskRecord)
class TaskRecordAdmin(admin.ModelAdmin):
    change_list_template = "admin/task_record_changelist.html"


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


    def upload_form_view(self, request):
        form = TaskRecordUploadForm()
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            adminform=self.form_as_adminform(form, request),
            opts=TaskRecord._meta,
            has_change_permission=self.has_change_permission(request),
            has_view_permission=self.has_view_permission(request),
            original='Upload task records',
            title='Upload task records'
        )
        return render(request, "admin/task_record_upload_form.html", context)


    def handle_upload(self, request):
        # Nothing yet
        self.message_user(request, "Your csv file has been imported")
        return redirect("..")
