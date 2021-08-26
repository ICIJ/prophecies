from actstream.models import Action
from rest_framework import viewsets
from rest_framework_json_api import serializers


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    actor = serializers.SerializerMethodField()
    action_object = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    def get_actor(self, action):
        return action.actor_object_id

    def get_target(self, action):
        return action.target_object_id

    def get_action_object(self, action):
        return action.action_object_object_id

    class Meta:
        model = Action
        fields = ['id', 'verb', 'actor', 'action_object', 'target', 'public',
                    'description', 'timestamp']


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    ordering = ['-id']
