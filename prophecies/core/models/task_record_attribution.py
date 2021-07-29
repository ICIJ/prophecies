from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.choice import Choice
from prophecies.core.models.task_record import TaskRecord


class TaskRecordAttributionManager(models.Manager):

    def latest_round(self, task_record):
        if self.filter(task_record=task_record).exists():
            latest = self.filter(task_record=task_record).latest()
            return latest.round
        return 0


class TaskRecordAttribution(models.Model):
    objects = TaskRecordAttributionManager()

    class StatusType(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        DONE = 'DONE', _('Done')


    class Meta:
        unique_together = ('task_record_id', 'checker_id')
        get_latest_by = 'round'


    task_record = models.ForeignKey(TaskRecord, null=True, on_delete=models.SET_NULL)
    checker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    round = models.PositiveIntegerField(verbose_name="Attribution round", null=True, default=None)
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=7)
    choice = models.ForeignKey(Choice, null=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=100, blank=True, verbose_name="Checker note")
    alternative_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.round is None:
            self.round = TaskRecordAttribution.objects.latest_round(self.task_record) + 1


    def __str__(self):
        return f'Task record #{self.task_record.id} on round {self.round}'


    def validate_unique(self):
        for fields in self._meta.unique_together:
            opts = { field: getattr(self, field)  for field in fields }
            if TaskRecordAttribution.objects.filter(**opts).exists():
                raise ValidationError(f'Task record #{self.task_record.id} was already attributed to {self.checker} before')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the round for this record
        self.task_record.rounds = self.round
        self.task_record.save()
