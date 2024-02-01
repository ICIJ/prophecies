from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views

from prophecies.core.models import TaskRecordMedia


class TaskRecordMediaSerializer(serializers.HyperlinkedModelSerializer):
    task_id = serializers.CharField(read_only=True)
    task_record_id = serializers.CharField(read_only=True)
    uid = serializers.CharField()

    class JSONAPIMeta:
        included_resources = []

    class Meta:
        model = TaskRecordMedia
        fields = [
            "id",
            "file",
            "media_type",
            "mime_type",
            "task_id",
            "task_record_id",
            "uid",
            "url",
        ]


class TaskRecordMediaViewSet(views.ModelViewSet):
    """
    A list of media associated with a task record (usually by their common uid).
    """
    
    resource_name = "TaskRecordMedia"
    serializer_class = TaskRecordMediaSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    search_fields = ["uid"]
    ordering = ["-created_at"]
    ordering_fields = ["created_at"]
    # Queryset is overridden within the `get_queryset` method
    queryset = TaskRecordMedia.objects.none()

    def get_queryset(self):
        """
        All the task record attribution for the currently authenticated user.
        """
        if not self.request.user.is_authenticated:
            return TaskRecordMedia.objects.none()
        return TaskRecordMedia.objects.user_scope(self.request.user)
