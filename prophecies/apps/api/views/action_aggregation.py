from prophecies.core.models import ActionAggregate
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from prophecies.apps.api.views.user import UserSerializer

class ActionAggregationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionAggregate
        resource_name = 'ActionAggregation'
        fields = ('verb','date','actor','actor_id','count')
    
    included_serializers = {
        'actor': UserSerializer,
    }
    
    class JSONAPIMeta:
        included_resources = ['actor']
    

class ActionAggregationViewSet(viewsets.ModelViewSet):
    queryset = ActionAggregate.objects.all()
    serializer_class = ActionAggregationSerializer
    resource_name = 'ActionAggregation'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    ordering = ['-date']
    filterset_fields = ['verb', 'date', 'actor_id']

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