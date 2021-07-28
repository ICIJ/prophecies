from constance.admin import ConstanceAdmin, Config
from django.contrib import admin

Config._meta.app_label = 'core'
Config._meta.object_name = 'Setting'
Config._meta.verbose_name_plural = 'Settings'
admin.site.unregister([Config])
admin.site.register([Config], ConstanceAdmin)
