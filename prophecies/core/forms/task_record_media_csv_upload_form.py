from django import forms
from prophecies.core.models import Task, TaskRecord, TaskRecordMedia
from prophecies.core.forms import AbstractUploadForm


class TaskRecordMediaCSVUploadForm(AbstractUploadForm):
    csv_file = forms.FileField(required=True, label="CSV file")
    task = forms.ModelChoiceField(required=True, queryset=Task.objects.all())

    class Meta:
        model = TaskRecordMedia
        csv_columns = [
            "task_record",
            "uid",
            "file",
            "mime_type",
            "height",
            "width",
            ]

    def row_to_task_record_media(self, task, task_record, row=None):
        row = {} if row is None else row
        # tr_obj = TaskRecord.objects.get(id=task_record)
        opts = {"task": task, "task_record": task_record}
        # collect allowed model field
        for field_name in self._meta.csv_columns:
            if field_name.endswith('_id') or field_name == 'task_record':
                continue
            opts[field_name] = row.get(field_name, None)
        return TaskRecordMedia(**opts)

    def save(self, commit=True):
        self.full_clean()
        task = self.cleaned_data["task"]
        # This list will contain all records to be created
        queues = {"bulk_update": [], "bulk_create": []}
        # This list will contain all records to be update
        # Iterate over all CSV line
        for row in self.csv_file_reader():
            # Convert the row to a task record
            task_record = TaskRecord.objects.get(
                id=row["task_record"]
            )
            task_record_media = self.row_to_task_record_media(task=task,
                                                              task_record=task_record,
                                                              row=row)
            existing_task_record_media = TaskRecordMedia.objects.get_by_uid(
                uid=row.get("uid"), task_record=task_record
            )
            # The task record already exists!
            if existing_task_record_media:
                task_record_media.id = existing_task_record_media.id
                queues["bulk_update"].append(task_record_media)
            else:
                queues["bulk_create"].append(task_record_media)
        # And finally, create and update all the task record at once)
        if commit:
            TaskRecordMedia.objects.bulk_create(queues["bulk_create"])
            TaskRecordMedia.objects.bulk_update(
                queues["bulk_update"], self._meta.csv_columns
            )
        return queues
