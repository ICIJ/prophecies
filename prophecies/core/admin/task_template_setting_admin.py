from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from prophecies.core.models.task_template_setting import (
    TaskTemplateSetting,
    TaskTemplateSettingForText,
    TaskTemplateSettingForMedia,
    TaskTemplateSettingForIframe,
)


@admin.register(TaskTemplateSettingForText)
class TaskTemplateSettingForTextAdmin(PolymorphicChildModelAdmin):
    base_model = TaskTemplateSettingForText

    def has_module_permission(self, request):
        return False


@admin.register(TaskTemplateSettingForMedia)
class TaskTemplateSettingForMediaAdmin(PolymorphicChildModelAdmin):
    base_model = TaskTemplateSettingForMedia

    def has_module_permission(self, request):
        return False


@admin.register(TaskTemplateSettingForIframe)
class TaskTemplateSettingForIframeAdmin(PolymorphicChildModelAdmin):
    base_model = TaskTemplateSettingForIframe

    def has_module_permission(self, request):
        return False


@admin.register(TaskTemplateSetting)
class TaskTemplateSettingAdmin(PolymorphicParentModelAdmin):
    base_model = TaskTemplateSetting

    child_models = (
        TaskTemplateSettingForText,
        TaskTemplateSettingForMedia,
        TaskTemplateSettingForIframe,
    )

    # def has_module_permission(self, request):
    #     return False
