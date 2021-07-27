from rest_framework import serializers
from prophecies.core.models.task_choices_group import TaskChoicesGroup
from prophecies.apps.api.views.task_choice import TaskChoiceSerializer


class TaskChoicesGroupSerializer(serializers.ModelSerializer):
    choices = TaskChoiceSerializer(many=True)

    class Meta:
        model = TaskChoicesGroup
        fields = ['name', 'choices']
