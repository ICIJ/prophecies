from actstream import action
from functools import lru_cache
from django.db.models import Prefetch
from rest_framework import exceptions, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers
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
        'choice': ChoiceSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['checker', 'choice']

    class Meta:
        model = TaskRecordReview
        fields = ['id', 'url', 'checker', 'choice', 'status',
                    'note', 'note_created_at', 'note_updated_at',
                    'task_id', 'alternative_value']


class TaskRecordReviewSerializer(serializers.HyperlinkedModelSerializer):
    checker = ResourceRelatedField(many=False, read_only=True)
    choice = ResourceRelatedField(many=False, queryset=Choice.objects, required=False)
    task_record = ResourceRelatedField(many=False, read_only=True)
    history = SerializerMethodResourceRelatedField(many=True, model=TaskRecordReview, read_only=True)
    included_serializers = {
        'checker': UserSerializer,
        'choice': ChoiceSerializer,
        'task_record': TaskRecordSerializer,
        'history': FlatTaskRecordReviewSerializer
    }

    class JSONAPIMeta:
        included_resources = ['checker', 'choice', 'task_record', 'history']

    class Meta:
        model = TaskRecordReview
        fields = ['id', 'url', 'checker', 'choice', 'status',
                    'note', 'note_created_at', 'note_updated_at',
                    'alternative_value', 'task_record', 'task_id', 'history']
        read_only_fields = ['status',]

    def __init__(self, *args, **kwargs):
        try:
            self.filter_choice_queryset(self.fields['choice'], *args, **kwargs)
        except AttributeError:
            self.fields['choice'].queryset = Choice.objects.none()
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

    def save(self):
        user = self.context.get('request').user
        if 'choice' in self.validated_data:
            action.send(user, verb='reviewed', target=self.instance, action_object=self.validated_data.get('choice'), task_id=self.instance.task_record.task_id)
        if self.validated_data.get('alternative_value', None):
            action.send(user, verb='selected', target=self.instance, alternative_value=self.validated_data.get('alternative_value'), task_id=self.instance.task_record.task_id)
        if 'note' in self.validated_data:
            action.send(user, verb='commented', target=self.instance, note=self.validated_data.get('note'), task_id=self.instance.task_record.task_id)
        return super(TaskRecordReviewSerializer, self).save()


class TaskRecordReviewViewSet(viewsets.ModelViewSet):
    resource_name = 'TaskRecordReview'
    serializer_class = TaskRecordReviewSerializer
    http_method_names = ['get', 'put', 'head']
    permission_classes = [IsAuthenticated]
    search_fields = ['task_record__original_value',
                     'task_record__predicted_value']
    ordering = ['-id']
    ordering_fields = ['task_record__original_value', 'task_record__predicted_value',
                       'task_record__id']
    filterset_fields = {
       'choice': ('exact', 'in', 'isnull'),
       'alternative_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
       'task_record__priority': ('exact', 'in'),
       'task_record__rounds': ('exact', 'in'),
       'task_record__task': ('exact', 'in'),
       'task_record__locked': ('exact',),
       'task_record__has_notes': ('exact',),
       'task_record__has_disagreements': ('exact',),
       'task_record__predicted_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
       'task_record__original_value': ('icontains', 'exact', 'iexact', 'contains', 'in'),
       'task_record__reviews__checker': ('exact', 'in'),
       'task_record__reviews__choice': ('exact', 'in'),
       'task_record__reviews__id': ('exact', 'in'),
    }
    # Queryset is overridden within the `get_queryset` method
    queryset = TaskRecordReview.objects.none()

    def get_queryset(self):
        """
        All the task record attribution for the currently authenticated user.
        """
        if not self.request.user.is_authenticated:
            return TaskRecordReview.objects.none()
        return TaskRecordReview.objects \
            .filter(checker=self.request.user) \
            .select_related('checker') \
            .select_related('task_record') \
            .select_related('task_record__task') \
            .select_related('task_record__task__project')

    def check_object_permissions(self, request, obj):
        if obj.checker != request.user:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource.')
        if 'choice' in request.data and obj.task_record.locked:
            raise exceptions.PermissionDenied(detail='This resource was locked by a user.')
