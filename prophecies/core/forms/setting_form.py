from constance import settings
from constance.admin import ConstanceForm
from django import forms

from prophecies.core.models import Setting


class SettingForm(ConstanceForm):
    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, initial, request=None, *args, **kwargs):
        super().__init__(initial=initial, request=request, *args, **kwargs)
        # One boolean field is created for each setting
        for name in settings.CONFIG:
            field_name = SettingForm.visibility_field_name(name)
            self.fields[field_name] = forms.BooleanField(required=False)
            try:
                self.fields[field_name].initial = Setting.objects.get(key=name).public
            except Setting.DoesNotExist:
                self.fields[field_name].initial = False

    @staticmethod
    def visibility_field_name(name):
        return f'{name}_visibility'

    def save(self):
        for name in settings.CONFIG:
            setting, _created = Setting.objects.get_or_create(key=name)
            setting.public = self.cleaned_data.get(SettingForm.visibility_field_name(name), False)
            setting.save()
        super().save()
