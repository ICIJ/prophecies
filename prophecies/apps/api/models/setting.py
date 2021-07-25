from ..contrib.strings import to_camel_case
from constance.backends.database.models import Constance
from django.conf import settings
from django.db import models
import os


class SettingManager(models.Manager):
    env_prefix = 'PROPHECIES_APP_'

    def env(self):
        items = os.environ.items()
        # Create a dict with only env variables that starts with 'PROPHECIES_'
        return dict(item for item in items if item[0].startswith(self.env_prefix))

    def from_env(self):
        settings = []
        # A dict of static settings targeting to be visible publicaly
        for (key, value) in Setting.objects.env().items():
            # Remove the 'APP_' part from the key and convert to camel case
            key = to_camel_case(key[len(self.env_prefix):])
            # Finally, add the setting to the list
            settings.append(Setting(key=key, value=value))
        return settings


    def with_env(self):
        all_as_list = list(Setting.objects.all())
        return all_as_list + Setting.objects.from_env()


class Setting(Constance):
    objects = SettingManager()

    class Meta:
        app_label = 'constance'
        proxy = True
