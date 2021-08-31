import re
import logging
from django.db import models
from django.contrib.auth.models import User
from prophecies.core.models import Project, Task

class Tip(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tip name", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def mentions(self):
        """
        Returns a list of unique mentions, with their corresponding User.
        """
        results = re.findall("@([a-zA-Z0-9]{1,15})", self.description)
        if len(results) > 1:
            results = list(dict.fromkeys(results))
        objects = []
        for result in results:
            class Mention:
                mention = result
                try:
                    user = User.objects.get(username=result)
                except User.DoesNotExist:
                    user = None
            mention = Mention()
            objects.append(mention)
        return objects
