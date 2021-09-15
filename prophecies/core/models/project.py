from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Project name")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name


    @property
    def members(self):
        try:
            return User.objects.filter(task__project=self).distinct().all()
        except AttributeError:
            return None
