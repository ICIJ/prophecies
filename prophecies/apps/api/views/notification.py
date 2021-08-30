from actstream.models import Action
from django.contrib.auth.models import User
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from prophecies.apps.api.views.action import ActionSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.core.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient = ResourceRelatedField(many=False, queryset=User.objects)
    action = ResourceRelatedField(many=False, queryset=Action.objects)

    class Meta:
        model = Notification
        fields = ['id', 'url', 'recipient', 'action', 'read', 'read_at']

    included_serializers = {
        'recipient': UserSerializer,
        'action': ActionSerializer,
    }

    class JSONAPIMeta:
        included_resources = ['recipient', 'action']


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    search_fields = []
    ordering = ['-created_at']
    ordering_fields = ['created_at']
    filterset_fields = ['level']


    def get_queryset(self):
        """
        All notifications for the currently authenticated user.
        """
        if not self.request.user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user)
