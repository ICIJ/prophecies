from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models.project import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    creator = UserSerializer(many=False)

    class Meta:
        model = Project
        fields = ['id', 'url', 'creator', 'name']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = ['name']

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None, **kwarg):
        from prophecies.apps.api.views.task import TaskSerializer
        project = self.get_object()
        serializer = TaskSerializer(project.tasks.all(), context={'request': request}, many=True)
        return Response(serializer.data)
