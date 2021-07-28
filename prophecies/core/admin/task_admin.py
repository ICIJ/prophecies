from django.contrib import admin
from django.utils.html import format_html
from prophecies.core.models import Task
from prophecies.core.models import TaskRecord


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ['creator']
    list_display = ('name', 'description', 'task_actions',)


    def task_actions(self, obj):
        return format_html('<a href="{}">Upload records</a>', '/')

    task_actions.short_description = 'Actions'
    task_actions.allow_tags = True


    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
