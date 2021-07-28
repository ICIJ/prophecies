from django.db import models
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.task import Task


class TaskRecord(models.Model):

    class StatusType(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ASSIGNED = 'ASSIGNED', _('Assigned')
        DONE = 'DONE', _('Done')

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    # Original value of the record
    orginal_value = models.TextField()
    # Suggested value to be reviewed
    suggested_value = models.TextField()
    # Optional metadata for this record (in JSON)
    metadata = models.JSONField(null=True)
    # Status of the record. Set to done after it passes all task's rounds
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=8)
    # Number of rounds this record was submitted to
    rounds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Record #{self.id} for task #{self.task.id}'
