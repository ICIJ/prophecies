from django import forms
from prophecies.core.models import Task

class TaskRecordUploadForm(forms.Form):
    csv_file = forms.FileField()
    task = forms.ModelChoiceField(queryset=Task.objects.all())
