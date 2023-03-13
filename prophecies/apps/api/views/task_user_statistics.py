from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField

from prophecies.apps.api.views.task import TaskSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models import TaskUserStatistics


class TaskUserStatisticsSerializer(serializers.ModelSerializer):
    checker = ResourceRelatedField(many=False, read_only=True)
    task = ResourceRelatedField(many=False, read_only=True)

    included_serializers = {
        'checker': UserSerializer,
        'task': TaskSerializer,
    }

    # class JSONAPIMeta:
    #     included_resources = ['task', 'checker']

    class Meta:
        model = TaskUserStatistics
        resource_name = 'TaskUserStatistics'
        fields = [
            'task',
            'checker',
            'round',
            'done_count',
            'pending_count',
            'total_count',
            'progress',
        ]


class TaskUserStatisticsViewSet(views.ReadOnlyModelViewSet):
    queryset = TaskUserStatistics.objects.all()
    serializer_class = TaskUserStatisticsSerializer
    resource_name = 'TaskUserStatistics'
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_fields = ['task',
                        'checker',
                        'round']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskUserStatistics.objects.none()
        return super().get_queryset().user_scope(self.request.user)
