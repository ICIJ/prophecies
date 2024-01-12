from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from prophecies.core.models.task_template_setting import (
    TaskTemplateSetting,
    TaskTemplateSettingForText,
    TaskTemplateSettingForMedia,
    TaskTemplateSettingForIframe,
)


class BaseTaskTemplateSetting(PolymorphicChildModelAdmin):
    readonly_fields = ["task"]

    def has_module_permission(self, request):
        return False


@admin.register(TaskTemplateSettingForText)
class TaskTemplateSettingForTextAdmin(BaseTaskTemplateSetting):
    base_model = TaskTemplateSettingForText


@admin.register(TaskTemplateSettingForMedia)
class TaskTemplateSettingForMediaAdmin(BaseTaskTemplateSetting):
    base_model = TaskTemplateSettingForMedia


@admin.register(TaskTemplateSettingForIframe)
class TaskTemplateSettingForIframeAdmin(BaseTaskTemplateSetting):
    base_model = TaskTemplateSettingForIframe


@admin.register(TaskTemplateSetting)
class TaskTemplateSettingAdmin(PolymorphicParentModelAdmin):
    base_model = TaskTemplateSetting

    child_models = (
        TaskTemplateSettingForText,
        TaskTemplateSettingForMedia,
        TaskTemplateSettingForIframe,
    )

    def has_module_permission(self, request):
        return False
