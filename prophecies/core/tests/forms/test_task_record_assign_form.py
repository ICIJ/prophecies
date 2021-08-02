from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Project, Task, TaskRecord, TaskRecordReview
from prophecies.core.forms import TaskRecordAssignForm

class TaskRecordAssignFormTests(TestCase):
    def setUp(self):
        self.olivia = User.objects.create(username='olivia')
        self.pierre = User.objects.create(username='pierre')
        self.maxime = User.objects.create(username='maxime')
        self.project = Project.objects.create(name='Pencil Papers')
        self.task = Task.objects.create(name='Art', project=self.project, color='#fe6565', rounds=2)
        self.task_record_blue = TaskRecord.objects.create(original_value='blue', task=self.task)
        self.task_record_pink = TaskRecord.objects.create(original_value='pink', task=self.task)
        self.task.checkers.add(self.olivia)
        self.task.checkers.add(self.pierre)
        self.task.checkers.add(self.maxime)


    def test_is_valid(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        form = TaskRecordAssignForm(data)
        self.assertTrue(form.is_valid())


    def test_missing_checker_isnt_valid(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": None }
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())
        data = { "task_records": task_records }
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())


    def test_missing_task_records_isnt_valid(self):
        data = { "task_records": [], "checker": self.olivia }
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())
        data = { "checker": self.olivia }
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())


    def test_it_create_two_reviews_for_olivia(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordAssignForm(data).save()
        olivia_reviews_count = TaskRecordReview.objects.filter(checker=self.olivia).count()
        self.assertEqual(olivia_reviews_count, 2)


    def test_it_create_two_reviews_for_olivia_at_first_round(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordAssignForm(data).save()
        olivia_reviews_count = TaskRecordReview.objects.filter(checker=self.olivia, round=1).count()
        self.assertEqual(olivia_reviews_count, 2)


    def test_it_create_two_reviews_for_olivia_at_next_available_round(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia }
        TaskRecordReview.objects.create(round=1, checker=self.pierre, task_record=self.task_record_blue)
        TaskRecordReview.objects.create(round=1, checker=self.pierre, task_record=self.task_record_pink)
        TaskRecordAssignForm(data).save()
        olivia_reviews_count = TaskRecordReview.objects.filter(checker=self.olivia, round=2).count()
        self.assertEqual(olivia_reviews_count, 2)


    def test_it_create_two_reviews_for_olivia_at_round_three_manually(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia, "round": 3 }
        TaskRecordAssignForm(data).save()
        olivia_reviews_count = TaskRecordReview.objects.filter(checker=self.olivia, round=3).count()
        self.assertEqual(olivia_reviews_count, 2)


    def test_it_cannot_create_two_more_reviews_for_olivia_at_round_one(self):
        task_records = [self.task_record_blue, self.task_record_pink]
        data = { "task_records": task_records, "checker": self.olivia, "round": 1 }
        TaskRecordReview.objects.create(round=1, checker=self.olivia, task_record=self.task_record_blue)
        TaskRecordReview.objects.create(round=1, checker=self.olivia, task_record=self.task_record_pink)
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())


    def test_it_cannot_add_more_than_two_rounds_of_reviews(self):
        TaskRecordReview.objects.create(task_record=self.task_record_blue, checker=self.olivia)
        TaskRecordReview.objects.create(task_record=self.task_record_blue, checker=self.pierre)
        task_records = [self.task_record_blue]
        data = { "task_records": task_records, "checker": self.maxime }
        form = TaskRecordAssignForm(data)
        self.assertFalse(form.is_valid())
