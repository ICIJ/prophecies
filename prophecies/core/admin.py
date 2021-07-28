from django import forms
from django.contrib import admin
from constance import config
from constance.admin import ConstanceAdmin, Config
from prophecies.core.models import Project
from prophecies.core.models import Choice
from prophecies.core.models import ChoiceGroup
from prophecies.core.models import Task


Config._meta.app_label = 'core'
Config._meta.object_name = 'Setting'
Config._meta.verbose_name_plural = 'Settings'
admin.site.unregister([Config])
admin.site.register([Config], ConstanceAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    exclude = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)



class ChoiceInline(admin.TabularInline):
    model = Choice
    fk_name = "choice_group"
    extra = 0


@admin.register(ChoiceGroup)
class ChoiceGroupAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline,]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
