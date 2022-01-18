from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, F, signals
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from prophecies.core.models import Choice, TaskRecord, UserNotification, TaskUserStatistics
from prophecies.core.contrib.mentions import list_mentions, get_or_create_mention_action, mentioned, notify_mentioned_users

class StatusType(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    DONE = 'DONE', _('Done')


class TaskRecordReviewQuerySet(models.QuerySet):

    def count_by_task(self, task_field='task', count_field='count'):
        count = Count('pk', distinct=True)
        annotate = { task_field: F('task_record__task_id'), count_field: count }
        return self.exclude(task_record=None) \
            .values('task_record__task_id') \
            .annotate(**annotate) \
            .values(task_field, count_field) \
            .order_by()
            
    def count_by_choice(self, choice_field='choice', count_field='count'):
        count = Count('pk', distinct=True)
        annotate = { choice_field: F('choice_id'), count_field: count }
        return self \
            .values('choice_id') \
            .annotate(**annotate) \
            .values(choice_field, count_field) \
            .order_by()
            

class TaskRecordReviewManager(models.Manager):

    def get_queryset(self) -> TaskRecordReviewQuerySet:
        return TaskRecordReviewQuerySet(model=self.model,
            using=self._db, hints=self._hints)

    def from_checker_task(self, user):
        return self.filter(task_record__task__in=user.task.all())


    def latest_round(self, task_record):
        if self.filter(task_record=task_record).exists():
            latest = self.filter(task_record=task_record).latest('round')
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
    
    def pending_by_round(self, **filter):
        buckets = self.pending() \
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
        unique_together = ('task_record_id', 'checker_id', 'round')
        index_together = [
            ('checker_id', 'round'),
            ('checker_id', 'round', 'status'),
        ]
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
        if self.task_record and self.checker:
            if self.choice:
                return f'Record #{self.task_record.id} reviewed by {self.checker}'
            return f'Record #{self.task_record.id} pending review by {self.checker}'            
        return super().__str__()



    @property
    def project(self):
        try:
            return self.task_record.task.project
        except AttributeError:
            return None


    @property
    def task(self):
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
        if not self.choice is None :
            self.status = StatusType.DONE
        elif self.choice_cancelled : # on cancel the status goes from DONE to PENDING
            self.status = StatusType.PENDING
        super().save(*args, **kwargs)


    def check_user_is_authorized(self, **kwargs):
        if not self.task_record.task.checkers.filter(pk=self.checker.pk).exists():
            raise ValidationError(f'{self.checker} is not a checker for the task "{self.task_record.task}"')


    def check_unique_constraints(self, ignored_fields=[], **kwargs):
        for fields in self._meta.unique_together:
            # Remove ignored field
            fields = [field for field in fields if field not in ignored_fields]
            # Collect values for the field that must be unique together
            opts = { field: getattr(self, field) for field in fields }
            if TaskRecordReview.objects.filter(**opts).exists():
                raise ValidationError(f'Task record #{self.task_record.id} was already attributed to {self.checker} before')


    def check_round_upper_bound(self, **kwarg):
        if self.task_record:
            max_round = self.task_record.task.rounds
            if self.task_record.reviews.count() >= max_round:
                raise ValidationError(f'Task record #{self.task_record.id} cannot get more than {max_round} reviews')
    
    @property
    def choice_cancelled(self):
        if self.pk is not None:
            instance = TaskRecordReview.objects.get(pk=self.pk)
            had_choice = instance.choice is not None
            has_no_choice = self.choice is None
            return had_choice and has_no_choice
        return False

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


    @property
    def mentioned_project(self):
        if mentioned(self.note, 'project'):
            return self.project


    @property
    def mentioned_task(self):
        if mentioned(self.note, 'task'):
            return self.task


    @staticmethod
    def signal_notify_members_in_mentioned_project(sender, instance, **kwargs):
        project = instance.mentioned_project
        if project is not None:
            notify_mentioned_users(instance.checker, project.members, instance)


    @staticmethod
    def signal_notify_task_checkers_in_mentioned_task(sender, instance, **kwargs):
        task = instance.mentioned_task
        if task is not None:
            notify_mentioned_users(instance.checker, task.checkers.all(), instance)

    @staticmethod
    def signal_save_task_user_statistics(sender, instance, **kwargs) :
        # Find or create the relevant TaskUserStatistics
        task = instance.task
        checker = instance.checker
        round = instance.round
        # Avoid collecting statistics for uncomplete review
        if task and checker:
            stats, _ = TaskUserStatistics.objects.get_or_create(task=task, checker=checker, round=round)
            # Collect the statitics
            task_round_reviews = sender.objects.filter(task_record__task=task, checker=checker, round=round)
            done_count = task_round_reviews.filter(status=StatusType.DONE).count()
            pending_count = task_round_reviews.filter(status=StatusType.PENDING).count()
            # Save the statistics
            stats.done_count = done_count
            stats.pending_count = pending_count
            stats.save()


signals.post_save.connect(TaskRecordReview.signal_save_task_user_statistics, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_members_in_mentioned_project, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_task_checkers_in_mentioned_task, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_members_in_mentioned_project, sender=TaskRecordReview)
signals.post_save.connect(TaskRecordReview.signal_notify_mentioned_users, sender=TaskRecordReview)
signals.pre_save.connect(TaskRecordReview.signal_fill_note_created_at_and_updated_at, sender=TaskRecordReview)
# Send signals to the TaskRecord model
signals.post_save.connect(TaskRecord.signal_update_has_notes, sender=TaskRecordReview)
signals.post_save.connect(TaskRecord.signal_update_has_disagreements, sender=TaskRecordReview)
signals.post_save.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
signals.post_delete.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
