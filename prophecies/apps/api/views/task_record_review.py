from rest_framework import viewsets, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from prophecies.core.models import Choice, TaskRecordReview
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.task_record import TaskRecordSerializer


class TaskRecordReviewSerializer(serializers.HyperlinkedModelSerializer):
    task_record = TaskRecordSerializer(many=False, read_only=True)
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = TaskRecordReview
        fields = ['id', 'url', 'choice', 'status', 'note', 'alternative_value', 'task_record']
        read_only_fields = ['task_record', 'status']

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


class TaskRecordReviewViewSet(viewsets.ModelViewSet):
    serializer_class = TaskRecordReviewSerializer
    queryset = TaskRecordReview.objects.all()
    http_method_names = ['get', 'put', 'head']
    permission_classes = [IsAuthenticated]
    search_fields = ['task_record__original_value', 'task_record__suggested_value']
    ordering_fields = ['task_record__original_value', 'task_record__suggested_value', 'task_record__id']
    filterset_fields = ['task_record__original_value', 'task_record__suggested_value']

    def get_queryset(self):
        """
        All the task record attribution for the currently authenticated user.
        """
        return TaskRecordReview.objects \
            .filter(checker=self.request.user) \
            .prefetch_related('task_record', 'task_record__task', 'task_record__task__project', 'checker')


    def check_object_permissions(self, request, obj):
        if obj.checker != request.user:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource.')
