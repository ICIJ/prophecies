from rest_framework_json_api import serializers
from prophecies.core.models import Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'name', 'value', 'shortkeys', 'require_alternative_value', 'color']
