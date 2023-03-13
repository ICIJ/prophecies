from django import forms

from prophecies.core.forms import AbstractUploadForm
from prophecies.core.models import ChoiceGroup, AlternativeValue


class AlternativeValueUploadForm(AbstractUploadForm):
    csv_file = forms.FileField(required=True, label="CSV file")
    choice_group = forms.ModelChoiceField(required=True, queryset=ChoiceGroup.objects.all())

    class Meta:
        model = AlternativeValue
        csv_columns = ['name', 'value']

    def row_to_alternative_value(self, choice_group, row={}):
        opts = {'choice_group': choice_group}
        # collect allowed model field
        for field_name in self.get_csv_columns():
            opts[field_name] = row.get(field_name, None)
        return AlternativeValue(**opts)

    def save(self, commit=True):
        self.full_clean()
        choice_group = self.cleaned_data["choice_group"]
        # This list will contain all records to be created
        queue = []
        # Iterate over all CSV line
        for row in self.csv_file_reader():
            # Convert the row to a alternative value
            alternative_value = self.row_to_alternative_value(choice_group=choice_group, row=row)
            queue.append(alternative_value)
        # And finally, create all the alternative values at once
        if commit:
            AlternativeValue.objects.bulk_create(queue)
        return queue
