from actstream.models import Action
from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Task, TaskRecord, TaskRecordReview, Project
from prophecies.core.models.task_record_review import StatusType
from prophecies.core.contrib.colors import hex_scale_brightness

class TestTask(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Pencil Papers')
        self.art = Task.objects.create(name='Art', project=self.project, color='#fe6565', rounds=3)
        self.shop = Task.objects.create(name='Shop', project=self.project, rounds=3)
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')


    def test_it_returns_3_colors(self):
        self.assertEqual(self.art.colors[0], hex_scale_brightness('#fe6565', 0.75))
        self.assertEqual(self.art.colors[1], hex_scale_brightness('#fe6565', 1.00))
        self.assertEqual(self.art.colors[2], hex_scale_brightness('#fe6565', 1.25))


    def test_progress_by_round_for_django(self):
        record_foo = TaskRecord.objects.create(task=self.art)
        record_bar = TaskRecord.objects.create(task=self.art)
        # Round 1 is completed at 0% by django and at 100% by olivia
        record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.PENDING, checker=self.django))
        record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 100% by django
        record_bar.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        # Get the overall progress
        progress = self.art.progress_by_round(checker=self.django)
        self.assertEqual(progress[1], 0)
        self.assertEqual(progress[2], 100)


    def test_progress_by_round_on_two_tasks(self):
        record_painting = TaskRecord.objects.create(task=self.art)
        record_gallery = TaskRecord.objects.create(task=self.shop)
        # Round 1 is completed at 100% by olivia on both tasks
        record_painting.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        record_gallery.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 0% by django on "Art" and 100% on "Shop"
        record_painting.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.django))
        record_gallery.reviews.add(TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        # Get the overall progress for "Art"
        progress = self.art.progress_by_round()
        self.assertEqual(progress[1], 100)
        self.assertEqual(progress[2], 0)
        self.assertEqual(progress[3], 0)
        # Get the overall progress for "Shop"
        progress = self.shop.progress_by_round()
        self.assertEqual(progress[1], 100)
        self.assertEqual(progress[2], 100)
        self.assertEqual(progress[3], 0)


    def test_progress_is_0(self):
        TaskRecord.objects.create(task=self.art, status=StatusType.PENDING)
        TaskRecord.objects.create(task=self.art, status=StatusType.PENDING)
        self.assertEqual(self.art.progress, 0)


    def test_progress_is_50(self):
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.PENDING)
        self.assertEqual(self.art.progress, 50)


    def test_progress_is_75(self):
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.PENDING)
        self.assertEqual(self.art.progress, 75)


    def test_progress_is_100(self):
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        self.assertEqual(self.art.progress, 100)


    def test_progress_is_100_without_mixing_tasks(self):
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.art, status=StatusType.DONE)
        TaskRecord.objects.create(task=self.shop, status=StatusType.PENDING)
        self.assertEqual(self.art.progress, 100)

    def test_it_locks_the_task(self):
        task = Task.objects.create(name='Foo', project=self.project)
        self.assertEqual(task.status, 'OPEN')
        task.lock()
        self.assertEqual(task.status, 'LOCKED')

    def test_it_closes_the_task(self):
        task = Task.objects.create(name='Foo', project=self.project)
        self.assertEqual(task.status, 'OPEN')
        task.close()
        self.assertEqual(task.status, 'CLOSED')

    def test_it_opens_the_task(self):
        task = Task.objects.create(name='Foo', status='CLOSED', project=self.project)
        self.assertEqual(task.status, 'CLOSED')
        task.open()
        self.assertEqual(task.status, 'OPEN')

    def test_task_is_locked(self):
        task = Task.objects.create(name='Foo', project=self.project)
        task.lock()
        self.assertTrue(task.is_locked)

    def test_task_is_closed(self):
        task = Task.objects.create(name='Foo', project=self.project)
        task.close()
        self.assertTrue(task.is_closed)

    def test_task_is_open(self):
        task = Task.objects.create(name='Foo', status='CLOSED', project=self.project)
        task.open()
        self.assertTrue(task.is_open)

    def test_it_log_action_when_task_is_locked(self):
        task = Task.objects.create(name='Foo', project=self.project, creator=self.olivia)
        task.lock()
        action = Action.objects.filter_actor(actor=self.olivia).first()
        self.assertTrue(action is not None)
        self.assertEqual(action.verb, 'locked')
        self.assertEqual(action.target, task)

    def test_it_log_action_when_task_is_closed(self):
        task = Task.objects.create(name='Foo', project=self.project, creator=self.olivia)
        task.close()
        action = Action.objects.filter_actor(actor=self.olivia).first()
        self.assertTrue(action is not None)
        self.assertEqual(action.verb, 'closed')
        self.assertEqual(action.target, task)

    def test_it_log_action_when_task_is_open(self):
        task = Task.objects.create(name='Foo', project=self.project, creator=self.olivia, status='CLOSE')
        task.open()
        action = Action.objects.filter_actor(actor=self.olivia).first()
        self.assertTrue(action is not None)
        self.assertEqual(action.verb, 'open')
        self.assertEqual(action.target, task)
