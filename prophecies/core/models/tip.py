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
