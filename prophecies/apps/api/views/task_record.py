from rest_framework import viewsets, serializers
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import Task, TaskRecord
from prophecies.apps.api.views.task import TaskSerializer

class TaskRecordSerializer(serializers.HyperlinkedModelSerializer):
    task = ResourceRelatedField(many=False, queryset=Task.objects)
    link = serializers.SerializerMethodField()
    included_serializers = {
        'task': TaskSerializer
    }

    class JSONAPIMeta:
        included_resources = ['task']

    class Meta:
        model = TaskRecord
        fields = ['id', 'url', 'task', 'original_value', 'predicted_value', 'link', 'metadata', 'rounds', 'status']

    def get_link(self, task_record):
        return task_record.computed_link()


class TaskRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskRecord.objects.all()
    serializer_class = TaskRecordSerializer
    ordering = ['-id']
