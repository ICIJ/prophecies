from django.db import models
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.task import Task


class StatusType(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    ASSIGNED = 'ASSIGNED', _('Assigned')
    DONE = 'DONE', _('Done')


class TaskRecordManager(models.Manager):

    def get_by_uid(self, uid, task=None):
        if not uid:
            return None
        return self.filter(uid=uid, task=task).first()


    def pending(self):
        return self.filter(status=StatusType.PENDING)


    def assigned(self):
        return self.filter(status=StatusType.ASSIGNED)
        

    def done(self):
        return self.filter(status=StatusType.DONE)


class TaskRecord(models.Model):
    objects = TaskRecordManager()

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    # An optional unique identifier used to update task records in bulk
    uid = models.CharField(max_length=50, blank=True, null=True, verbose_name='UID')
    # Original value of the record
    original_value = models.TextField(blank=True, null=True)
    # Suggested value to be reviewed
    suggested_value = models.TextField(blank=True, null=True)
    # Optional metadata for this record (in JSON)
    metadata = models.JSONField(blank=True, null=True)
    # Status of the record. Set to done after it passes all task's rounds
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=8)
    # Number of rounds this record was submitted to
    rounds = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f'Record #{self.id} to be review in {self.task.name}'


    def computed_status(self):
        if self.attributions.count() == 0:
            return StatusType.PENDING
        elif self.attributions.done().count() >= self.task.rounds:
            return StatusType.DONE
        else:
            return StatusType.ASSIGNED

    def computed_rounds(self):
        return self.attributions.latest_round(self)


    @staticmethod
    def update_rounds_and_status(sender, instance=None, created=False, **kwargs):
        task_record = instance.task_record
        # Update the round for this record
        task_record.status = task_record.computed_status()
        task_record.rounds = task_record.computed_rounds()
        task_record.save(update_fields=['rounds', 'status'])
