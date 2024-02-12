from django import forms
from django.contrib.auth.models import User
from prophecies.core.models import TaskRecordReview


class TaskRecordReviewChangelistForm(forms.ModelForm):
    checker = forms.ModelChoiceField(required=False, queryset=User.objects.none())

    class Meta:
        model = TaskRecordReview
        fields = "__all__"

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        if instance and instance.task:
            self.fields["checker"].queryset = instance.task.checkers.all()
