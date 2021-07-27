from rest_framework import filters, viewsets, serializers, permissions
from prophecies.core.models.task import Task
from prophecies.apps.api.views.task_choices_group import TaskChoicesGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ProjectSerializer(many=False)
    choices_group = TaskChoicesGroupSerializer(many=False)

    def get_colors(self, task):
        return [task.color]

    class Meta:
        model = Task
        fields = ['id', 'url', 'choices_group', 'colors', 'description', 'name', 'project', 'priority', 'rounds']


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority']
