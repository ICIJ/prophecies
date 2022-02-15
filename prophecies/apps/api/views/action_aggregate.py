from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets
from prophecies.core.models import ActionAggregate
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task import TaskSerializer

class ActionAggregateSerializer(serializers.ModelSerializer):
    
    included_serializers = {
        'user': UserSerializer,
        'task': TaskSerializer,
    }
    
    class JSONAPIMeta:
        included_resources = ['user','task']

    class Meta:
        model = ActionAggregate
        resource_name = 'ActionAggregate'
        fields = ('verb','date','user','task','count')
    

class ActionAggregateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActionAggregateSerializer
    resource_name = 'ActionAggregate'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    ordering = ['-date']
    filterset_fields = ['verb', 'date', 'user_id']
    queryset = ActionAggregate.objects.none()
    
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ActionAggregate.objects.none()
        # retrieve projects from tasks where i'm a checker
        my_projects = ActionAggregate.objects.filter(task__checkers__in = [self.request.user] ).values('task__project')
        # retrieve tasks from my projects
        return ActionAggregate.objects.filter(task__project__in = my_projects)
