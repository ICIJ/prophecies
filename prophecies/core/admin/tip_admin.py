from django.contrib import admin
from prophecies.core.models import Tip
from prophecies.core.contrib.display import display_task_addon


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    exclude = ['creator']

    list_filter = ['creator', 'project', 'task']
    search_fields = ['name', 'description']
    list_display = ['name', 'creator', 'project', 'task_with_addon']

    def task_with_addon(self, task_record):
        return display_task_addon(task_record.task)

    task_with_addon.short_description = "Task"


    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
