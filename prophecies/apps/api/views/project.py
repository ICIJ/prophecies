from django.contrib.auth.models import User
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models.project import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    creator = ResourceRelatedField(many=False, queryset=User.objects)

    class Meta:
        model = Project
        fields = ['id', 'url', 'creator', 'name']

    included_serializers = {
        'creator': UserSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['creator']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    search_fields = ['name']
    ordering = ['-id']
    ordering_fields = ['name']
    filterset_fields = ['name']
    pagination_class = None

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None, **kwarg):
        from prophecies.apps.api.views.task import TaskSerializer
        project = self.get_object()
        serializer = TaskSerializer(project.tasks.all(), context={'request': request}, many=True)
        return Response(serializer.data)
