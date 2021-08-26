from actstream.models import Action
from rest_framework import viewsets
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    actor = ResourceRelatedField(many=False, read_only=True)
    action_object = ResourceRelatedField(many=False, read_only=True)
    target = ResourceRelatedField(many=False, read_only=True)

    included_serializers = {
        'actor': 'prophecies.apps.api.views.user.UserSerializer',
    }

    class Meta:
        model = Action
        fields = ['id', 'verb', 'actor', 'action_object', 'target', 'public',
                    'description', 'timestamp']

    class JSONAPIMeta:
        included_resources = ['actor']


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    ordering = ['-timestamp']
