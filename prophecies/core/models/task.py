from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from prophecies.core.models.project import Project
from prophecies.core.models.choice_group import ChoiceGroup
from prophecies.core.contrib.colors import hex_scale_brightness


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", help_text="Project this task belong to")
    checkers = models.ManyToManyField(User, through='TaskChecker', through_fields=('task', 'checker'), verbose_name="User in charge of checking this task's data", related_name='task')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    rounds = models.PositiveIntegerField(default=3, verbose_name="Number of rounds")
    automatic_round_attributions = models.BooleanField(default=True, verbose_name="Attribute rounds (if not checked, all checkers will participate in all rounds)")
    allow_multiple_checks = models.BooleanField(default=True, verbose_name="Allow checkers to check several time the same item")
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    choice_group = models.ForeignKey(ChoiceGroup, verbose_name="Choices", on_delete=models.SET_NULL, null=True, blank=True)
    allow_items_addition = models.BooleanField(default=False, verbose_name="Allow checker to add items")
    color = ColorField(default='#31807D')
    recordLinkTemplate = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Record link template", help_text="A link template to build a link for each task record. Task record can override this value with their own link")


    def __str__(self):
        return self.name


    @property
    def colors(self):
        """
        Generate 3 colors tones based on the `color` attribute
        """
        scales = [0.75, 1.0, 1.25]
        return tuple(hex_scale_brightness(self.color, s) for s in scales)
