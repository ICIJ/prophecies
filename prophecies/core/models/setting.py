from prophecies.apps.api.contrib.strings import to_camel_case
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
        for (key, value) in self.env().items():
            # Remove the 'APP_' part from the key and convert to camel case
            key = to_camel_case(key[len(self.env_prefix):])
            # Avoid overriding existing keys
            if not self.key_exists(key):
                # Finally, add the setting to the list
                settings.append(Setting(key=key, value=value))
        return settings

    def key_exists(self, key):
        existing_keys = self.values_list('key', flat=True)
        return key in existing_keys

    def with_env(self):
        all_as_list = list(self.all())
        return all_as_list + self.from_env()


class Setting(Constance):
    objects = SettingManager()

    class Meta:
        proxy = True
