from rest_framework import serializers
from prophecies.core.models.choice_group import ChoiceGroup
from prophecies.apps.api.views.choice import ChoiceSerializer


class ChoiceGroupSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = ChoiceGroup
        fields = ['id', 'name', 'choices']
