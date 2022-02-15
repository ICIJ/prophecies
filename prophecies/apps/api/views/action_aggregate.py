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
    filterset_fields = ['verb', 'date', 'user']

    queryset = ActionAggregate.objects.all()
            
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ActionAggregate.objects.none()
        return super().get_queryset().user_scope(self.request.user)
