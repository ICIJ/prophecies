from copy import deepcopy
from django.db import models
from django.utils.translation import gettext_lazy as _
from types import SimpleNamespace
from prophecies.core.contrib.namespace import ExtendedNamespace
from prophecies.core.contrib.formatter import URLEncodedFormatter
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
    uid = models.CharField(max_length=50, blank=True, null=True, verbose_name='UID', help_text="An optional unique identifier used to update task records in bulk")
    original_value = models.TextField(blank=True, null=True, help_text="Original value of the record")
    suggested_value = models.TextField(blank=True, null=True, help_text="Suggested value to be reviewed")
    metadata = models.JSONField(blank=True, null=True, help_text="Optional metadata for this record (in JSON)")
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=8, help_text="Status of the record. Set to done after it passes all task's rounds")
    rounds = models.PositiveIntegerField(default=0, help_text="Number of rounds this record was submitted to")
    link = models.CharField(max_length=1000, null=True, blank=True, help_text="An optional link to the record")


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


    def computed_link(self):
        if self.link:
            return self.link
        elif self.task.recordLinkTemplate:
            opts = deepcopy(self.__dict__)
            # Convert metadata field into namespace to use dot notation
            if type(opts['metadata']) == dict or type(opts['metadata']) == list:
                opts['metadata'] = ExtendedNamespace(opts.get('metadata', {}))
            formatter = URLEncodedFormatter()
            return formatter.format(self.task.recordLinkTemplate, **opts)


    @staticmethod
    def update_rounds_and_status(sender, instance=None, created=False, **kwargs):
        task_record = instance.task_record
        # Update the round for this record
        task_record.status = task_record.computed_status()
        task_record.rounds = task_record.computed_rounds()
        task_record.save(update_fields=['rounds', 'status'])
