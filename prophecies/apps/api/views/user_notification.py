from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework import exceptions, viewsets
from rest_framework.permissions import IsAuthenticated
from prophecies.apps.api.views.action import ActionSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models import UserNotification


class UserNotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient = ResourceRelatedField(many=False, read_only=True)
    action = ResourceRelatedField(many=False, read_only=True)

    class Meta:
        model = UserNotification
        fields = ['id', 'url', 'recipient', 'action', 'read', 'read_at', 'created_at']
        read_only_fields = ['recipient', 'action', 'read_at', 'created_at']

    included_serializers = {
        'recipient': UserSerializer,
        'action': ActionSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['recipient', 'action']


class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.none()
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
        return UserNotification.objects \
            .filter(recipient=self.request.user) \
            .select_related('action') \
            .select_related('recipient')


    def check_object_permissions(self, request, obj):
        if obj.recipient != request.user:
            raise exceptions.PermissionDenied(detail='You do not have permission to update this resource.')
