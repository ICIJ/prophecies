import csv
import io

from django import forms
from django.db.models import Model
from django.core.exceptions import ValidationError
from functools import lru_cache


class AbstractUploadForm(forms.Form):
    csv_file = forms.FileField(required=True, label="CSV file")

    class Meta:
        model = Model
        csv_columns = []


    def __init__(self, *args, **kwargs):
        super().__init__ (*args, **kwargs)
        self._meta = self.Meta()


    def get_model(self):
        return self._meta.model


    def get_csv_columns(self):
        return self._meta.csv_columns


    def get_model_fields(self):
        return self.get_model()._meta.get_fields()


    def csv_valid_fieldnames(self):
        return [ f.name for f in self.get_model_fields() ]


    def clean_csv_file(self):
        csv_fieldnames = self.csv_file_reader().fieldnames or []
        for fieldname in csv_fieldnames:
            if fieldname not in self.csv_valid_fieldnames():
                raise ValidationError('Your CSV contains a column "%s" which is not a valid' % fieldname)
        return self.cleaned_data['csv_file']


    @lru_cache(maxsize=None)
    def csv_file_reader(self):
        csv_file = self.cleaned_data["csv_file"]
        stream = io.StringIO(csv_file.read().decode("UTF8"), newline=None)
        return csv.DictReader(stream)


    def save(self, commit=True):
        raise NotImplementedError('You must implement a `save` method')
