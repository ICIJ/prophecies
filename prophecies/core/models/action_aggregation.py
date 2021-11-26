from django.db import models


class ActionAggregation(models.Model):
    verb = models.CharField(max_length=100)
    actor_object_id = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        abstract = True