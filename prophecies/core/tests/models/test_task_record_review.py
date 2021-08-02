from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Project, Task, TaskRecord, TaskRecordReview
from prophecies.core.models.task_record_review import StatusType
from prophecies.core.models.task import Task

class TestTaskRecordReview(TestCase):
    def setUp(self):
        project = Project.objects.create(name='Pencil Papers')
        task = Task.objects.create(name='Art', project=project, color='#fe6565', rounds=2)
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')
        self.record_foo = TaskRecord.objects.create(original_value='foo', task=task)
        self.record_bar = TaskRecord.objects.create(original_value='bar', task=task)
        self.record_baz = TaskRecord.objects.create(original_value='baz', task=task)
        self.record_qux = TaskRecord.objects.create(original_value='quz', task=task)
        self.record_qud = TaskRecord.objects.create(original_value='qud', task=task)


    def test_progress_by_round_for_all(self):
        # Task Record "foo" is completed at 100%
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE))
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE))
        # Task Record "bar" is completed at 50%
        self.record_bar.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE))
        self.record_bar.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING))
        # Get the overall progress
        progress = TaskRecordReview.objects.progress_by_round()
        self.assertEqual(progress[1], 100)
        self.assertEqual(progress[2], 50)


    def test_progress_by_round_for_olivia(self):
        # Round 1 is completed at 100% by olivia
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 25% by olivia
        self.record_bar.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        self.record_baz.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        self.record_qux.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        self.record_qud.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        # Get the overall progress
        progress = TaskRecordReview.objects.progress_by_round(checker=self.olivia)
        self.assertEqual(progress[1], 100)
        self.assertEqual(progress[2], 25)


    def test_progress_by_round_for_django(self):
        # Round 1 is completed at 0% by django and at 100% by olivia
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.PENDING, checker=self.django))
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 75% by django
        self.record_bar.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.django))
        self.record_baz.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        self.record_qux.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        self.record_qud.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        # Round 2 is completed at 100% by olivia
        self.record_bar.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        self.record_baz.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        # Get the overall progress
        progress = TaskRecordReview.objects.progress_by_round(checker=self.django)
        self.assertEqual(progress[1], 0)
        self.assertEqual(progress[2], 75)
