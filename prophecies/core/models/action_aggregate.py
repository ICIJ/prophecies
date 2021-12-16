from django.db import models
from django.contrib.auth.models import User
from prophecies.core.models import Task

class ActionAggregate(models.Model):
    verb = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=0)