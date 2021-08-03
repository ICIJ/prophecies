from rest_framework import filters, viewsets, serializers
from rest_framework_json_api.relations import ResourceRelatedField
from prophecies.core.models import ChoiceGroup, Project, Task
from prophecies.apps.api.views.choice_group import ChoiceGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ResourceRelatedField(many=False, queryset=Project.objects)
    choice_group = ResourceRelatedField(many=False, queryset=ChoiceGroup.objects)
    user_progress_by_round = serializers.SerializerMethodField()
    included_serializers = {
        'choice_group': ChoiceGroupSerializer,
        'project': ProjectSerializer
    }

    class JSONAPIMeta:
        included_resources = ['choice_group', 'project']

    class Meta:
        model = Task
        fields = ['id', 'url', 'choice_group', 'colors', 'description', 'name',
            'project', 'priority', 'user_progress_by_round', 'progress_by_round',
            'progress', 'rounds']

    def get_user_progress_by_round(self, task):
        checker = self.context.get('request').user
        return task.progress_by_round(checker=checker)


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all() \
        .prefetch_related('project') \
        .prefetch_related('project__creator') \
        .prefetch_related('choice_group') \
        .prefetch_related('choice_group__choices')
    serializer_class = TaskSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_fields = ['name', 'rounds', 'priority']
    pagination_class = None
    ordering = ['-id']
