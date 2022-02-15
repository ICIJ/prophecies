from django.db import models
from django.contrib.auth.models import User
from prophecies.core.models import Task


class TaskUserStatisticsQuerySet(models.QuerySet):
    
    def user_scope(self, user):
        return self.filter(task__in=user.task.all())
    
    
class TaskUserStatisticsManager(models.Manager):
    
    def user_scope(self, user):
        return self.get_queryset().user_scope(user)
    
    def get_queryset(self) -> TaskUserStatisticsQuerySet:
        return TaskUserStatisticsQuerySet(model=self.model, using=self._db, hints=self._hints)
    

class TaskUserStatistics(models.Model):
    objects = TaskUserStatisticsManager()
    
    task = models.ForeignKey(Task, null=False, blank=False, on_delete=models.CASCADE)
    checker = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    round = models.IntegerField(null=False, blank=False, help_text='Round number of the static entry')
    done_count = models.IntegerField(default=0, help_text='Count of done records')
    pending_count = models.IntegerField(default=0, help_text='Count of pending records')

    def __str__(self):
        return f'{self.task.name}\'s statistics for user {self.checker.name}'

    class Meta:
        unique_together = ('task_id', 'checker_id', 'round')

    @property
    def progress(self):
        if self.total_count == 0:
            return 0
        return self.done_count / self.total_count * 100

    @property
    def total_count(self):
        return self.done_count + self.pending_count