from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_json_api import serializers, views
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task import TaskSerializer
from prophecies.core.models import TaskUserChoiceStatistics


class TaskUserChoiceStatisticsSerializer(serializers.ModelSerializer):
    choice = ResourceRelatedField(many=False, read_only=True)
    checker = ResourceRelatedField(many=False, read_only=True)
    task = ResourceRelatedField(many=False, read_only=True)

    included_serializers = {
        'checker': UserSerializer,
        'choice': ChoiceSerializer,
        'task': TaskSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['task', 'choice', 'checker']

    class Meta:
        model = TaskUserChoiceStatistics
        resource_name = 'TaskChoiceStatistics'
        fields = [
            'task',
            'checker',
            'choice',
            'round',
            'count',
        ]


@extend_schema_view(
    list=extend_schema(
        operation_id="List TaskUserChoiceStatistics",
        description="Returns a list of TaskUserChoiceStatistics.",
    ),
    retrieve=extend_schema(
        operation_id="Get TaskUserChoiceStatistic",
        description="Get a single TaskUserChoiceStatistic using an ID.",
    ),
)
class TaskUserChoiceStatisticsViewSet(views.ReadOnlyModelViewSet):
    """
    An aggregation of the choices made by a user within a task.
    """
    queryset = TaskUserChoiceStatistics.objects.all()
    serializer_class = TaskUserChoiceStatisticsSerializer
    resource_name = 'TaskChoiceStatistics'
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_fields = ['task',
                        'checker',
                        'choice',
                        'round']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskUserChoiceStatistics.objects.none()
        return super().get_queryset().user_scope(self.request.user)
