from django.contrib import admin
from prophecies.core.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    exclude = ['creator']


    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
