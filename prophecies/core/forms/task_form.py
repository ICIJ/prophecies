from django import forms
from django.core.exceptions import ValidationError
from prophecies.core.models import Task, TaskRecordReview

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice_group'].disabled = not self.can_change_choice_group

    def clean_choice_group(self):
        if not self.can_change_choice_group and self.choice_group_changed:
            raise ValidationError("You cannot change the choice group.")
        return self.cleaned_data.get('choice_group')

    @property
    def can_change_choice_group(self):
        if self.instance and self.instance.pk:
            return self.instance.choice_group is None or not self.has_reviews
        return True

    @property
    def choice_group_changed(self):
        return self.instance.choice_group != self.cleaned_data.get('choice_group')
        
    @property
    def has_reviews(self):
        return TaskRecordReview.objects.filter(task_record__task = self.instance).exists()