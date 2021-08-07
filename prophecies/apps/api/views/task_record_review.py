from functools import lru_cache
from django.db.models import Prefetch
from rest_framework import viewsets, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.relations import ResourceRelatedField, SerializerMethodResourceRelatedField
from prophecies.core.models import Choice, TaskRecord, TaskRecordReview
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.task_record import TaskRecordSerializer
from prophecies.apps.api.views.user import UserSerializer


class FlatTaskRecordReviewSerializer(serializers.HyperlinkedModelSerializer):
    checker = ResourceRelatedField(many=False, read_only=True)
    choice = ResourceRelatedField(many=False, read_only=True)
    included_serializers = {
        'checker': UserSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['checker', 'choice']

    class Meta:
        model = TaskRecordReview
        fields = ['id', 'url', 'checker', 'choice', 'status', 'note', 'alternative_value']


class TaskRecordReviewSerializer(serializers.HyperlinkedModelSerializer):
    checker = ResourceRelatedField(many=False, read_only=True)
    collaborators = SerializerMethodResourceRelatedField(many=True, model=UserSerializer, read_only=True)
    choice = ResourceRelatedField(many=False, queryset=Choice.objects, required=False)
    task_record = ResourceRelatedField(many=False, read_only=True)
    history = SerializerMethodResourceRelatedField(many=True, model=TaskRecordReview, read_only=True)
    included_serializers = {
        'checker': UserSerializer,
        'collaborators': UserSerializer,
        'choice': ChoiceSerializer,
        'task_record': TaskRecordSerializer,
        'history': FlatTaskRecordReviewSerializer
    }

    class JSONAPIMeta:
        included_resources = ['checker', 'collaborators', 'choice', 'task_record', 'history']

    class Meta:
        model = TaskRecordReview
        fields = ['id', 'url', 'checker', 'collaborators', 'choice', 'status', 'note', 'alternative_value', 'task_record', 'history']
        read_only_fields = ['status',]

    def __init__(self, *args, **kwargs):
        self.filter_choice_queryset(self.fields['choice'], *args, **kwargs)
        super().__init__(*args, **kwargs)

    def filter_choice_queryset(self, f, instance=None, data=serializers.empty, request=None, **kwargs):
        if instance is None or not hasattr(instance, 'task_record'):
            return
        if instance.task_record.task.choice_group is None:
            f.queryset = Choice.objects.none()
        else:
            f.queryset = instance.task_record.task.choice_group.choices.all()

    @lru_cache(maxsize=None)
    def get_history(self, instance):
        return instance.history.select_related('checker', 'choice')

    @lru_cache(maxsize=None)
    def get_collaborators(self, instance):
        return [ i.checker for i in instance.history if i.checker != instance.checker ]

    # For some reason the validator require the choice to be set.
    # This is a workaround to allow empty value for the choice relationship.
    @lru_cache(maxsize=None)
    def get_validation_exclusions(self):
        exclusions = super(TaskRecordReviewSerializer, self).get_validation_exclusions()
        return exclusions + ['choice',]


class TaskRecordReviewViewSet(viewsets.ModelViewSet):
    serializer_class = TaskRecordReviewSerializer
    http_method_names = ['get', 'put', 'head']
    permission_classes = [IsAuthenticated]
    search_fields = ['task_record__original_value', 'task_record__predicted_value']
    ordering = ['-id']
    ordering_fields = ['task_record__original_value', 'task_record__predicted_value', 'task_record__id']
    filterset_fields = ['task_record__task', 'task_record__original_value', 'task_record__predicted_value']
    # Queryset is overridden within the `get_queryset` method
    queryset = TaskRecordReview.objects.none()

    def get_queryset(self):
        """
        All the task record attribution for the currently authenticated user.
        """
        return TaskRecordReview.objects \
            .filter(checker=self.request.user) \
            .prefetch_related('task_record', 'task_record__task',
                'task_record__task__project', 'task_record__reviews', 'checker')


    def check_object_permissions(self, request, obj):
        if obj.checker != request.user:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource.')
