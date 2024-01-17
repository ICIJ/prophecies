from django import forms
from prophecies.core.models import TaskRecord


class TaskRecordChangelistForm(forms.ModelForm):
    class Meta:
        model = TaskRecord
        fields = '__all__'

    original_value = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'textarea-autogrow'}))
      