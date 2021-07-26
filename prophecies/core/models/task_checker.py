from django.contrib.auth.models import User
from django.db import models
from prophecies.core.models.task import Task


class TaskChecker(models.Model):
    checker = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.checker} is cheker on task #{self.task.id}'
