from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_json_api import serializers
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


class TipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TipSerializer
    prefetch_for_includes = {
        'project': ['project'],
        'creator': ['creator'],
        'task': ['task']
    }
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = {
        'name': ('exact',),
        'project': ('exact',),
        'task': ('exact',),
        'creator': ('exact',),
        'id': ('exact','in',),
    }
    pagination_class = None
    ordering = ['-id']
    permission_classes = [IsAuthenticated]
    queryset = Tip.objects.none()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tip.objects.none()
    
        my_projects = Tip.objects.filter(task__checkers__in = [self.request.user] ).values('task__project')
        
        return Tip.objects.user_scope(self.request.user) \
            .filter(project__in= my_projects)

