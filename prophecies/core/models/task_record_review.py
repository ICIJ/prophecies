from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, signals
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.choice import Choice
from prophecies.core.models.task_record import TaskRecord

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
    def history(self):
        return self.task_record.reviews.exclude(choice__isnull=True).all()


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



signals.post_save.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
signals.post_delete.connect(TaskRecord.signal_update_rounds_and_status, sender=TaskRecordReview)
