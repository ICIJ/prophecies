from rest_framework import viewsets, serializers
from prophecies.core.models.task_record import TaskRecord
from prophecies.apps.api.views.task import TaskSerializer

class TaskRecordSerializer(serializers.HyperlinkedModelSerializer):
    task = TaskSerializer(many=False)
    link = serializers.SerializerMethodField()

    class Meta:
        model = TaskRecord
        fields = ['id', 'url', 'task', 'original_value', 'suggested_value', 'link', 'metadata', 'rounds', 'status']

    def get_link(self, task_record):
        return task_record.computed_link()


class TaskRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskRecord.objects.all()
    serializer_class = TaskRecordSerializer
