from rest_framework import viewsets
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import Choice, ChoiceGroup
from prophecies.apps.api.views.choice import ChoiceSerializer
from prophecies.apps.api.views.alternative_value import AlternativeValueSerializer
from prophecies.apps.api.views.alternative_value import AlternativeValue


class ChoiceGroupSerializer(serializers.ModelSerializer):
    choices = ResourceRelatedField(many=True, queryset=Choice.objects)
    alternative_values = ResourceRelatedField(
        many=True, queryset=AlternativeValue.objects
    )

    included_serializers = {
        "choices": ChoiceSerializer,
        "alternative_values": AlternativeValueSerializer,
    }

    class JSONAPIMeta:
        included_resources = ["choices"]

    class Meta:
        model = ChoiceGroup
        fields = ["id", "url", "name", "choices", "alternative_values"]


class ChoiceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A list of options that will be presented to the checker when reviewing a record. For instance "Correct", "Incorrect" and "I don't know". An option can be mark as "requiring an alternative value". For instance if you pick incorrect when reviewing an address, you might have to select the correct country.
    """
    queryset = ChoiceGroup.objects.all()
    serializer_class = ChoiceGroupSerializer
    ordering = ["-id"]
