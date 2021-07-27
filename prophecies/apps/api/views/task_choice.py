from rest_framework import serializers
from prophecies.core.models.task_choice import TaskChoice

class TaskChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChoice
        fields = ['id', 'name', 'value']
