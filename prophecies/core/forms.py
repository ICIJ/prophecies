import csv
import io

from django import forms
from django.core.exceptions import ValidationError
from functools import lru_cache
from prophecies.core.models import Task
from prophecies.core.models import TaskRecord

class TaskRecordUploadForm(forms.Form):
    csv_file = forms.FileField(required=True, label="CSV file")
    task = forms.ModelChoiceField(required=True, queryset=Task.objects.all())

    ALLOWED_MODEL_FIELDS = ['original_value', 'suggested_value', 'uid', 'metadata']


    def csv_valid_fieldnames(self):
        return [ f.name for f in TaskRecord._meta.get_fields() ]


    def clean_csv_file(self):
        csv_fieldnames = self.csv_file_reader().fieldnames or []
        for fieldname in csv_fieldnames:
            if fieldname not in self.csv_valid_fieldnames():
                raise ValidationError('Your CSV contains a column "%s" which is not a valid' % fieldname)
        return self.cleaned_data['csv_file']


    def row_to_task_record(self, task, row={}):
        opts = { 'task': task }
        # collect allowed model field
        for field_name in TaskRecordUploadForm.ALLOWED_MODEL_FIELDS:
            opts[field_name] = row.get(field_name, None)
        return TaskRecord(**opts)


    @lru_cache(maxsize=None)
    def csv_file_reader(self):
        csv_file = self.cleaned_data["csv_file"]
        stream = io.StringIO(csv_file.read().decode("UTF8"), newline=None)
        return csv.DictReader(stream)


    def save(self):
        task = self.cleaned_data["task"]
        # This list will contain all records to be created
        queues = { 'bulk_update': [], 'bulk_create': [] }
        # This list will contain all records to be update
        existing_task_records = []
        # Iterate over all CSV line
        for row in self.csv_file_reader():
            # Convert the row to a task record
            task_record = self.row_to_task_record(task=task, row=row)
            existing_task_record = TaskRecord.objects.get_by_uid(uid=row.get('uid'), task=task)
            # The task record already exists!
            if existing_task_record:
                task_record.id = existing_task_record.id
                queues['bulk_update'].append(task_record)
            else:
                queues['bulk_create'].append(task_record)
        # And finally, create and update all the task record at once)
        TaskRecord.objects.bulk_create(queues['bulk_create'])
        TaskRecord.objects.bulk_update(queues['bulk_update'], TaskRecordUploadForm.ALLOWED_MODEL_FIELDS)
