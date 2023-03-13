from rest_framework_json_api import serializers

from prophecies.core.models import AlternativeValue


class AlternativeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeValue
        fields = ['id', 'name', 'value']
