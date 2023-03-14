from django.db import models
from prophecies.core.models.choice_group import ChoiceGroup


class AlternativeValue(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, blank=True)
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE, related_name='alternative_values')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.name
        super().save(*args, **kwargs)
