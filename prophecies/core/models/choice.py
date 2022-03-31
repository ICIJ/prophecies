from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from prophecies.core.models.choice_group import ChoiceGroup


class Choice(models.Model):
    COLOR_PALETTE = [
        ('#73B782', 'Correct',),
        ('#FE6565', 'Incorrect', ),
        ('#FFE980','Warning',),
        ('#BEBFBF','Don\'t know',),
    ]
    color = ColorField(samples=COLOR_PALETTE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, blank=True)
    shortkeys = models.CharField(max_length=100, null=True, blank=True, help_text='Comma separated list of shortkeys to pick this choice')
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE, related_name='choices')
    require_alternative_value = models.BooleanField(default=False, verbose_name='Requires an alternative value?')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.name
        super().save(*args, **kwargs)
