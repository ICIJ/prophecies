from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Choice, ChoiceGroup, UserNotification, Project, Task, TaskRecord, TaskRecordReview, \
    TaskUserStatistics
from prophecies.core.models.task_record_review import StatusType


class TestTaskRecordReview(TestCase):
    def setUp(self):
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')
        self.project = Project.objects.create(name='Pencil Papers')
        checkers = [self.olivia, self.django]
        art_task = Task.objects.create(name='Art', project=self.project, color='#fe6565', rounds=2)
        art_task.checkers.set(checkers)
        art_task.save()
        diet_task = Task.objects.create(name='Diet', project=self.project, rounds=1)
        diet_task.checkers.set(checkers)
        diet_task.save()
        self.choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        self.record_foo = TaskRecord.objects.create(original_value='foo', task=art_task)
        self.record_bar = TaskRecord.objects.create(original_value='bar', task=art_task)
        self.record_baz = TaskRecord.objects.create(original_value='baz', task=art_task)
        self.record_qux = TaskRecord.objects.create(original_value='quz', task=art_task)
        self.record_qud = TaskRecord.objects.create(original_value='qud', task=art_task)
        self.record_fux = TaskRecord.objects.create(original_value='fux', task=diet_task)
        self.record_fax = TaskRecord.objects.create(original_value='fax', task=diet_task)

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
        self.record_foo.reviews.add(
            TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 25% by olivia
        self.record_bar.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        self.record_baz.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        self.record_qux.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        self.record_qud.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.olivia))
        # Get the overall progress
        progress = TaskRecordReview.objects.progress_by_round(checker=self.olivia)
        self.assertEqual(progress[1], 100)
        self.assertEqual(progress[2], 25)

    def test_progress_by_round_for_django(self):
        # Round 1 is completed at 0% by django and at 100% by olivia
        self.record_foo.reviews.add(
            TaskRecordReview.objects.create(round=1, status=StatusType.PENDING, checker=self.django))
        self.record_foo.reviews.add(
            TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))
        # Round 2 is completed at 75% by django
        self.record_bar.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.PENDING, checker=self.django))
        self.record_baz.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        self.record_qux.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        self.record_qud.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.django))
        # Round 2 is completed at 100% by olivia
        self.record_bar.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        self.record_baz.reviews.add(
            TaskRecordReview.objects.create(round=2, status=StatusType.DONE, checker=self.olivia))
        # Get the overall progress
        progress = TaskRecordReview.objects.progress_by_round(checker=self.django)
        self.assertEqual(progress[1], 0)
        self.assertEqual(progress[2], 75)

    def test_cancels_a_review(self):
        # Round 1 is completed at 0% by django and at 100% by olivia
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        review = TaskRecordReview.objects.create(choice=correct, task_record=self.record_foo)
        review.save()
        self.assertEqual(review.status, StatusType.DONE)
        review.choice = None
        review.save()
        self.assertEqual(review.status, StatusType.PENDING)

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

    def test_it_count_reviews_by_tasks(self):
        # Two reviews for the Art task
        self.record_foo.reviews.add(TaskRecordReview.objects.create())
        self.record_bar.reviews.add(TaskRecordReview.objects.create())
        # And one for the Diet task
        self.record_fax.reviews.add(TaskRecordReview.objects.create())
        count_by = TaskRecordReview.objects.all().count_by_task()
        self.assertEqual(len(count_by), 2)
        self.assertEqual(count_by[0]['task'], 1)
        self.assertEqual(count_by[0]['count'], 2)
        self.assertEqual(count_by[1]['task'], 2)
        self.assertEqual(count_by[1]['count'], 1)

    def test_it_count_reviews_by_tasks_with_custom_task_field(self):
        # Two reviews for the Art task
        self.record_foo.reviews.add(TaskRecordReview.objects.create())
        self.record_bar.reviews.add(TaskRecordReview.objects.create())
        count_by = TaskRecordReview.objects.all().count_by_task(task_field='taskId')
        self.assertEqual(count_by[0]['taskId'], 1)

    def test_it_count_reviews_by_tasks_with_custom_count_field(self):
        # Two reviews for the Art task
        self.record_foo.reviews.add(TaskRecordReview.objects.create())
        self.record_bar.reviews.add(TaskRecordReview.objects.create())
        count_by = TaskRecordReview.objects.all().count_by_task(count_field='total')
        self.assertEqual(count_by[0]['total'], 2)

    def test_it_count_reviews_by_choice(self):
        correct = Choice.objects.create(value='Correct', choice_group=self.choice_group)
        incorrect = Choice.objects.create(value='Incorrect', choice_group=self.choice_group)
        # Two reviews for the Art task
        self.record_foo.reviews.add(TaskRecordReview.objects.create(choice=correct))
        self.record_bar.reviews.add(TaskRecordReview.objects.create(choice=incorrect))
        count_by = TaskRecordReview.objects.all().count_by_choice()
        self.assertEqual(len(count_by), 2)
        self.assertEqual(count_by[0]['choice'], correct.id)
        self.assertEqual(count_by[0]['count'], 1)
        self.assertEqual(count_by[1]['choice'], incorrect.id)
        self.assertEqual(count_by[1]['count'], 1)

    def test_it_should_returns_no_mentions(self):
        review = TaskRecordReview(
            note="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(review.mentions), 0)

    def test_it_should_returns_one_mention_with_user(self):
        review = TaskRecordReview(
            note="Hi @django, lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(review.mentions), 1)
        self.assertEqual(review.mentions[0].get('mention'), 'django')
        self.assertEqual(review.mentions[0].get('user'), self.django)

    def test_it_should_returns_one_mention_with_user_and_one_without_user(self):
        review = TaskRecordReview(
            note="Hi @django, lorem @ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(review.mentions), 2)
        #  First mention "@django"
        self.assertEqual(review.mentions[0].get('mention'), 'django')
        self.assertEqual(review.mentions[0].get('user'), self.django)
        #  Second mention "@ipsum" (match with no existing user)
        self.assertEqual(review.mentions[1].get('mention'), 'ipsum')
        self.assertEqual(review.mentions[1].get('user'), None)

    def test_it_should_returns_two_mentions(self):
        review = TaskRecordReview(
            note="Hi @django, it's @olivia lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        self.assertEqual(len(review.mentions), 2)
        #  First mention "@django"
        self.assertEqual(review.mentions[0].get('mention'), 'django')
        self.assertEqual(review.mentions[0].get('user'), self.django)
        #  Second mention "@olivia"
        self.assertEqual(review.mentions[1].get('mention'), 'olivia')
        self.assertEqual(review.mentions[1].get('user'), self.olivia)

    def test_it_should_only_return_one_mention_once(self):
        review = TaskRecordReview(note="Hi @olivia, it's @olivia right?")
        self.assertEqual(len(review.mentions), 1)
        self.assertEqual(review.mentions[0].get('mention'), 'olivia')
        self.assertEqual(review.mentions[0].get('user'), self.olivia)

    def test_it_notifies_user_when_mentioned(self):
        TaskRecordReview.objects.create(note="Hi @olivia!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_once_even_if_mentioned_twice(self):
        TaskRecordReview.objects.create(note="Hi @olivia, it's @olivia right?", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_two_users_when_mentioned(self):
        TaskRecordReview.objects.create(note="Hi @olivia and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned(self):
        TaskRecordReview.objects.create(note="Hi @olivia, @olivia and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned_even_after_edits(self):
        review = TaskRecordReview.objects.create(note="Hi @olivia, @olivia and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)
        review.description = "Hi @olivia and @django!"
        review.save()
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_doesnt_notify_unkown_user(self):
        TaskRecordReview.objects.create(note="Hi @caroline!", checker=self.django)
        self.assertEqual(UserNotification.objects.count(), 0)

    def test_it_doesnt_notify_unkown_user_and_only_known_user(self):
        TaskRecordReview.objects.create(note="Hi @caroline and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)

    def test_it_doesnt_notify_unkown_users_and_only_known_user(self):
        TaskRecordReview.objects.create(note="Hi @caroline, @django and @olivia!", checker=self.django)
        self.assertEqual(UserNotification.objects.count(), 2)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_twice(self):
        TaskRecordReview.objects.create(note="Hi @olivia and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        TaskRecordReview.objects.create(note="Hi again @olivia and @django!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 2)

    def test_it_fills_note_timestamps(self):
        review = TaskRecordReview.objects.create(note="Foo")
        self.assertTrue(review.note_created_at is not None)
        self.assertTrue(review.note_updated_at is None)

    def test_it_fills_note_timestamps_after_save(self):
        review = TaskRecordReview(note="Foo")
        self.assertTrue(review.note_created_at is None)
        review.save()
        self.assertTrue(review.note_created_at is not None)

    def test_it_fills_note_updated_at_on_edits(self):
        review = TaskRecordReview.objects.create(note="Foo")
        self.assertTrue(review.note_updated_at is None)
        review.note = "Bar"
        review.save()
        self.assertTrue(review.note_updated_at is not None)

    def test_it_doesnt_fills_note_updated_without_edits(self):
        review = TaskRecordReview.objects.create(note="Foo")
        self.assertTrue(review.note_updated_at is None)
        review.note = "Foo"
        review.save()
        self.assertTrue(review.note_updated_at is None)

    def test_it_doesnt_fills_note_updated_without_edits_and_initial_note(self):
        review = TaskRecordReview.objects.create()
        review.note = "Foo"
        review.save()
        self.assertTrue(review.note_updated_at is None)

    def test_it_returns_a_task_if_note_mentions_task(self):
        review = TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @task!")
        self.assertTrue(review.mentioned_task is not None)
        self.assertTrue(review.mentioned_task.name == 'Art')

    def test_it_returns_none_if_note_does_not_mention_task(self):
        review = TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi!")
        self.assertTrue(review.mentioned_task is None)

    def test_it_returns_a_project_if_note_mentions_project(self):
        review = TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @project!")
        self.assertTrue(review.mentioned_project is not None)
        self.assertTrue(review.mentioned_project.name == 'Pencil Papers')

    def test_it_returns_none_if_note_does_not_mention_project(self):
        review = TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi!")
        self.assertTrue(review.mentioned_project is None)

    def test_it_notifies_all_project_members_except_for_note_author_not_just_specific_task_checkers(self):
        task_science = Task.objects.create(name='Science', project=self.project, color='#fe6565', rounds=2)
        record_buz = TaskRecord.objects.create(original_value='foo', task=task_science)
        TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @project!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 0)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_does_not_notify_users_who_are_not_project_members(self):
        ruby = User.objects.create(username='ruby')
        TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @project!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 0)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_users_who_are_task_checkers(self):
        ruby = User.objects.create(username='ruby')
        self.record_foo.task.checkers.add(ruby)
        TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @task!", checker=ruby)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_does_not_notify_checker_on_the_instance_when_task_is_mentioned(self):
        ruby = User.objects.create(username='ruby')
        self.record_foo.task.checkers.add(ruby)
        TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @task!", checker=ruby)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 0)

    def test_it_does_not_notify_users_who_are_not_task_checkers(self):
        ruby = User.objects.create(username='ruby')
        TaskRecordReview.objects.create(task_record=self.record_foo, note="Hi @task!", checker=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 0)

    def test_it_creates_a_task_user_statistics_on_save(self):
        TaskRecordReview.objects.create(task_record=self.record_foo, checker=self.django, round=2)
        tus = TaskUserStatistics.objects.filter(checker=self.django, task=self.record_foo.task, round=2)
        self.assertTrue(tus.exists())

    def test_it_creates_a_task_user_statistics_on_save_with_two_pendings(self):
        TaskRecordReview.objects.create(task_record=self.record_foo, checker=self.django, round=2)
        TaskRecordReview.objects.create(task_record=self.record_bar, checker=self.django, round=2)
        tus = TaskUserStatistics.objects.get(checker=self.django, task=self.record_foo.task, round=2)
        self.assertEqual(tus.pending_count, 2)
