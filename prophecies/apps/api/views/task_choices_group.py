from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from prophecies.core.models.task_choices_group import TaskChoicesGroup
from prophecies.apps.api.views.task_choice import TaskChoiceSerializer


class TaskChoicesGroupSerializer(serializers.ModelSerializer):
    choices = TaskChoiceSerializer(many=True)

    class Meta:
        model = TaskChoicesGroup
        fields = ['name', 'choices']
