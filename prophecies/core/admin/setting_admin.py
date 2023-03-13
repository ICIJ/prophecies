from constance.admin import ConstanceAdmin, Config
from django.contrib import admin

from prophecies.core.forms import SettingForm


class SettingAdmin(ConstanceAdmin):
    change_list_form = SettingForm

    def get_config_value(self, name, options, form, initial):
        config_value = super().get_config_value(name, options, form, initial)
        config_value['visibility_field'] = form['%s_visibility' % name]
        return config_value


Config._meta.app_label = 'core'
Config._meta.object_name = 'Setting'
Config._meta.verbose_name_plural = 'Settings'
admin.site.unregister([Config])
admin.site.register([Config], SettingAdmin)
