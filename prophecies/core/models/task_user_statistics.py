from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property
from prophecies.core.models.task import Task


class TaskUserStatistics(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False, on_delete=models.CASCADE)
    checker = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    round = models.IntegerField(null=False, blank=False, help_text='Round number of the static entry')
    done_count = models.IntegerField(default=0, help_text='Count of done records')
    pending_count = models.IntegerField(default=0, help_text='Count of pending records')

    def __str__(self):
        return f'{self.task.name}\'s statistics for user {self.checker.name}'

    class Meta:
        unique_together = ('task_id', 'checker_id', 'round')

    @cached_property
    def progress(self):
        if self.done_count == 0:
            return 0
        return (self.done_count + self.pending_count) / self.done_count * 100
