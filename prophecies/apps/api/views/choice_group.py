from rest_framework import serializers, viewsets
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import Choice, ChoiceGroup
from prophecies.apps.api.views.choice import ChoiceSerializer


class ChoiceGroupSerializer(serializers.ModelSerializer):
    choices = ResourceRelatedField(many=True, queryset=Choice.objects)

    included_serializers = {
        'choices': ChoiceSerializer
    }

    class JSONAPIMeta:
        included_resources = ['choices']

    class Meta:
        model = ChoiceGroup
        fields = ['id', 'url', 'name', 'choices']


class ChoiceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChoiceGroup.objects.all()
    serializer_class = ChoiceGroupSerializer
    ordering = ['-id']
