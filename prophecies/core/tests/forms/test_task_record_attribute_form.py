from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Project, Task, TaskRecord, TaskRecordAttribution
from prophecies.core.forms import TaskRecordAttributeForm

class TaskRecordAttributeFormTests(TestCase):
    def setUp(self):
        self.olivia = User.objects.create(username='olivia')
        self.pierre = User.objects.create(username='pierre')
        self.project = Project.objects.create(name='Pencil Papers')
        self.task = Task.objects.create(name='Art', project=self.project, color='#fe6565')
        self.task_record_blue = TaskRecord.objects.create(original_value='blue', task=self.task)
        self.task_record_pink = TaskRecord.objects.create(original_value='pink', task=self.task)


    def test_is_valid(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        form = TaskRecordAttributeForm(data)
        self.assertTrue(form.is_valid())


    def test_missing_checker_isnt_valid(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": None }
        form = TaskRecordAttributeForm(data)
        self.assertFalse(form.is_valid())
        data = { "task_records": task_records }
        form = TaskRecordAttributeForm(data)
        self.assertFalse(form.is_valid())


    def test_missing_task_records_isnt_valid(self):
        data = { "task_records": [], "checker": self.olivia }
        form = TaskRecordAttributeForm(data)
        self.assertFalse(form.is_valid())
        data = { "checker": self.olivia }
        form = TaskRecordAttributeForm(data)
        self.assertFalse(form.is_valid())


    def test_it_create_two_attributions_for_olivia(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordAttributeForm(data).save()
        olivia_attributions_count = TaskRecordAttribution.objects.filter(checker=self.olivia).count()
        self.assertEqual(olivia_attributions_count, 2)


    def test_it_create_two_attributions_for_olivia_at_first_round(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordAttributeForm(data).save()
        olivia_attributions_count = TaskRecordAttribution.objects.filter(checker=self.olivia, round=1).count()
        self.assertEqual(olivia_attributions_count, 2)


    def test_it_create_two_attributions_for_olivia_at_next_available_round(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordAttribution.objects.create(round=1, checker=self.pierre, task_record=self.task_record_blue)
        TaskRecordAttribution.objects.create(round=1, checker=self.pierre, task_record=self.task_record_pink)
        TaskRecordAttributeForm(data).save()
        olivia_attributions_count = TaskRecordAttribution.objects.filter(checker=self.olivia, round=2).count()
        self.assertEqual(olivia_attributions_count, 2)


    def test_it_create_two_attributions_for_olivia_at_round_3_manually(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia, "round": 3 }
        TaskRecordAttributeForm(data).save()
        olivia_attributions_count = TaskRecordAttribution.objects.filter(checker=self.olivia, round=3).count()
        self.assertEqual(olivia_attributions_count, 2)


    def test_it_cannot_create_two_more_attributions_for_olivia_at_round_1(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia, "round": 1 }
        TaskRecordAttribution.objects.create(round=1, checker=self.olivia, task_record=self.task_record_blue)
        TaskRecordAttribution.objects.create(round=1, checker=self.olivia, task_record=self.task_record_pink)
        form = TaskRecordAttributeForm(data)
        self.assertFalse(form.is_valid())
