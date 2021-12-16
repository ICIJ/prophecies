from prophecies.core.models import ActionAggregate
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
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
    

class ActionAggregateViewSet(viewsets.ModelViewSet):
    queryset = ActionAggregate.objects.all()
    serializer_class = ActionAggregateSerializer
    resource_name = 'ActionAggregate'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    ordering = ['-date']
    filterset_fields = ['verb', 'date', 'user_id']

"""
/action-aggregations/?filter[actor=13]
{
    data:[
        {
            attributes: {
                ts:101010101,
                type:"day"
                actions:
                    [
                        {
                            actor:'13',
                            verb:'reviewed'
                            targetType:'TaskRecordReview'
                            count:25
                        }
                    ]
            }
        }
    ]
}

"""