import os

from constance.backends.database.models import Constance
from django.db import models
from django.db.models import signals

from prophecies.apps.api.contrib.strings import to_camel_case


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

    def all_with_env(self):
        all_as_list = list(self.all())
        return all_as_list + self.from_env()

    def public(self):
        return self.filter(visibility__public=True)


class Setting(Constance):
    objects = SettingManager()

    class Meta:
        proxy = True

    @property
    def public(self):
        if hasattr(self, 'visibility'):
            return self.visibility.public
        return False

    @public.setter
    def public(self, value):
        self.visibility, created = SettingVisibility.objects.get_or_create(setting=self)
        self.visibility.public = value

    @property
    def private(self):
        return not self.public

    def publish(self):
        self.visibility, created = SettingVisibility.objects.get_or_create(setting=self)
        self.visibility.public = True
        self.visibility.save()

    def unpublish(self):
        self.visibility, created = SettingVisibility.objects.get_or_create(setting=self)
        self.visibility.public = False
        self.visibility.save()

    @staticmethod
    def signal_save_visibility(sender, instance, **kwargs):
        if hasattr(instance, 'visibility'):
            instance.visibility.save()


signals.post_save.connect(Setting.signal_save_visibility, sender=Setting)


class SettingVisibility(models.Model):
    setting = models.OneToOneField(Setting, on_delete=models.CASCADE, related_name='visibility')
    public = models.BooleanField(default=False, verbose_name='Make a setting public (visible without authentication)')
