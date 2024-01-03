from actstream import action
from rest_framework import exceptions, viewsets
from rest_framework import decorators
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.filters import TaskRecordFilter
from prophecies.core.models import TaskRecord, TaskRecordMedia
from prophecies.apps.api.views.action import ActionSerializer
from prophecies.apps.api.views.task import TaskSerializer
from prophecies.apps.api.views.task_record_media import TaskRecordMediaSerializer
from prophecies.apps.api.views.user import UserSerializer


class TaskRecordSerializer(serializers.HyperlinkedModelSerializer):
    task = ResourceRelatedField(many=False, read_only=True)
    link = serializers.SerializerMethodField()
    embeddable_link = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()
    locked_by = ResourceRelatedField(many=False, read_only=True)
    medias = ResourceRelatedField(many=True, model=TaskRecordMedia, read_only=True)
    included_serializers = {
        "locked_by": UserSerializer,
        "task": TaskSerializer,
        "medias": TaskRecordMediaSerializer,
    }

    class JSONAPIMeta:
        included_resources = ["locked_by", "task", "medias"]

    class Meta:
        model = TaskRecord
        resource_name = "TaskRecord"
        fields = [
            "id",
            "url",
            "uid",
            "task",
            "original_value",
            "predicted_value",
            "link",
            "embeddable_link",
            "locked",
            "locked_by",
            "medias",
            "metadata",
            "rounds",
            "status",
            "bookmarked",
        ]
        read_only_fields = [
            "url",
            "original_value",
            "predicted_value",
            "link",
            "embeddable_link",
            "metadata",
            "rounds",
            "status",
        ]

    def get_link(self, task_record):
        return task_record.computed_link()

    def get_embeddable_link(self, task_record):
        return task_record.computed_embeddable_link()

    def get_bookmarked(self, task_record):
        user = self.context.get("request").user
        return task_record.bookmarked_by.filter(id=user.id).exists()

    def get_medias(self, instance):
        return instance.medias.all()

    def update(self, instance, validated_data):
        self.update_locked(instance, validated_data)
        self.update_bookmarked(instance, validated_data)
        instance.save()
        return instance

    def update_locked(self, instance, validated_data):
        user = self.context.get("request").user
        locked = validated_data.get("locked")
        if locked is True:
            instance.locked = True
            instance.locked_by = user
            action.send(user, verb="locked", target=instance)
        elif locked is False:
            instance.locked = False
            instance.locked_by = None
            action.send(user, verb="unlocked", target=instance)
        return instance

    def update_bookmarked(self, instance, validated_data):
        user = self.context.get("request").user
        # "bookmarked" is not in the validated_data dict because it's a method field
        bookmarked = self.initial_data.get("bookmarked")
        if bookmarked is True:
            instance.bookmarked_by.add(user)
            action.send(user, verb="bookmarked", target=instance)
        elif bookmarked is False:
            instance.bookmarked_by.remove(user)
            action.send(user, verb="unbookmarked", target=instance)
        return instance

    def validate_locked(self, value):
        """
        Check the user can lock/unlock the record
        """
        user = self.context.get("request").user
        if value and not self.instance.can_lock(user):
            raise serializers.ValidationError("Cannot lock this task record")
        if not value and not self.instance.can_unlock(user):
            raise serializers.ValidationError("Cannot unlock this task record")
        return value


class TaskRecordViewSet(viewsets.ModelViewSet):
    queryset = TaskRecord.objects.all()
    serializer_class = TaskRecordSerializer
    ordering = ["-id"]
    permission_classes = [IsAuthenticated]
    filterset_class = TaskRecordFilter

    def get_task_record(self, pk):
        try:
            return TaskRecord.objects.get(pk=pk)
        except TaskRecord.DoesNotExist:
            raise exceptions.NotFound()

    @decorators.action(methods=["get"], detail=True)
    def actions(self, request, pk=None, **_kwargs):
        """
        List of actions performed over this task record.
        """
        # Change the resource name for the current view to ensure the "type" of
        # the serialized data is correct (the render uses this view property
        # to find the current type).
        self.resource_name = "Action"
        queryset = self.get_task_record(pk).actions.order_by("-timestamp").all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActionSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = ActionSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def check_object_permissions(self, request, obj):
        if not request.user in obj.checkers:
            raise exceptions.PermissionDenied(
                detail="You do not have permission to update this resource"
            )
        if not obj.task.is_open:
            raise exceptions.PermissionDenied(
                detail="You do not have permission to update a resource from a locked or closed task"
            )
