from copy import deepcopy
from actstream.models import Action
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from prophecies.core.contrib.namespace import ExtendedNamespace
from prophecies.core.contrib.formatter import URLEncodedFormatter
from prophecies.core.models.task import Task


class StatusType(models.TextChoices):
    UNASSIGNED = 'UNASSIGNED', _('Unassigned')
    ASSIGNED = 'ASSIGNED', _('Assigned')
    DONE = 'DONE', _('Done')


class TaskRecordManager(models.Manager):

    def get_by_uid(self, uid, task=None):
        if not uid:
            return None
        return self.filter(uid=uid, task=task).first()

    def unassigned(self):
        return self.filter(status=StatusType.UNASSIGNED)

    def assigned(self):
        return self.filter(status=StatusType.ASSIGNED)

    def done(self):
        return self.filter(status=StatusType.DONE)


class TaskRecord(models.Model):
    objects = TaskRecordManager()

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='records')
    uid = models.CharField(max_length=100, blank=True, null=True, verbose_name='UID',
                           help_text="An optional unique identifier used to update task records in bulk")
    original_value = models.TextField(blank=True, null=True, help_text="Original value of the record")
    predicted_value = models.TextField(blank=True, null=True, help_text="Suggested value to be reviewed")
    metadata = models.JSONField(blank=True, null=True, help_text="Optional metadata for this record (in JSON)")
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.UNASSIGNED, max_length=10,
                              help_text="Status of the record. Set to done after it passes all task's rounds")
    rounds = models.PositiveIntegerField(default=0, help_text="Number of rounds this record was submitted to")
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    link = models.CharField(max_length=1000, null=True, blank=True, help_text="An optional link to the record")
    embeddable_link = models.CharField(max_length=1000, null=True, blank=True,
                                       help_text="An optional alternative link to preview the record in an iframe")
    locked = models.BooleanField(default=False, help_text="A user locked this task record")
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                  help_text="User who locked this task record", related_name="locked_task_records")
    has_notes = models.BooleanField(default=False, help_text="One or more reviews have notes")
    has_disagreements = models.BooleanField(default=False, help_text="Reviews are different")
    bookmarked_by = models.ManyToManyField(User, help_text="Users who bookmarked this task record",
                                           related_name='bookmarked_task_records', blank=True)

    def __str__(self):
        return f'Record #{self.id} to be review in {self.task.name}'

    @cached_property
    def checkers_list(self):
        checkers = [review.checker for review in self.reviews.all()]
        return  list(filter(None, checkers))

    @cached_property
    def checkers_pretty(self):
        # Extract only the usernames
        usernames = [checker.username for checker in self.checkers_list]
        count = len(usernames)
        # Use the correct format depending on the count or use `many`
        return {0: lambda u: 'nobody', 1: lambda u: u[0], 2: lambda u: ' and '.join(u), }.\
            get(count, lambda u: ', '.join(u[0:-2]) + ', ' + ' and '.join(u[-2:]))(usernames) # pylint: disable=unnecessary-lambda

    @cached_property
    def reviews_actions_query(self):
        ctype = ContentType.objects.get_for_model(self.reviews.model)
        review_ids = list(self.reviews.values_list('id', flat=True))
        query = Q()
        for id in review_ids:
            query |= Q(target_content_type=ctype, target_object_id=id)
            query |= Q(action_object_content_type=ctype, action_object_object_id=id)
        return query

    @cached_property
    def actions_query(self):
        ctype = ContentType.objects.get_for_model(self)
        id = self.pk
        return Q(
            Q(target_content_type=ctype, target_object_id=id) |
            Q(action_object_content_type=ctype, action_object_object_id=id)
        )

    @cached_property
    def actions(self):
        return Action.objects.public(self.actions_query | self.reviews_actions_query)

    def can_lock(self, user):
        checkers_ids = [checker.id for checker in self.checkers_list]
        return not self.locked and user.id in checkers_ids

    def can_unlock(self, user):
        return self.locked and user.id is self.locked_by.id

    def computed_status(self):
        if self.reviews.count() == 0:
            return StatusType.UNASSIGNED
        if self.reviews.done().count() >= self.task.rounds:
            return StatusType.DONE
        return StatusType.ASSIGNED

    def computed_rounds(self):
        return self.reviews.latest_round(self)

    def computed_link(self):
        if self.link:
            return self.link
        if self.task.record_link_template:
            return self.format_link_template(self.task.record_link_template)
        return None

    def computed_embeddable_link(self):
        if self.embeddable_link:
            return self.embeddable_link
        if self.task.embeddable_record_link_template:
            return self.format_link_template(self.task.embeddable_record_link_template)
        return self.computed_link()

    def format_link_template(self, link_template):
        opts = deepcopy(self.__dict__)
        # Convert metadata field into ExtendedNamespace to use dot notation
        if isinstance(opts['metadata'], (dict, list)):
            opts['metadata'] = ExtendedNamespace(opts.get('metadata', {}))
        formatter = URLEncodedFormatter()
        return formatter.format(link_template, **opts)

    def update_rounds_and_status(self):
        self.status = self.computed_status()
        self.rounds = self.computed_rounds()
        self.save(update_fields=['rounds', 'status'])

    @staticmethod
    def signal_update_rounds_and_status(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        if instance.task_record:
            # Call the instance method
            instance.task_record.update_rounds_and_status()

    @staticmethod
    def signal_delete_review(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        if instance.task_record:
            # Call the instance method
            instance.task_record.reviews.remove(instance)
            instance.task_record.update_rounds_and_status()

    @staticmethod
    def signal_update_all_rounds_and_status(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        for task_record in TaskRecord.objects.all():
            task_record.update_rounds_and_status()

    @staticmethod
    def signal_update_has_notes(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        if instance.task_record:
            notes = [review.note for review in instance.task_record.reviews.all()]
            instance.task_record.has_notes = any(notes)
            instance.task_record.save(update_fields=['has_notes'])

    @staticmethod
    def signal_update_has_disagreements(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        if instance.task_record:
            choices = [review.choice_id for review in instance.task_record.reviews.all() if review.choice_id]
            choices = list(set(choices))
            instance.task_record.has_disagreements = len(choices) > 1
            instance.task_record.save(update_fields=['has_disagreements'])

# Disabled temporarly
# signals.post_save.connect(TaskRecord.signal_update_all_rounds_and_status, sender=Task)
