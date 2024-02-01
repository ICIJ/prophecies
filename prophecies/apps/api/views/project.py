from django.contrib.auth.models import User
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework.response import Response
from rest_framework.decorators import action
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models.project import Project

from rest_framework_json_api.utils import get_included_resources


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    creator = ResourceRelatedField(many=False, queryset=User.objects)
    included_serializers = {
        "creator": UserSerializer,
    }

    class Meta:
        model = Project
        fields = ["id", "url", "creator", "name"]

    class JSONAPIMeta:
        included_resources = []


class ProjectViewSet(views.ReadOnlyModelViewSet):
    """
    A group of tasks to verify. For instance "Pandora Papers" is a project.
    """

    queryset = Project.objects.all()
    select_for_includes = {"creator": ["creator"]}
    serializer_class = ProjectSerializer
    search_fields = ["name"]
    ordering = ["-id"]
    ordering_fields = ["name"]
    filterset_fields = ["name"]
    pagination_class = None

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None, **kwarg):
        from prophecies.apps.api.views.task import TaskSerializer

        project = self.get_object()
        serializer = TaskSerializer(
            project.tasks.all(), context={"request": request}, many=True
        )
        return Response(serializer.data)
