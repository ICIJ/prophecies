from rest_framework import filters, viewsets, serializers
from prophecies.core.models.task import Task
from prophecies.apps.api.views.choice_group import ChoiceGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ProjectSerializer(many=False)
    choice_group = ChoiceGroupSerializer(many=False)
    user_progress_by_round = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'url', 'choice_group', 'colors', 'description', 'name',
            'project', 'priority', 'user_progress_by_round', 'progress_by_round',
            'progress', 'rounds']

    def get_user_progress_by_round(self, task):
        checker = self.context.get('request').user
        return task.progress_by_round(checker=checker)


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all() \
        .prefetch_related('project') \
        .prefetch_related('project__creator') \
        .prefetch_related('choice_group') \
        .prefetch_related('choice_group__choices')
    serializer_class = TaskSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority']
