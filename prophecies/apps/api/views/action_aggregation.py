from rest_framework_json_api.relations import PolymorphicResourceRelatedField, ResourceRelatedField
from prophecies.apps.api.views.action import GenericModelSerializer
from prophecies.core.models import ActionAggregation
from actstream.models import Action
from django.db.models.expressions import RawSQL
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response
from prophecies.apps.api.views.user import UserSerializer



class ActionAggregationSerializer(serializers.ModelSerializer):
    actor_id = UserSerializer(source='actor', read_only=True)
    class Meta:
        model = ActionAggregation
        resource_name = 'ActionAggregation'
        fields = ('verb','date','actor','actor_id','count')
    
    included_serializers = {
        'actor': UserSerializer,
    }
    
    class JSONAPIMeta:
        included_resources = ['actor']
    

class ActionAggregationViewSet(viewsets.ModelViewSet):
    queryset = ActionAggregation.objects.all()
    serializer_class = ActionAggregationSerializer
    resource_name = 'ActionAggregation'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    ordering = ['-date']

    # def list(self, request, *args, **kwargs):
    #     actions = Action.objects.annotate(
    #         day=RawSQL( 'select DATE(timestamp) as day from actstream_action',() )
    #     )
    #     res = actions.order_by('day').values('verb','actor_object_id','actor_content_type','day').annotate(Count('verb'))
       
    #     serializer = ActionAggregationSerializer(res, many=True)
    #     return Response(serializer.instance)
    # def list(self, request, *args, **kwargs):
    #     res = self.queryset.values('verb','actor','count')
       
    #     serializer = ActionAggregationSerializer(res, many=True)
    #     return Response(serializer.instance)

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