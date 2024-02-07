from pydoc import locate
from rest_framework import viewsets
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import PolymorphicResourceRelatedField
from drf_spectacular.utils import extend_schema_serializer, extend_schema_view, extend_schema
from actstream.models import Action
from django.contrib.auth.models import User
from prophecies.core.filters import ActionFilter
from prophecies.core.models import (
    ActionAggregate,
    Choice,
    TaskRecord,
    TaskRecordReview,
    Tip,
)


class GenericModelSerializer(serializers.ModelSerializer):
    MODEL_SERIALIZERS_MAPPING = {
        ActionAggregate: "prophecies.apps.api.views.action_aggregate.ActionAggregateSerializer",
        User: "prophecies.apps.api.views.user.UserSerializer",
        Choice: "prophecies.apps.api.views.choice.ChoiceSerializer",
        TaskRecord: "prophecies.apps.api.views.task_record.TaskRecordSerializer",
        Tip: "prophecies.apps.api.views.tip.TipSerializer",
        TaskRecordReview: "prophecies.apps.api.views.task_record_review.FlatTaskRecordReviewSerializer",
    }

    def get_instance_serializer(self):
        instanceType = type(self)
        serializer = GenericModelSerializer.MODEL_SERIALIZERS_MAPPING.get(
            instanceType, None
        )
        if isinstance(serializer, str):
            return locate(serializer)
        return serializer

    def __new__(cls, instance=None, **kwargs):
        if instance is not None:
            serializer = cls.get_instance_serializer(instance)
            if serializer is not None:
                return serializer(instance, **kwargs)
            cls.Meta.model = type(instance)
        return super().__new__(cls, instance, **kwargs)

    class Meta:
        model = Action
        fields = ["id", "url"]


@extend_schema_serializer(exclude_fields=("actor", "action_object", "target"))
class ActionSerializer(serializers.HyperlinkedModelSerializer):
    actor = PolymorphicResourceRelatedField(
        GenericModelSerializer, many=False, read_only=True
    )
    action_object = PolymorphicResourceRelatedField(
        GenericModelSerializer, many=False, read_only=True
    )
    target = PolymorphicResourceRelatedField(
        GenericModelSerializer, many=False, read_only=True
    )

    included_serializers = {
        "actor": GenericModelSerializer,
        "action_object": GenericModelSerializer,
        "target": GenericModelSerializer,
    }

    class Meta:
        model = Action
        resource_name = "Action"
        fields = [
            "id",
            "url",
            "verb",
            "actor",
            "action_object",
            "target",
            "data",
            "public",
            "description",
            "timestamp",
        ]

    class JSONAPIMeta:
        included_resources = ["actor", "action_object", "target"]


@extend_schema_view(
    list=extend_schema(
        operation_id="List Actions",
        description="Returns a list of Actions.",
    ),
    retrieve=extend_schema(
        operation_id="Get Action",
        description="Get a single Action using an ID.",
    ),
)
class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filterset_class = ActionFilter
    ordering = ["-timestamp"]

    prefetch_for_includes = {
        "action": [
            "action",
            "action__actor",
            "action__target",
            "action__action_object",
        ],
        "action.actionObject": ["action", "action__action_object"],
    }
