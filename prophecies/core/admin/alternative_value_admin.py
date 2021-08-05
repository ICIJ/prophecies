from django.contrib import admin
from prophecies.core.models import AlternativeValue


@admin.register(AlternativeValue)
class AlternativeValueAdmin(admin.ModelAdmin):
    pass
