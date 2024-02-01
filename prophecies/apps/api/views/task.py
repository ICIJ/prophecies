from functools import lru_cache
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import serializers, views
from rest_framework_json_api.relations import (
    ResourceRelatedField,
    PolymorphicResourceRelatedField,
)
from prophecies.core.models import Task, TaskRecordReview, TaskTemplateSetting
from prophecies.core.models.task_record import StatusType
from prophecies.apps.api.views.choice_group import ChoiceGroupSerializer
from prophecies.apps.api.views.project import ProjectSerializer
from prophecies.apps.api.views.user import UserSerializer
from prophecies.apps.api.views.task_template_settings import (
    TaskTemplateSettingSerializer,
)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    project = ResourceRelatedField(many=False, read_only=True)
    checkers = ResourceRelatedField(many=True, read_only=True)
    choice_group = ResourceRelatedField(many=False, read_only=True)
    task_records_count = serializers.SerializerMethodField()
    task_records_done_count = serializers.SerializerMethodField()
    template_setting = PolymorphicResourceRelatedField(
        TaskTemplateSettingSerializer,
        queryset=TaskTemplateSetting.objects.all(),
        many=False,
    )
    user_task_records_count = serializers.SerializerMethodField()
    user_task_records_done_count = serializers.SerializerMethodField()
    user_progress_by_round = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    included_serializers = {
        "checkers": UserSerializer,
        "choice_group": ChoiceGroupSerializer,
        "project": ProjectSerializer,
        "template_setting": TaskTemplateSettingSerializer,
    }

    class JSONAPIMeta:
        included_resources = ["project", "template_setting"]

    class Meta:
        model = Task
        fields = [
            "id",
            "checkers",
            "choice_group",
            "colors",
            "created_at",
            "description",
            "embeddable_links",
            "name",
            "priority",
            "progress_by_round",
            "progress",
            "project",
            "rounds",
            "status",
            "task_records_count",
            "task_records_done_count",
            "template_setting",
            "template_type",
            "url",
            "user_progress_by_round",
            "user_progress",
            "user_task_records_count",
            "user_task_records_done_count",
        ]

    @lru_cache(maxsize=None)
    def get_user_progress_by_round(self, task):
        checker = self.context.get("request").user
        return task.progress_by_round(checker=checker)

    @lru_cache(maxsize=None)
    def get_user_progress(self, task):
        all_records = self.get_user_task_records_count(task)
        # No records assigned to that user
        if all_records == 0:
            return 100
        else:
            user_records = self.get_user_task_records_done_count(task)
            return user_records / all_records * 100

    @lru_cache(maxsize=None)
    def get_user_task_records_count(self, task):
        checker = self.context.get("request").user
        filter = dict(task_record__task=task, checker=checker)
        return TaskRecordReview.objects.filter(**filter).count()

    @lru_cache(maxsize=None)
    def get_user_task_records_done_count(self, task):
        checker = self.context.get("request").user
        filter = dict(task_record__task=task, status=StatusType.DONE, checker=checker)
        return TaskRecordReview.objects.filter(**filter).count()

    def get_task_records_done_count(self, task):
        return task.records_done_count

    def get_task_records_count(self, task):
        return task.records_count


class TaskViewSet(views.ReadOnlyModelViewSet):
    """
    Each task, or list of records, that must be verified under a specific set of rules. For instance, a list of "Paintings locations" to check. A task can have many options, including the type of form to use, the type of options present, the number of rounds of checks, etc.
    """

    permission_classes = [IsAuthenticated]
    prefetch_for_includes = {
        "project": ["project", "project__creator"],
        "template_setting": ["template_setting"],
        "choice_group": ["choice_group", "choice_group__choices"],
    }
    serializer_class = TaskSerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    filterset_fields = ["name", "rounds", "priority", "checkers"]
    pagination_class = None
    ordering = ["-id"]
    # Queryset is overridden within the `get_queryset` method
    queryset = Task.objects.all()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Task.objects.none()
        return super().get_queryset().user_scope(self.request.user)
