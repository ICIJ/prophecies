from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import UserNotification, Tip, Task, TaskRecordReview, Project, TaskRecord, TaskChecker


class TestTip(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Pencil Papers')
        self.art = Task.objects.create(name='Art', project=self.project, color='#fe6565', rounds=2)
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')
        self.record_foo = TaskRecord.objects.create(original_value='foo', task=self.art)

    def test_it_should_returns_no_mentions(self):
        tip = Tip(
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor "
                        "incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 0)

    def test_it_should_returns_one_mention_with_user(self):
        tip = Tip(
            description="Hi @django, lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor "
                        "incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 1)
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)

    def test_it_should_returns_one_mention_with_user_and_one_without_user(self):
        tip = Tip(
            description="Hi @django, lorem @ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor "
                        "incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)
        #  Second mention "@ipsum" (match with no existing user)
        self.assertEqual(tip.mentions[1].get('mention'), 'ipsum')
        self.assertEqual(tip.mentions[1].get('user'), None)

    def test_it_should_returns_two_mentions(self):
        tip = Tip(
            description="Hi @django, it's @olivia lorem ipsum dolor sit amet, consectetur adipisicing elit, "
                        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
                        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum "
                        "dolore eu fugiat nulla pariatur.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)
        #  Second mention "@olivia"
        self.assertEqual(tip.mentions[1].get('mention'), 'olivia')
        self.assertEqual(tip.mentions[1].get('user'), self.olivia)

    def test_it_should_only_return_one_mention_once(self):
        tip = Tip(description="Hi @olivia, it's @olivia right?")
        self.assertEqual(len(tip.mentions), 1)
        self.assertEqual(tip.mentions[0].get('mention'), 'olivia')
        self.assertEqual(tip.mentions[0].get('user'), self.olivia)

    def test_it_notifies_user_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_once_even_if_mentioned_twice(self):
        Tip.objects.create(description="Hi @olivia, it's @olivia right?", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_two_users_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia, @olivia and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned_even_after_edits(self):
        tip = Tip.objects.create(description="Hi @olivia, @olivia and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.count(), 2)
        tip.description = "Hi @olivia and @django!"
        tip.save()
        self.assertEqual(UserNotification.objects.count(), 2)

    def test_it_doesnt_notify_unkown_user(self):
        Tip.objects.create(description="Hi @caroline!", creator=self.django)
        self.assertEqual(UserNotification.objects.count(), 0)

    def test_it_doesnt_notify_unkown_user_and_only_known_user(self):
        Tip.objects.create(description="Hi @caroline and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)

    def test_it_doesnt_notify_unkown_users_and_only_known_user(self):
        Tip.objects.create(description="Hi @caroline, @django and @olivia!", creator=self.django)
        self.assertEqual(UserNotification.objects.count(), 2)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_twice(self):
        Tip.objects.create(description="Hi @olivia and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)
        Tip.objects.create(description="Hi again @olivia and @django!", creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 2)

    def test_it_returns_a_task_if_description_mentions_task(self):
        review = Tip.objects.create(task=self.record_foo.task, creator=self.django, description="Hi @task!")
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
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.django)
        task_science = Task.objects.create(name='Science', project=self.project, color='#fe6565', rounds=2)
        record_buz = TaskRecord.objects.create(original_value='foo', task=task_science)
        TaskChecker.objects.create(task=record_buz.task, checker=self.olivia)
        Tip.objects.create(description="Hi @project!", creator=self.django, project=self.project, task=task_science)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 0)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_does_not_notify_users_who_are_not_project_members(self):
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.django)
        ruby = User.objects.create(username='ruby')
        TaskChecker.objects.create(task=self.record_foo.task, checker=ruby)
        Tip.objects.create(description="Hi @project!", creator=self.django, project=self.project)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 0)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 0)

    def test_it_notifies_users_who_are_task_checkers(self):
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.django)
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.olivia)
        ruby = User.objects.create(username='ruby')
        TaskChecker.objects.create(task=self.record_foo.task, checker=ruby)
        Tip.objects.create(description="Hi @task!", creator=ruby, task=self.record_foo.task, project=self.project)
        self.assertEqual(UserNotification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(UserNotification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_does_not_notify_checker_on_the_instance_when_task_is_mentioned(self):
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.django)
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.olivia)
        ruby = User.objects.create(username='ruby')
        TaskChecker.objects.create(task=self.record_foo.task, checker=ruby)
        Tip.objects.create(task=self.record_foo.task, project=self.project, description="Hi @task!", creator=ruby)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 0)

    def test_it_does_not_notify_users_who_are_not_task_checkers(self):
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.django)
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.olivia)
        ruby = User.objects.create(username='ruby')
        Tip.objects.create(task=self.record_foo.task, project=self.project, description="Hi @task!",
                           creator=self.django)
        self.assertEqual(UserNotification.objects.filter(recipient=ruby).count(), 0)

    def test_it_should_filter_tips_based_on_user_access(self):
        TaskChecker.objects.create(task=self.record_foo.task, checker=self.olivia)
        Tip.objects.create(description="Hi, you should be able to see this", creator=self.django, project=self.project,
                           task=self.record_foo.task)
        Tip.objects.create(description="Hi, you also should be able to see this", creator=self.django)
        project = Project.objects.create(name='Chronos')
        task = Task.objects.create(name='Jewels', project=project, color='#fe6565', rounds=2)
        Tip.objects.create(description="Hi, you should not be able to see this", creator=self.django, project=project,
                           task=task)
        user_scoped_tips = Tip.objects.user_scope(self.olivia)
        self.assertEqual(len(user_scoped_tips), 2)

    def test_it_set_a_project_when_a_task_is_given(self):
        tip = Tip.objects.create(description="Foo", creator=self.django, task=self.art)
        self.assertEqual(tip.project, self.project)

    def test_it_set_task_to_none_when_its_not_part_of_project(self):
        fincen_files = Project.objects.create(name='FinCEN Files')
        addresses = Task.objects.create(name='Addresses', project=fincen_files)
        tip = Tip.objects.create(description="Foo", creator=self.django, project=self.project, task=addresses)
        self.assertEqual(tip.task, None)
