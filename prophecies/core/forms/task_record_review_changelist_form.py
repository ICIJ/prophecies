from django import forms
from prophecies.core.models import TaskRecordReview


class TaskRecordReviewChangelistForm(forms.ModelForm):
    class Meta:
        model = TaskRecordReview
        fields = "__all__"