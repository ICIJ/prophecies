from actstream import action
from colorfield.fields import ColorField
from django.apps import apps
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.task_template_setting import TaskTemplateSetting
from prophecies.core.models.project import Project
from prophecies.core.models.choice_group import ChoiceGroup
from prophecies.core.contrib.colors import hex_scale_brightness


class StatusType(models.TextChoices):
    OPEN = "OPEN", _("Open")
    CLOSED = "CLOSED", _("Closed")
    LOCKED = "LOCKED", _("Locked")


class TemplateType(models.TextChoices):
    TEXT = "TEXT", _("Text Task")
    MEDIA = "MEDIA", _("Media Task")
    IFRAME = "IFRAME", _("Iframe Task")


class TaskQuerySet(models.QuerySet):
    def user_scope(self, user):
        projects = self.filter(checkers=user).values("project")
        return self.filter(project__in=projects)


class TaskManager(models.Manager):
    def user_scope(self, user):
        return self.get_queryset().user_scope(user)

    def get_queryset(self) -> TaskQuerySet:
        return TaskQuerySet(model=self.model, using=self._db, hints=self._hints)


class Task(models.Model):
    objects = TaskManager()

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Project this task belong to",
    )
    checkers = models.ManyToManyField(
        User,
        through="TaskChecker",
        through_fields=("task", "checker"),
        verbose_name="User in charge of checking this task's data",
        related_name="task",
    )
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    rounds = models.PositiveIntegerField(default=3, verbose_name="Number of rounds")
    automatic_round_attributions = models.BooleanField(
        default=False,
        verbose_name="Attribute rounds (if not checked, "
        "all checkers will participate in all rounds)",
    )
    allow_multiple_checks = models.BooleanField(
        default=False, verbose_name="Allow checkers to check several time the same item"
    )
    allow_items_addition = models.BooleanField(
        default=False, verbose_name="Allow checker to add items (not implemented yet)"
    )
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    choice_group = models.ForeignKey(
        ChoiceGroup,
        verbose_name="Choices",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    color = ColorField(default="#31807D")
    record_link_template = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Record link template",
        help_text="A link template to build a link for each task record. "
        "Task record can override this value with their own link",
    )
    embeddable_links = models.BooleanField(
        default=False,
        verbose_name="Allow end-users to preview links within an iframe "
        "(targeted website must allow it)",
    )
    embeddable_record_link_template = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Embeddable record link template",
        help_text="An optional alternative link template "
        "to use within the link preview.",
    )
    status = models.CharField(
        blank=True,
        choices=StatusType.choices,
        default=StatusType.OPEN,
        max_length=6,
        help_text="Status of the task. Set to closed or locked will prevent "
        "any update of the records.",
    )
    template_type = models.CharField(
        max_length=16,
        choices=TemplateType.choices,
        default=TemplateType.TEXT,
        help_text="Template type to use to display the task.",
    )
    template_setting = models.OneToOneField(
        TaskTemplateSetting,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="task",
        help_text="Each template type has its own set of settings.",
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

    @property
    def cache_key(self):
        app_label = self._meta.app_label
        model_name = self._meta.model_name
        return f"{app_label}:{model_name}:{self.pk}"

    @property
    def progress(self):
        cache_key = self.progress_cache_key()
        progress = cache.get(cache_key)
        if progress is None:
            from prophecies.core.models.task_record_review import (
                TaskRecordReview,
                StatusType as st,
            )

            tasks_reviews = TaskRecordReview.objects.filter(
                task_record__task_id=self.id
            )
            done_reviews = tasks_reviews.filter(status=st.DONE)
            all_reviews = len(tasks_reviews)
            done_reviews = len(done_reviews)
            progress = 100 if all_reviews == 0 else done_reviews / all_reviews * 100
            cache.set(cache_key, progress, timeout=300)
        return progress

    def progress_cache_key(self):
        return f"{self.cache_key}:progress"

    def progress_by_round(self, **task_record_review_filter):
        cache_key = self.progress_by_round_cache_key(**task_record_review_filter)
        progress = cache.get(cache_key)
        if progress is None:
            from prophecies.core.models.task_record_review import TaskRecordReview

            filter = dict(task_record__task=self, **task_record_review_filter)
            progress = TaskRecordReview.objects.progress_by_round(**filter)
            # Get all task's rounds to only display the progress by existing rounds
            rounds = range(1, self.rounds + 1)
            progress = {round: progress.get(round, 0) for round in rounds}
            cache.set(cache_key, progress, timeout=300)
        return progress

    def progress_by_round_cache_key(self, **task_record_review_filter):
        hash_key = hash(frozenset(task_record_review_filter.items()))
        return f"{self.cache_key}:progress_by_round:{hash_key}"

    @property
    def records_done_count(self):
        cache_key = f"{self.cache_key}:records_done_count"
        count = cache.get(cache_key)
        if count is None:
            from prophecies.core.models.task_record_review import TaskRecord

            count = TaskRecord.objects.done().filter(task=self).count()
            cache.set(cache_key, count, timeout=60)
        return count

    @property
    def records_count(self):
        cache_key = f"{self.cache_key}:records_count"
        count = cache.get(cache_key)
        if count is None:
            from prophecies.core.models.task_record_review import TaskRecord

            count = TaskRecord.objects.filter(task=self).count()
            cache.set(cache_key, count, timeout=60)
        return count

    def open(self):
        self.status = StatusType.OPEN
        self.save()

    def close(self):
        self.status = StatusType.CLOSED
        self.save()

    def lock(self):
        self.status = StatusType.LOCKED
        self.save()

    @property
    def is_open(self):
        return self.status == StatusType.OPEN

    @property
    def is_closed(self):
        return self.status == StatusType.CLOSED

    @property
    def is_locked(self):
        return self.status == StatusType.LOCKED

    @staticmethod
    def has_attribute_changed(current_instance, attribute_name):
        if current_instance.pk is not None:
            instance = Task.objects.get(pk=current_instance.pk)
            return getattr(current_instance, attribute_name) != getattr(
                instance, attribute_name
            )
        return False

    @property
    def is_open_changed(self):
        return Task.has_attribute_changed(self, "is_open")

    @property
    def is_closed_changed(self):
        return Task.has_attribute_changed(self, "is_closed")

    @property
    def is_locked_changed(self):
        return Task.has_attribute_changed(self, "is_locked")

    @property
    def template_type_model(self):
        model_mapping = {
            TemplateType.TEXT: apps.get_model("core", "TaskTemplateSettingForText"),
            TemplateType.MEDIA: apps.get_model("core", "TaskTemplateSettingForMedia"),
            TemplateType.IFRAME: apps.get_model("core", "TaskTemplateSettingForIframe"),
        }
        return model_mapping[self.template_type]

    @cached_property
    def colors(self):
        """
        Generate 3 colors tones based on the `color` attribute
        """
        scales = [0.75, 1.0, 1.25]
        return tuple(hex_scale_brightness(self.color, s) for s in scales)

    @staticmethod
    def signal_log_task_locked(
        sender, instance, **kwargs
    ):  # pylint: disable=unused-argument
        if instance.is_locked_changed and instance.is_locked:
            if instance.creator:
                action.send(instance.creator, verb="locked", target=instance)

    @staticmethod
    def signal_log_task_closed(
        sender, instance, **kwargs
    ):  # pylint: disable=unused-argument
        if instance.is_closed_changed and instance.is_closed:
            if instance.creator:
                action.send(instance.creator, verb="closed", target=instance)

    @staticmethod
    def signal_log_task_open(
        sender, instance, **kwargs
    ):  # pylint: disable=unused-argument
        if instance.is_open_changed and instance.is_open:
            if instance.creator:
                action.send(instance.creator, verb="open", target=instance)

    @staticmethod
    def signal_delete_orphan_template_settings(
        sender, *args, **kwargs
    ):  # pylint: disable=unused-argument
        for task_template_settings in TaskTemplateSetting.objects.all():
            if not hasattr(task_template_settings, 'task'):
                task_template_settings.delete()


signals.pre_save.connect(Task.signal_log_task_locked, sender=Task)
signals.pre_save.connect(Task.signal_log_task_closed, sender=Task)
signals.pre_save.connect(Task.signal_log_task_open, sender=Task)
signals.post_save.connect(Task.signal_delete_orphan_template_settings, sender=Task)
