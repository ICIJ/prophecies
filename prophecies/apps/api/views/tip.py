from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import Tip
from prophecies.apps.api.views.project import ProjectSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task import TaskSerializer


class TipSerializer(serializers.HyperlinkedModelSerializer):
    project = ResourceRelatedField(many=False, read_only=True)
    creator = ResourceRelatedField(many=False, read_only=True)
    task = ResourceRelatedField(many=False, read_only=True)

    included_serializers = {
        'creator': UserSerializer,
        'project': ProjectSerializer,
        'task': TaskSerializer
    }

    class JSONAPIMeta:
        included_resources = []

    class Meta:
        model = Tip
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'project', 'creator', 'task']


class TipViewSet(views.ReadOnlyModelViewSet):
    """
    A list of tips for end users, associated with a task or a whole project.
    """

    serializer_class = TipSerializer
    prefetch_for_includes = {
        'project': ['project'],
        'creator': ['creator'],
        'task': ['task']
    }
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    filterset_fields = {
        'name': ('exact',),
        'project': ('exact',),
        'task': ('exact',),
        'creator': ('exact',),
        'id': ('exact', 'in',),
    }
    pagination_class = None
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]
    queryset = Tip.objects.all()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tip.objects.none()
        return super().get_queryset().user_scope(self.request.user)
