from actstream import action
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from prophecies.core.models import Task


class ActionAggregateQuerySet(models.QuerySet):

    def user_scope(self, user):
        projects = self.filter(task__checkers=user).values('task__project')
        return self.filter(task__project__in=projects)


class ActionAggregateManager(models.Manager):

    def user_scope(self, user):
        return self.get_queryset().user_scope(user)

    def get_queryset(self) -> ActionAggregateQuerySet:
        return ActionAggregateQuerySet(model=self.model, using=self._db, hints=self._hints)


class ActionAggregate(models.Model):
    objects = ActionAggregateManager()

    verb = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=0)

    @staticmethod
    def signal_action_aggregate_creation(sender, instance, created, **kwargs):
        if instance.user and created:
            action.send(instance.user, verb='created-aggregate', target=instance)


signals.post_save.connect(ActionAggregate.signal_action_aggregate_creation, sender=ActionAggregate)
