from rest_framework import filters, viewsets, serializers, permissions
from prophecies.core.models.task import Task
from prophecies.apps.api.views.project import ProjectSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    colors = serializers.SerializerMethodField()
    project = ProjectSerializer(many=False)

    def get_colors(self, task):
        return [task.color]

    class Meta:
        model = Task
        fields = ['id', 'url', 'colors', 'description', 'name', 'project', 'priority', 'rounds']


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority']
