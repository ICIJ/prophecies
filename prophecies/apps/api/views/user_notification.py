from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import ResourceRelatedField

from prophecies.apps.api.views.action import ActionSerializer
from prophecies.core.models import UserNotification


class UserNotificationSerializer(serializers.HyperlinkedModelSerializer):
    action = ResourceRelatedField(many=False, read_only=True)

    class Meta:
        model = UserNotification
        fields = ['id', 'url', 'action', 'read', 'read_at', 'created_at']
        read_only_fields = ['action', 'read_at', 'created_at']

    included_serializers = {
        'action': ActionSerializer,
    }

    class JSONAPIMeta:
        included_resources = []


class UserNotificationViewSet(views.ModelViewSet):
    queryset = UserNotification.objects.all()
    prefetch_for_includes = {
        'action': ['action', 'action__actor', 'action__action_object'],
        'action.actor': ['action', 'action__actor'],
        'action.actionObject': ['action', 'action__action_object']
    }
    serializer_class = UserNotificationSerializer
    http_method_names = ['get', 'put', 'head']
    permission_classes = [IsAuthenticated]
    search_fields = []
    ordering = ['-created_at']
    ordering_fields = ['created_at']
    filterset_fields = ['level']
    resource_name = 'UserNotification'

    def get_queryset(self):
        """
        All notifications for the currently authenticated user.
        """
        if not self.request.user.is_authenticated:
            return UserNotification.objects.none()
        return super().get_queryset().filter(recipient=self.request.user)

    def check_object_permissions(self, request, obj):
        if obj.recipient != request.user:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource.')
