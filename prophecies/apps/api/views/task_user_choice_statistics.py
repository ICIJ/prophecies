from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField

from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.task import TaskSerializer
from prophecies.apps.api.views.user import UserSerializer
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


class TaskUserChoiceStatisticsViewSet(views.ReadOnlyModelViewSet):
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
