from constance.admin import ConstanceAdmin, Config
from django.contrib import admin

from prophecies.core.forms import SettingForm


class SettingAdmin(ConstanceAdmin):
    change_list_form = SettingForm

    def get_config_value(self, name, options, form, initial):
        config_value = super().get_config_value(name, options, form, initial)
        config_value['visibility_field'] = form[f'{name}_visibility']
        return config_value

# pylint: disable=protected-access
Config._meta.app_label = 'core'
# pylint: disable=protected-access
Config._meta.object_name = 'Setting'
# pylint: disable=protected-access
Config._meta.verbose_name_plural = 'Settings'
admin.site.unregister([Config])
admin.site.register([Config], SettingAdmin)
