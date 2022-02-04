from functools import lru_cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import Task, TaskRecord, TaskRecordReview
from prophecies.core.models.task_record import StatusType
from prophecies.apps.api.views.choice_group import ChoiceGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer
from prophecies.apps.api.views.user import UserSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ResourceRelatedField(many=False, read_only=True)
    checkers = ResourceRelatedField(many=True, read_only=True)
    choice_group = ResourceRelatedField(many=False, read_only=True)
    task_records_count = serializers.SerializerMethodField()
    task_records_done_count = serializers.SerializerMethodField()
    user_task_records_count = serializers.SerializerMethodField()
    user_task_records_done_count = serializers.SerializerMethodField()
    user_progress_by_round = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    included_serializers = {
        'checkers': UserSerializer,
        'choice_group': ChoiceGroupSerializer,
        'project': ProjectSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['project']

    class Meta:
        model = Task
        fields = ['id', 'url', 'choice_group', 'checkers', 'colors', 'created_at',
            'description', 'name', 'project', 'priority', 'rounds',
            'task_records_count',  'task_records_done_count', 'embeddable_links',
            'user_task_records_count', 'user_task_records_done_count',
            'user_progress_by_round', 'user_progress','status',
            'progress', 'progress_by_round']

    @lru_cache(maxsize=None)
    def get_user_progress_by_round(self, task):
        checker = self.context.get('request').user
        return task.progress_by_round(checker=checker)

    @lru_cache(maxsize=None)
    def get_user_progress(self, task):
        user_records = self.get_user_task_records_done_count(task)
        all_records = self.get_user_task_records_count(task)
        return 100 if all_records == 0 else user_records / all_records * 100

    @lru_cache(maxsize=None)
    def get_user_task_records_count(self, task):
        checker = self.context.get('request').user
        filter = dict(task_record__task=task, checker=checker)
        return TaskRecordReview.objects.filter(**filter).count()

    @lru_cache(maxsize=None)
    def get_user_task_records_done_count(self, task):
        checker = self.context.get('request').user
        filter = dict(task_record__task=task, status=StatusType.DONE, checker=checker)
        return TaskRecordReview.objects.filter(**filter).count()

    @lru_cache(maxsize=None)
    def get_task_records_done_count(self, task):
        return TaskRecord.objects.done().filter(task=task).count()

    @lru_cache(maxsize=None)
    def get_task_records_count(self, task):
        return TaskRecord.objects.filter(task=task).count()


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    
    serializer_class = TaskSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority', 'checkers']
    pagination_class = None
    ordering = ['-id']
    # Queryset is overridden within the `get_queryset` method
    queryset = Task.objects.none()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Task.objects.none()

        # retrieve projects from tasks where i'm a checker
        my_projects = Task.objects.filter(checkers__in = [self.request.user] ).values('project')
        # retrieve tasks from my projects
        return Task.objects.filter(project__in = my_projects)\
                    .prefetch_related('project') \
                    .prefetch_related('project__creator') \
                    .prefetch_related('choice_group') \
                    .prefetch_related('choice_group__choices')