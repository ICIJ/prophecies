from actstream import action
from rest_framework import exceptions, viewsets
from rest_framework import decorators
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from prophecies.core.models import Task, TaskRecord
from prophecies.apps.api.views.action import ActionSerializer
from prophecies.apps.api.views.task import TaskSerializer
from prophecies.apps.api.views.user import UserSerializer


class TaskRecordSerializer(serializers.HyperlinkedModelSerializer):
    task = ResourceRelatedField(many=False, read_only=True)
    link = serializers.SerializerMethodField()
    embeddable_link = serializers.SerializerMethodField()
    locked_by = ResourceRelatedField(many=False, read_only=True)
    included_serializers = {
        'locked_by': UserSerializer,
        'task': TaskSerializer
    }

    class JSONAPIMeta:
        included_resources = ['locked_by', 'task']

    class Meta:
        model = TaskRecord
        resource_name = 'TaskRecord'
        fields = ['id', 'url', 'task', 'original_value', 'predicted_value', 'link', 'embeddable_link', 'locked', 'locked_by', 'metadata', 'rounds', 'status']
        read_only_fields = ['url',  'original_value', 'predicted_value', 'link', 'embeddable_link', 'metadata', 'rounds', 'status']

    def get_link(self, task_record):
        return task_record.computed_link()
    
    def get_embeddable_link(self, task_record):
        return task_record.computed_embeddable_link()

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        if validated_data.get('locked') is True:
            instance.locked = True
            instance.locked_by = user
            action.send(user, verb='locked', target=instance)
        elif validated_data.get('locked') is False:
            instance.locked = False
            instance.locked_by = None
            action.send(user, verb='unlocked', target=instance)
        instance.save()
        return instance

    def validate_locked(self, value):
        """
        Check the user can lock/unlock the record
        """
        user = self.context.get('request').user
        if value and not self.instance.can_lock(user):
            raise serializers.ValidationError('Cannot lock this task record')
        elif not value and not self.instance.can_unlock(user):
            raise serializers.ValidationError('Cannot unlock this task record')
        return value


class TaskRecordViewSet(viewsets.ModelViewSet):
    queryset = TaskRecord.objects.all()
    serializer_class = TaskRecordSerializer
    ordering = ['-id']
    permission_classes = [IsAuthenticated]

    def get_task_record(self, pk):
        try:
            return TaskRecord.objects.get(pk=pk)
        except TaskRecord.DoesNotExist:
            raise exceptions.NotFound()

    @decorators.action(methods=['get'], detail=True)
    def actions(self, request, pk=None, **kwargs):
        """
        List of actions performed over this task record.
        """
        # Change the resource name for the current view to ensure the "type" of
        # the serialized data is correct (the render uses this view property
        # to find the current type).
        self.resource_name = 'Action'
        queryset = self.get_task_record(pk).actions.order_by('-timestamp').all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActionSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = ActionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def check_object_permissions(self, request, obj):
        if not request.user in obj.checkers:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource')
        if not obj.task.is_open:
            raise exceptions.PermissionDenied(detail='You do not have permission to update a resource from a locked or closed task')
