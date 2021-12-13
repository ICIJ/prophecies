from django.db import models
from django.contrib.auth.models import User

class ActionAggregation(models.Model):
    verb = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=0)