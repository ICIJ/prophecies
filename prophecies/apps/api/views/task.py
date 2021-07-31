from rest_framework import filters, viewsets, serializers
from prophecies.core.models.task import Task
from prophecies.apps.api.views.choice_group import ChoiceGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ProjectSerializer(many=False)
    choice_group = ChoiceGroupSerializer(many=False)

    class Meta:
        model = Task
        fields = ['id', 'url', 'choice_group', 'colors', 'description', 'name', 'project', 'priority', 'rounds']


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority']
