from actstream.models import Action
from rest_framework import exceptions, serializers, status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum,Count

class ActionAggregationSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(required=True)

    class Meta:
        model = Action
        fields = ('id', 'actor_object_id','verb')

class ActionAggregationViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionAggregationSerializer
    resource_name = 'ActionAggregation'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(verb=verb).values('id', 'actor_object_id','verb').annotate(count_by_verb =Count('verb'))
        


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