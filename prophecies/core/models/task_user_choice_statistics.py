from django.contrib.auth.models import User
from django.db import models

from prophecies.core.models import Task, Choice


class TaskUserChoiceStatisticsQuerySet(models.QuerySet):

    def user_scope(self, user):
        return self.filter(task__in=user.task.all())


class TaskUserStatisticsManager(models.Manager):

    def user_scope(self, user):
        return self.get_queryset().user_scope(user)

    def get_queryset(self) -> TaskUserChoiceStatisticsQuerySet:
        return TaskUserChoiceStatisticsQuerySet(model=self.model, using=self._db, hints=self._hints)


class TaskUserChoiceStatistics(models.Model):
    objects = TaskUserStatisticsManager()
    task = models.ForeignKey(Task, null=False, blank=False, on_delete=models.CASCADE)
    checker = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    round = models.IntegerField(null=False, blank=False, help_text='Round number of the static entry')
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.task.name}\'s statistics for user {self.checker.name}'

    class Meta:
        unique_together = ('task_id', 'choice_id', 'round', 'checker')
