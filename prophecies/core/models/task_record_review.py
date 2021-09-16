import re
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, signals
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from prophecies.core.models import Choice, TaskChecker, TaskRecord, Task, Project, UserNotification
from prophecies.core.contrib.mentions import list_mentions, get_or_create_mention_action

class StatusType(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    DONE = 'DONE', _('Done')


class TaskRecordReviewManager(models.Manager):

    def latest_round(self, task_record):
        if self.filter(task_record=task_record).exists():
            latest = self.filter(task_record=task_record).latest()
            return latest.round
        return 0


    def pending(self):
        return self.filter(status=StatusType.PENDING)


    def done(self):
        return self.filter(status=StatusType.DONE)


    def all_by_round(self, **filter):
        buckets = self.all() \
            .filter(**filter) \
            .values('round') \
            .annotate(count=models.Count('round')) \
            .order_by('count')
        return { i['round']: i['count'] for i in buckets }


    def done_by_round(self, **filter):
        buckets = self.done() \
            .filter(**filter) \
            .values('round') \
            .annotate(count=models.Count('round')) \
            .order_by('count')
        return { i['round']: i['count'] for i in buckets }


    def progress_by_round(self, **filter):
        all = self.all_by_round(**filter)
        done = self.done_by_round(**filter)
        # A lambda to calculate the progression for a given round
        progress = lambda round, total: done.get(round, 0) / total * 100
        # Return a dictionnary combinings both aggregations dict
        return { round: progress(round, count) for (round, count) in all.items() }



class TaskRecordReview(models.Model):
    objects = TaskRecordReviewManager()


    class Meta:
        unique_together = ('task_record_id', 'checker_id')
        get_latest_by = 'round'


    task_record = models.ForeignKey(TaskRecord, null=True, on_delete=models.SET_NULL, related_name='reviews')
    checker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='reviews')
    round = models.PositiveIntegerField(verbose_name="Attribution round", null=True, default=None)
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=7)
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=100, null=True, blank=True, verbose_name="Checker note")
    note_created_at = models.DateTimeField(null=True, blank=True)
    note_updated_at = models.DateTimeField(null=True, blank=True)
    alternative_value = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.round is None:
            self.round = TaskRecordReview.objects.latest_round(self.task_record) + 1


    def __str__(self):
        return f'Task record #{self.task_record.id} on round {self.round}'


    @property
    def mentioned_project(self):
        project = re.findall("(?i)@project", str(self.note))
        if len(project) > 0:
            return self.project

    @property
    def project(self):
        try:
            return self.task_record.task.project
        except AttributeError:
            return None


    @property
    def mentioned_task(self):
        task = re.findall("(?i)@task", str(self.note))
        if len(task) > 0:
            try:
                return self.task_record.task
            except AttributeError:
                return None


    @property
    def task_id(self):
        try:
            return self.task_record.task_id
        except AttributeError:
            return None

    @cached_property
    def history(self):
        try:
            return self.task_record.reviews.all()
        except AttributeError:
            return TaskRecordReview.objects.none()

    @property
    def mentions(self):
        """
        Returns a list of unique mentions, with their corresponding User.
        """
        return list_mentions(self.note)


    def save(self, *args, **kwargs):
        if not self.choice is None:
            self.status = StatusType.DONE
        super().save(*args, **kwargs)


    def check_user_is_authorized(self, **kwargs):
        if not self.task_record.task.checkers.filter(pk=self.checker.pk).exists():
            raise ValidationError(f'{self.checker} is not a checker for the task "{self.task_record.task}"')


    def check_unique_constraints(self, **kwargs):
        for fields in self._meta.unique_together:
            opts = { field: getattr(self, field) for field in fields }
            if TaskRecordReview.objects.filter(**opts).exists():
                raise ValidationError(f'Task record #{self.task_record.id} was already attributed to {self.checker} before')


    def check_round_upper_bound(self, **kwarg):
        if self.task_record:
            max_round = self.task_record.task.rounds
            if self.task_record.reviews.count() >= max_round:
                raise ValidationError(f'Task record #{self.task_record.id} cannot get more than {max_round} reviews')

    @property
    def already_has_note(self):
        return self.note is not None and self.note_created_at is not None

    @property
    def note_changed(self):
        if self.pk is not None:
            instance = TaskRecordReview.objects.get(pk=self.pk)
            return self.note != instance.note
        return False


    @staticmethod
    def signal_notify_mentioned_users(sender, instance, **kwargs):
        for mention in instance.mentions:
            user = mention.get('user')
            if user is not None:
                action, created = get_or_create_mention_action(instance.checker, user, instance)
                if created:
                    UserNotification.objects.create(recipient=user, action=action)


    @staticmethod
    def signal_fill_note_created_at_and_updated_at(sender, instance, **kwargs):
        if instance.already_has_note and instance.note_changed:
            instance.note_updated_at = timezone.now()
        if instance.note and not instance.already_has_note:
            instance.note_created_at = timezone.now()


    @staticmethod
    def signal_notify_members_in_mentioned_project(sender, instance, **kwargs):
        project = instance.mentioned_project
        if project is not None:
            for user in project.members:
                if instance.checker != user:
                    action, created = get_or_create_mention_action(instance.checker, user, instance)
                    if created:
                        UserNotification.objects.create(recipient=user, action=action)

    @staticmethod
    def signal_notify_task_checkers_in_mentioned_task(sender, instance, **kwargs):
        task = instance.mentioned_task
        if task is not None:
            for user in task.checkers.all():
                if instance.checker != user:
                    action, created = get_or_create_mention_action(instance.checker, user, instance)
                    if created:
                        UserNotification.objects.create(recipient=user, action=action)


signals.post_save.connect(TaskRecordReview.signal_notify_task_checkers_in_mentioned_task, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_members_in_mentioned_project, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_mentioned_users, sender=TaskRecordReview)
signals.pre_save.connect(TaskRecordReview.signal_fill_note_created_at_and_updated_at, sender=TaskRecordReview)
# Send signals to the TaskRecord model
signals.post_save.connect(TaskRecord.signal_update_has_notes, sender=TaskRecordReview)
signals.post_save.connect(TaskRecord.signal_update_has_disagreements, sender=TaskRecordReview)
signals.post_save.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
signals.post_delete.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
