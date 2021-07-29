from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from prophecies.core.contrib.display import display_task_addon
from prophecies.core.models import Task
from prophecies.core.models import TaskRecord


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ['creator']
    list_display = ('task_with_addon', 'description', 'task_actions',)


    def task_actions(self, obj):
        path = reverse('admin:core_taskrecord_upload')
        url = f'{path}?task={obj.id}'
        return format_html('<a href="{}">Upload records</a>', url)

    task_actions.short_description = 'Actions'


    def task_with_addon(self, task):
        return display_task_addon(task)

    task_with_addon.short_description = "Task Name"


    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
