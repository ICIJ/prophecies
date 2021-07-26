from django.db import models


class TaskChoicesGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        choices = self.choices.values_list('name', flat=True)
        if len(choices):
            joined_choices = ' | '.join(choices)
            return f'{self.name} ({joined_choices})'
        return self.name
