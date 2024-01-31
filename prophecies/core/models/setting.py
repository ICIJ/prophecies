import os

from constance.settings import CONFIG as CONSTANCE_CONFIG
from constance.backends.database.models import Constance
from django.db import models
from django.db.models import signals
from prophecies.apps.api.contrib.strings import to_camel_case


class SettingManager(models.Manager):
    env_prefix = "PROPHECIES_APP_"

    def env(self):
        items = os.environ.items()
        # Create a dict with only env variables that starts with 'PROPHECIES_'
        return dict(item for item in items if item[0].startswith(self.env_prefix))

    def from_env(self):
        settings = []
        # A dict of static settings targeting to be visible publicaly
        for key, value in self.env().items():
            # Remove the 'PROPHECIES_APP_' part from the key and convert to camel case
            key = to_camel_case(key[len(self.env_prefix) :])
            # Avoid overriding existing keys from the db
            if not self.key_exists(key):
                # Finally, add the setting to the list
                settings.append(Setting(key=key, value=value))
        return settings

    def from_config(self):
        settings = []
        # Add the constance config keys
        for key, (value, _) in CONSTANCE_CONFIG.items():
            # Avoid overriding existing keys from the db
            if not self.key_exists(key):
                settings.append(Setting(key=key, value=value))
        return settings

    def key_exists(self, key):
        existing_keys = self.values_list("key", flat=True)
        return key in existing_keys

    def all_with_env(self):
        all_as_list = list(self.all())
        settings = self.from_config() + self.from_env() + all_as_list
        return list({setting.key: setting for setting in settings}.values())

    def all_public_with_env(self):
        return [setting for setting in self.all_with_env() if setting.public]


class Setting(Constance):
    objects = SettingManager()

    class Meta:
        proxy = True

    @property
    def forced_public(self):
        from django.conf import settings

        return self.key in settings.CONSTANCE_PUBLIC_KEYS

    @property
    def public(self):
        is_forced_public = self.forced_public
        has_public_visibility = hasattr(self, "visibility") and self.visibility.public
        return is_forced_public or has_public_visibility

    @public.setter
    def public(self, value):
        if not self.forced_public:
            self.visibility, _created = SettingVisibility.objects.get_or_create(
                setting=self
            )
            self.visibility.public = value

    @property
    def private(self):
        return not self.public

    def publish(self):
        self.visibility, _created = SettingVisibility.objects.get_or_create(
            setting=self
        )
        self.visibility.public = True
        self.visibility.save()

    def unpublish(self):
        self.visibility, _created = SettingVisibility.objects.get_or_create(
            setting=self
        )
        self.visibility.public = False
        self.visibility.save()

    @staticmethod
    def signal_save_visibility(
        sender, instance, **kwargs
    ):  # pylint: disable=unused-argument
        if hasattr(instance, "visibility"):
            instance.visibility.save()


signals.post_save.connect(Setting.signal_save_visibility, sender=Setting)


class SettingVisibility(models.Model):
    setting = models.OneToOneField(
        Setting, on_delete=models.CASCADE, related_name="visibility"
    )
    public = models.BooleanField(
        default=False,
        verbose_name="Make a setting public (visible without authentication)",
    )
