from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from prophecies.core.models import Project, Task, TaskRecord
from prophecies.core.forms import TaskRecordUploadForm

class TaskRecordFormTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Pencil Papers')
        self.task = Task.objects.create(name='Art', project=self.project, color='#fe6565')


    def test_is_valid(self):
        data = { "task": self.task.id }
        files = { 'csv_file': self.build_csv_file('task,original_value') }
        form = TaskRecordUploadForm(data, files)
        self.assertTrue(form.is_valid())


    def test_missing_task_isnt_valid(self):
        data = { }
        files = { 'csv_file': self.build_csv_file('task,original_value') }
        form = TaskRecordUploadForm(data, files)
        self.assertFalse(form.is_valid())


    def test_missing_csv_file_isnt_valid(self):
        data = { "task": self.task.id }
        files = { }
        form = TaskRecordUploadForm(data, files)
        self.assertFalse(form.is_valid())


    def test_wrong_task_isnt_valid(self):
        data = { "task": -1 }
        files = { 'csv_file': self.build_csv_file('task,original_value') }
        form = TaskRecordUploadForm(data, files)
        self.assertFalse(form.is_valid())


    def test_wrong_csv_file_isnt_valid(self):
        data = { "task": self.task.id }
        files = { 'csv_file': self.build_csv_file('$ù*%,;') }
        form = TaskRecordUploadForm(data, files)
        self.assertFalse(form.is_valid())


    def test_unknown_columns_csv_file_isnt_valid(self):
        data = { "task": self.task.id }
        files = { 'csv_file': self.build_csv_file('$ù*%,;') }
        form = TaskRecordUploadForm(data, files)
        self.assertFalse(form.is_valid())


    def test_it_creates_two_task_records(self):
        data = { "task": self.task.id }
        csv_content = '\n'.join([
            'task,original_value',
            '%s,foo' % self.task.id,
            '%s,bar' % self.task.id,
        ])
        files = { 'csv_file': self.build_csv_file(csv_content) }
        form = TaskRecordUploadForm(data, files)
        form.full_clean()
        form.save()
        self.assertEqual(TaskRecord.objects.count(), 2)
        self.assertTrue(TaskRecord.objects.filter(original_value='foo').exists())
        self.assertTrue(TaskRecord.objects.filter(original_value='bar').exists())


    def test_it_update_two_task_records(self):
        TaskRecord.objects.create(uid='painting-1', original_value='blue', task=self.task)
        TaskRecord.objects.create(uid='painting-2', original_value='purple', task=self.task)
        data = { "task": self.task.id }
        csv_content = '\n'.join([
            'task,uid,original_value',
            '%s,painting-1,green' % self.task.id,
            '%s,painting-2,red' % self.task.id,
        ])
        files = { 'csv_file': self.build_csv_file(csv_content) }
        form = TaskRecordUploadForm(data, files)
        form.full_clean()
        form.save()
        self.assertEqual(TaskRecord.objects.count(), 2)
        self.assertTrue(TaskRecord.objects.filter(original_value='green').exists())
        self.assertTrue(TaskRecord.objects.filter(original_value='red').exists())


    def test_it_update_one_and_create_two_task_records(self):
        TaskRecord.objects.create(uid='painting-1', original_value='blue', task=self.task)
        data = { "task": self.task.id }
        csv_content = '\n'.join([
            'task,uid,original_value',
            '%s,painting-1,green' % self.task.id,
            '%s,painting-2,red' % self.task.id,
            '%s,painting-3,yellow' % self.task.id,
        ])
        files = { 'csv_file': self.build_csv_file(csv_content) }
        form = TaskRecordUploadForm(data, files)
        form.full_clean()
        form.save()
        self.assertEqual(TaskRecord.objects.count(), 3)
        self.assertTrue(TaskRecord.objects.filter(original_value='green').exists())
        self.assertTrue(TaskRecord.objects.filter(original_value='red').exists())
        self.assertTrue(TaskRecord.objects.filter(original_value='yellow').exists())


    def build_csv_file(self, content, filename='tmp.csv'):
        return SimpleUploadedFile(filename, bytes(content, 'utf-8'))
