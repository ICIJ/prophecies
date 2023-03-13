from rest_framework import viewsets
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

from prophecies.apps.api.views.alternative_value import AlternativeValue
from prophecies.apps.api.views.alternative_value import AlternativeValueSerializer
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.core.models import Choice, ChoiceGroup


class ChoiceGroupSerializer(serializers.ModelSerializer):
    choices = ResourceRelatedField(many=True, queryset=Choice.objects)
    alternative_values = ResourceRelatedField(many=True, queryset=AlternativeValue.objects)

    included_serializers = {
        'choices': ChoiceSerializer,
        'alternative_values': AlternativeValueSerializer
    }

    class JSONAPIMeta:
        included_resources = ['choices']

    class Meta:
        model = ChoiceGroup
        fields = ['id', 'url', 'name', 'choices', 'alternative_values']


class ChoiceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChoiceGroup.objects.all()
    serializer_class = ChoiceGroupSerializer
    ordering = ['-id']
