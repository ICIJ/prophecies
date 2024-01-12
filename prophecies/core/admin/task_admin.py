from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from polymorphic.admin import PolymorphicInlineSupportMixin
from prophecies.core.contrib.display import display_task_addon
from prophecies.core.forms.task_form import TaskForm
from prophecies.core.models import Task


class TaskAdminForm(TaskForm):
    checkers = forms.ModelMultipleChoiceField(
        required=True, queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple
    )


@admin.register(Task)
class TaskAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    exclude = ["creator"]
    search_fields = ["name"]
    list_display = (
        "task_with_addon",
        "description",
        "task_actions",
        "task_status",
    )
    form = TaskAdminForm

    def task_actions(self, obj):
        path = reverse("admin:core_taskrecord_upload")
        url = f"{path}?task={obj.id}"
        return format_html('<a href="{}">Upload records</a>', url)

    task_actions.short_description = "Actions"

    def task_status(self, task):
        return task.status.capitalize()

    task_status.short_description = "Status"

    def task_with_addon(self, task):
        return display_task_addon(task)

    task_with_addon.short_description = "Task Name"

    def save_model(self, request, obj, form, change):
        template_setting, _ = self.get_or_create_template_setting(obj)
        obj.template_setting = template_setting

        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def get_or_create_template_setting(self, obj):
        if obj.template_setting is None:
            return obj.template_type_model.objects.create(), True
        if not isinstance(obj.template_setting, obj.template_type_model):
            return obj.template_setting.convert_to(obj.template_type_model)
        return obj.template_setting, False
