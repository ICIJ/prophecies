from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.choice import Choice
from prophecies.core.models.task_record import TaskRecord


class TaskRecordAttribution(models.Model):

    class StatusType(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        DONE = 'DONE', _('Done')

    task_record = models.ForeignKey(TaskRecord, null=True, on_delete=models.SET_NULL)
    checker = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    round = models.PositiveIntegerField(verbose_name="Attribution round")
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=7)
    choice = models.ForeignKey(Choice, null=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=100, blank=True, verbose_name="Checker note")
    alternative_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.checker} must check task record #{self.task_record.id} on round #{self.round}'

    class Meta:
        unique_together = ('task_record_id', 'checker_id', 'round')
