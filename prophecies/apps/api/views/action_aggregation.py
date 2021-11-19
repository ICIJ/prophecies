from actstream.models import Action
from django.db.models.expressions import RawSQL
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response

class ActionAggregationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'verb', 'timestamp')


class ActionAggregationViewSet(viewsets.ModelViewSet):
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
       
        return Response(res)

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