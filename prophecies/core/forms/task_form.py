from django import forms
from django.core.exceptions import ValidationError
from prophecies.core.models import Task, TaskRecordReview

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    def clean_choice_group(self):
        if not self.can_change_choice_group:
            raise ValidationError("You cannot change the choice group.")
        return self.cleaned_data.get('choice_group')

    @property
    def can_change_choice_group(self):
        return self.instance.choice_group is None or not self.choice_group_changed or not self.has_reviews

    @property
    def choice_group_changed(self):
        return self.instance.choice_group != self.cleaned_data.get('choice_group')
        
    @property
    def has_reviews(self):
        return TaskRecordReview.objects.filter(task_record__task = self.instance).exists()