from django import forms
from django.contrib import admin
from constance import config
from constance.admin import ConstanceAdmin, Config
from prophecies.core.models import Project
from prophecies.core.models import TaskChoice
from prophecies.core.models import TaskChoicesGroup
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



class TaskChoiceInline(admin.TabularInline):
    model = TaskChoice
    fk_name = "choices_group"
    extra = 0


@admin.register(TaskChoicesGroup)
class TaskChoicesGroupAdmin(admin.ModelAdmin):
    inlines = [TaskChoiceInline,]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    exclude = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
