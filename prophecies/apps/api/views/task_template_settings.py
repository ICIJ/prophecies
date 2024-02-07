from drf_spectacular.utils import extend_schema_view, extend_schema
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


@extend_schema_view(
    list=extend_schema(
        operation_id="List TaskTemplateSettings",
        description="Returns a list of TaskTemplateSettings.",
    ),
    retrieve=extend_schema(
        operation_id="Get TaskTemplateSetting",
        description="Get a single TaskTemplateSetting using an ID.",
    ),
)
class TaskTemplateSettingViewSet(views.ReadOnlyModelViewSet):
    """
    A list of template settings, associated with a task.
    """
    queryset = TaskTemplateSetting.objects.all()
    serializer_class = TaskTemplateSettingSerializer
