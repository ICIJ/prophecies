from django.contrib import admin
from prophecies.core.models import Choice, ChoiceGroup

class ChoiceInline(admin.TabularInline):
    model = Choice
    fk_name = "choice_group"
    extra = 1


@admin.register(ChoiceGroup)
class ChoiceGroupAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline,]
