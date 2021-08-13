from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, TaskRecord, TaskRecordReview
from prophecies.core.models.task_record_review import StatusType
from prophecies.core.models.task import Task

class TestTaskRecordReview(TestCase):
    def setUp(self):
        project = Project.objects.create(name='Pencil Papers')
        task = Task.objects.create(name='Art', project=project, color='#fe6565', rounds=2)
        self.choice_group = ChoiceGroup.objects.create(name='Is it correct?')
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


    def test_set_has_notes_in_task_record_to_true(self):
        TaskRecordReview.objects.create(note='foo', task_record=self.record_foo)
        TaskRecordReview.objects.create(note='bar', task_record=self.record_foo)
        self.assertTrue(self.record_foo.has_notes)


    def test_set_has_notes_in_task_record_to_false(self):
        TaskRecordReview.objects.create(note='', task_record=self.record_foo)
        TaskRecordReview.objects.create(note=None, task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_notes)


    def test_change_has_notes_in_task_record_to_true(self):
        self.record_foo.has_notes = False
        self.record_foo.save()
        TaskRecordReview.objects.create(note='foo', task_record=self.record_foo)
        self.assertTrue(self.record_foo.has_notes)


    def test_change_has_notes_in_task_record_to_false(self):
        self.record_foo.has_notes = True
        self.record_foo.save()
        TaskRecordReview.objects.create(note='', task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_notes)


    def test_change_has_notes_in_task_record_to_true_when_update_review(self):
        review = TaskRecordReview.objects.create(note='', task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_notes)
        review.note = 'foo'
        review.save()
        self.assertTrue(self.record_foo.has_notes)


    def test_set_has_disagreements_in_task_record_to_true(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        incorrect = Choice.objects.create(value='Incorrect', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=incorrect, task_record=self.record_foo)
        self.assertTrue(self.record_foo.has_disagreements)


    def test_set_has_disagreements_in_task_record_to_false(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_disagreements)


    def test_set_has_disagreements_in_task_record_to_true_ignoring_empty(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        incorrect = Choice.objects.create(value='Incorrect', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=incorrect, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=None, task_record=self.record_foo)
        self.assertTrue(self.record_foo.has_disagreements)


    def test_set_has_disagreements_in_task_record_to_false_ignoring_empty(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        TaskRecordReview.objects.create(choice=None, task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_disagreements)


    def test_change_has_disagreements_in_task_record_to_true(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        incorrect = Choice.objects.create(value='Incorrect', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        last_review = TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        self.assertFalse(self.record_foo.has_disagreements)
        last_review.choice = incorrect
        last_review.save()
        self.assertTrue(self.record_foo.has_disagreements)


    def test_change_has_disagreements_in_task_record_to_false(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        incorrect = Choice.objects.create(value='Incorrect', choice_group=self.choice_group)
        TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        last_review = TaskRecordReview.objects.create(choice=incorrect, task_record=self.record_foo)
        self.assertTrue(self.record_foo.has_disagreements)
        last_review.choice = correct
        last_review.save()
        self.assertFalse(self.record_foo.has_disagreements)
