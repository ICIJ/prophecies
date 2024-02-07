from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from prophecies.core.filters import ActionAggregateFilter
from prophecies.core.models import ActionAggregate
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task import TaskSerializer


class ActionAggregateSerializer(serializers.ModelSerializer):
    included_serializers = {
        'user': UserSerializer,
        'task': TaskSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['user', 'task']

    class Meta:
        model = ActionAggregate
        resource_name = 'ActionAggregate'
        fields = ('verb', 'date', 'user', 'task', 'count')


@extend_schema_view(
    list=extend_schema(
        operation_id="List ActionAggregates",
        description="Returns a list of ActionAggregates.",
    ),
    retrieve=extend_schema(
        operation_id="Get ActionAggregate",
        description="Get a single ActionAggregate using an ID.",
    ),
)
class ActionAggregateViewSet(views.ReadOnlyModelViewSet):
    serializer_class = ActionAggregateSerializer
    resource_name = 'ActionAggregate'
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    ordering = ['-date']
    filterset_class = ActionAggregateFilter
    filter_backends = [DjangoFilterBackend]
    queryset = ActionAggregate.objects.all().order_by('-date')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ActionAggregate.objects.none()
        return super().get_queryset().user_scope(self.request.user)
