from copy import deepcopy
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
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

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_records')
    uid = models.CharField(max_length=50, blank=True, null=True, verbose_name='UID', help_text="An optional unique identifier used to update task records in bulk")
    original_value = models.TextField(blank=True, null=True, help_text="Original value of the record")
    predicted_value = models.TextField(blank=True, null=True, help_text="Suggested value to be reviewed")
    metadata = models.JSONField(blank=True, null=True, help_text="Optional metadata for this record (in JSON)")
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.PENDING, max_length=8, help_text="Status of the record. Set to done after it passes all task's rounds")
    rounds = models.PositiveIntegerField(default=0, help_text="Number of rounds this record was submitted to")
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    link = models.CharField(max_length=1000, null=True, blank=True, help_text="An optional link to the record")
    locked = models.BooleanField(default=False, help_text="A user locked this task record")
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, help_text="User who locked this task record", related_name="locked_task_records")
    has_notes = models.BooleanField(default=False, help_text="One or more reviews have notes")
    has_disagreements = models.BooleanField(default=False, help_text="Reviews are different")

    def __str__(self):
        return f'Record #{self.id} to be review in {self.task.name}'


    def computed_status(self):
        if self.reviews.count() == 0:
            return StatusType.PENDING
        elif self.reviews.done().count() >= self.task.rounds:
            return StatusType.DONE
        else:
            return StatusType.ASSIGNED

    def computed_rounds(self):
        return self.reviews.latest_round(self)


    def computed_link(self):
        if self.link:
            return self.link
        elif self.task.recordLinkTemplate:
            opts = deepcopy(self.__dict__)
            # Convert metadata field into ExtendedNamespace to use dot notation
            if type(opts['metadata']) == dict or type(opts['metadata']) == list:
                opts['metadata'] = ExtendedNamespace(opts.get('metadata', {}))
            formatter = URLEncodedFormatter()
            return formatter.format(self.task.recordLinkTemplate, **opts)


    def update_rounds_and_status(self):
        self.status = self.computed_status()
        self.rounds = self.computed_rounds()
        self.save(update_fields=['rounds', 'status'])


    @staticmethod
    def signal_update_rounds_and_status(sender, instance=None, created=False, **kwargs):
        if instance.task_record:
            # Call the instance method
            instance.task_record.update_rounds_and_status()


    @staticmethod
    def signal_update_all_rounds_and_status(sender, instance=None, created=False, **kwargs):
        for task_record in TaskRecord.objects.all():
            task_record.update_rounds_and_status()

    @staticmethod
    def signal_update_has_notes(sender, instance=None, created=False, **kwargs):
        if instance.task_record:
            notes = [review.note for review in instance.task_record.reviews.all()]
            instance.task_record.has_notes = any(notes)
            instance.task_record.save(update_fields=['has_notes'])

    @staticmethod
    def signal_update_has_disagreements(sender, instance=None, created=False, **kwargs):
        if instance.task_record:
            choices = [review.choice_id for review in instance.task_record.reviews.all() if review.choice_id]
            choices = list(set(choices))
            instance.task_record.has_disagreements = len(choices) > 1
            instance.task_record.save(update_fields=['has_disagreements'])

# Disabled temporarly
# signals.post_save.connect(TaskRecord.signal_update_all_rounds_and_status, sender=Task)
