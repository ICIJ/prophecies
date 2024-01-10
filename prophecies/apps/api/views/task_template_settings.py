from rest_framework_json_api import serializers, views
from prophecies.core.models.task_template_setting import (
    TaskTemplateSetting,
    TaskTemplateSettingForText,
    TaskTemplateSettingForMedia,
    TaskTemplateSettingForIframe,
)


class BaseTaskTemplateSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplateSetting
        exclude = ("polymorphic_ctype",)


class TaskTemplateSettingForTextSerializer(BaseTaskTemplateSettingSerializer):
    class Meta:
        model = TaskTemplateSettingForText
        exclude = ("polymorphic_ctype",)


class TaskTemplateSettingForMediaSerializer(BaseTaskTemplateSettingSerializer):
    class Meta:
        model = TaskTemplateSettingForMedia
        exclude = ("polymorphic_ctype",)


class TaskTemplateSettingForIframeSerializer(BaseTaskTemplateSettingSerializer):
    class Meta:
        model = TaskTemplateSettingForIframe
        exclude = ("polymorphic_ctype",)


class TaskTemplateSettingSerializer(serializers.PolymorphicModelSerializer):
    polymorphic_serializers = [
        TaskTemplateSettingForTextSerializer,
        TaskTemplateSettingForMediaSerializer,
        TaskTemplateSettingForIframeSerializer,
    ]

    class Meta:
        model = TaskTemplateSetting
        exclude = ("polymorphic_ctype",)


class TaskTemplateSettingViewSet(views.ReadOnlyModelViewSet):
    queryset = TaskTemplateSetting.objects.all()
    serializer_class = TaskTemplateSettingSerializer
