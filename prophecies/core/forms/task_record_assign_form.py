from django import forms
from django.contrib.auth.models import User
from prophecies.core.models import Task, TaskRecord, TaskRecordReview


class TaskRecordAssignForm(forms.Form):
    task_records = forms.ModelMultipleChoiceField(required=True, queryset=TaskRecord.objects.all(),
                                                  widget=forms.MultipleHiddenInput())
    checker = forms.ModelChoiceField(required=True, queryset=User.objects.all())
    round = forms.IntegerField(required=False, min_value=1,
                               help_text="Leave empty to select the round automatically "
                                         "based on the latest record's attribution.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'task_records' in kwargs['initial']:
            task_ids = kwargs['initial']['task_records'].values_list('task_id', flat=True)
            tasks = Task.objects.filter(id__in=task_ids)
            self.fields['checker'].queryset = tasks.checkers()
            self.fields['round'] = forms.IntegerField(required=False, min_value=1,
                                                        max_value=tasks.min_round(),
                                                        help_text=self.fields['round'].help_text)

    def clean(self):
        super().clean()
        if self.is_valid():
            for object in self.task_record_reviews():
                object.check_user_is_authorized()
                ignored_fields = [] if object.task.allow_multiple_checks else ['round']
                object.check_unique_constraints(ignored_fields=ignored_fields)
                object.check_round_upper_bound()

    def task_record_reviews(self):
        checker = self.cleaned_data["checker"]
        round = self.cleaned_data["round"]
        task_records = self.cleaned_data["task_records"]
        objects = []
        for task_record in task_records:
            opts = dict(task_record=task_record, checker=checker, round=round)
            task_record_review = TaskRecordReview(**opts)
            objects.append(task_record_review)
        return objects

    def save(self, commit=True):
        self.full_clean()
        objects = self.task_record_reviews()
        if commit:
            for object in objects:
                object.save()
        return objects
