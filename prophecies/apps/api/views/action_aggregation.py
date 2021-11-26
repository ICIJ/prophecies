from prophecies.core.models import ActionAggregation
from actstream.models import Action
from django.db.models.expressions import RawSQL
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response
import uuid

class ActionAggregationSerializer(serializers.Serializer):
  
    class Meta:
        model = ActionAggregation
        fields = ('verb','actor_object_id','day')

class ActionAggregationViewSet(viewsets.ViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionAggregationSerializer
    resource_name = 'ActionAggregation'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        actions = Action.objects.annotate(
            day=RawSQL( 'select DATE(timestamp) as day from actstream_action',() )
        )
        res = actions.order_by('day').values('verb','actor_object_id','day').annotate(Count('verb'))
       
        serializer = ActionAggregationSerializer(res, many=True)
        return Response(serializer.instance)

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