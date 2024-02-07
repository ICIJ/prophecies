from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework.response import Response
from rest_framework.decorators import action
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models.project import Project


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


@extend_schema_view(
    list=extend_schema(
        operation_id="List Projects",
        description="Returns a list of Projects.",
    ),
    tasks=extend_schema(
        operation_id="List Project's Tasks",
        description="List a Project's Tasks  using an ID.",
    ),
    retrieve=extend_schema(
        operation_id="Get Project",
        description="Get a single Project using an ID.",
    ),
)
class ProjectViewSet(views.ReadOnlyModelViewSet):
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
