from django.db import models
from prophecies.core.models.project import Project
from prophecies.core.models.task_choices_group import TaskChoicesGroup
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Task name")
    description = models.CharField(max_length=100, verbose_name="Task description")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project this task belong to")
    checkers = models.ManyToManyField(User, through='TaskChecker', through_fields=('task', 'checker'), verbose_name="User in charge of checking this task's data", related_name='task')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    rounds = models.PositiveIntegerField(default=3, verbose_name="Number of rounds")
    automatic_round_attributions = models.BooleanField(default=True, verbose_name="Attribute rounds (if not checked, all checkers will participate in all rounds)")
    allow_multiple_checks = models.BooleanField(default=True, verbose_name="Allow checkers to check several time the same item")
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    choices_group = models.ForeignKey(TaskChoicesGroup, verbose_name="Choices", on_delete=models.SET_NULL, null=True, blank=True)
    allow_items_addition = models.BooleanField(default=False, verbose_name="Allow checker to add items")

    def __str__(self):
        return self.name
