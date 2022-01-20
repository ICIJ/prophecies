from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task import TaskSerializer
from prophecies.core.models import TaskUserChoiceStatistics,Choice

   
class TaskUserChoiceStatisticsSerializer(serializers.ModelSerializer):
    choice_id = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all(), source='choice', write_only=True)
    choice = ResourceRelatedField(many=False, read_only=True)
    checker = ResourceRelatedField(many=False, read_only=True)
    task = ResourceRelatedField(many=False, read_only=True)

    included_serializers = {
        'checker': UserSerializer,
        'choice': ChoiceSerializer,
        'task': TaskSerializer,
    }
    
    class JSONAPIMeta:
        included_resources = ['task', 'choice','checker']

    class Meta:
        model = TaskUserChoiceStatistics
        resource_name = 'TaskChoiceStatistics'
        fields = [
                    'task',
                    'checker',
                    'choice_id',
                    'choice',
                    'round',
                    'count',
                ]
        
class TaskUserChoiceStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskUserChoiceStatistics.objects.none()
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
        return TaskUserChoiceStatistics.objects.filter(task__in=self.request.user.task.all())
    