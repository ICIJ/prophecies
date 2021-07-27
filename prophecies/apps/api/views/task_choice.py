from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from prophecies.core.models.task_choice import TaskChoice

class TaskChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChoice
        fields = ['id', 'name', 'value']
