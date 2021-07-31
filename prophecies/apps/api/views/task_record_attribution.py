from rest_framework import viewsets, serializers
from prophecies.core.models import Choice, TaskRecordAttribution
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.task_record import TaskRecordSerializer


class TaskRecordAttributionSerializer(serializers.HyperlinkedModelSerializer):
    task_record = TaskRecordSerializer(many=False, read_only=True)
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = TaskRecordAttribution
        fields = ['id', 'url', 'choice', 'status', 'note', 'alternative_value', 'task_record']
        read_only_fields = ['task_record', 'status']

    def __init__(self, *args, **kwargs):
        self.filter_choice_queryset(self.fields['choice'], *args, **kwargs)
        super().__init__(*args, **kwargs)

    def filter_choice_queryset(self, f, instance=None, data=serializers.empty, request=None, **kwargs):
        if instance is None or not hasattr(instance, 'task_record'):
            return
        f.queryset = instance.task_record.task.choice_group.choices.all()


class TaskRecordAttributionViewSet(viewsets.ModelViewSet):
    serializer_class = TaskRecordAttributionSerializer
    queryset = TaskRecordAttribution.objects.all()
    http_method_names = ['get', 'put', 'head']

    def get_queryset(self):
        """
        All the task record attribution for the currently authenticated user.
        """
        return TaskRecordAttribution.objects.filter(checker=self.request.user).prefetch_related('task_record')
