from django import forms
from prophecies.core.models import Task, TaskRecord
from prophecies.core.forms import AbstractUploadForm


class TaskRecordUploadForm(AbstractUploadForm):
    csv_file = forms.FileField(required=True, label="CSV file")
    task = forms.ModelChoiceField(required=True, queryset=Task.objects.all())

    class Meta:
        model = TaskRecord
        csv_columns = ['original_value', 'predicted_value', 'uid', 'metadata']


    def row_to_task_record(self, task, row={}):
        opts = { 'task': task }
        # collect allowed model field
        for field_name in self._meta.csv_columns:
            opts[field_name] = row.get(field_name, None)
        return TaskRecord(**opts)


    def save(self, commit=True):
        self.full_clean()
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
        if commit:
            TaskRecord.objects.bulk_create(queues['bulk_create'])
            TaskRecord.objects.bulk_update(queues['bulk_update'], self._meta.csv_columns)
        return queues
