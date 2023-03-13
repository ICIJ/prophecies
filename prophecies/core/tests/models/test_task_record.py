from actstream import action
from django.contrib.auth.models import User
from django.test import TestCase

from prophecies.core.models import Choice, ChoiceGroup, Project, TaskRecord, TaskRecordReview
from prophecies.core.models.task import Task


class TestTaskRecord(TestCase):
    def setUp(self):
        self.do_you_agree = ChoiceGroup.objects.create(name='Do you agree?')
        self.agree = Choice.objects.create(name="agree", choice_group=self.do_you_agree)
        self.disagree = Choice.objects.create(name="disagree", choice_group=self.do_you_agree)
        self.project = Project.objects.create(name='FinCEN Files')
        self.transactions_task = Task.objects.create(name='Transactions', project=self.project)

    def test_it_should_use_task_record_link(self):
        task = Task.objects.create(name='Addresses', project=self.project)
        task_record = TaskRecord.objects.create(task=task, link='https://offshoreleaks.icij.org', original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://offshoreleaks.icij.org')

    def test_it_should_ignore_task_link_template(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={original_value}')
        task_record = TaskRecord.objects.create(task=task, link='https://offshoreleaks.icij.org', original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://offshoreleaks.icij.org')

    def test_it_should_use_task_link_template(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={original_value}')
        task_record = TaskRecord.objects.create(task=task, original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=foo')

    def test_it_should_use_task_link_template_with_metadata(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.foo}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": "Paris"})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Paris')

    def test_it_should_use_task_link_template_with_nested_metadata(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.foo.bar}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": {"bar": "Paris"}})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Paris')

    def test_it_should_use_task_link_template_with_nested_list(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.foo.bar[1]}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": {"bar": ["Paris", "London"]}})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')

    def test_it_should_use_task_link_template_with_canonical_string(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata}')
        task_record = TaskRecord.objects.create(task=task, metadata="London")
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')

    def test_it_should_use_task_link_template_with_a_list(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata[1]}')
        task_record = TaskRecord.objects.create(task=task, metadata=["Paris", "London"])
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')

    def test_it_should_use_task_link_template_with_a_list_of_objects(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata[1].city}')
        task_record = TaskRecord.objects.create(task=task, metadata=[{"city": "Paris"}, {"city": "London"}])
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')

    def test_it_should_use_task_link_template_with_urlencored_original_value(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={original_value:u}')
        task_record = TaskRecord.objects.create(task=task, original_value='Kuala Lumpur')
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Kuala%20Lumpur')

    def test_it_should_use_task_link_template_with_urlencored_metadata_field(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.city:u}')
        task_record = TaskRecord.objects.create(task=task, metadata={'city': 'Kuala Lumpur'})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Kuala%20Lumpur')

    def test_it_should_use_task_link_template_with_unknown_key(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={foo}')
        task_record = TaskRecord.objects.create(task=task)
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=')

    def test_it_should_use_task_link_template_with_unknown_metadata_key(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.foo}')
        task_record = TaskRecord.objects.create(task=task)
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=')

    def test_it_should_use_task_link_template_with_nunknown_nested_metadata_key(self):
        task = Task.objects.create(name='Addresses', project=self.project,
                                   record_link_template='https://www.openstreetmap.org/search?query={metadata.foo.bar}')
        task_record = TaskRecord.objects.create(task=task)
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=')

    def test_it_should_have_a_list_of_checkers(self):
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=django)
        self.assertTrue(olivia in task_record.checkers)
        self.assertTrue(django in task_record.checkers)

    def test_it_should_allow_both_checkers_to_lock(self):
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=django)
        self.assertTrue(task_record.can_lock(olivia))
        self.assertTrue(task_record.can_lock(django))

    def test_it_should_only_allow_olivia_to_unlock(self):
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        pierre = User.objects.create(username='pierre')
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=django)
        task_record.locked = True
        task_record.locked_by = olivia
        self.assertTrue(task_record.can_unlock(olivia))
        self.assertFalse(task_record.can_unlock(django))
        self.assertFalse(task_record.can_unlock(pierre))

    def test_it_should_list_all_actions_related_to_a_record(self):
        olivia = User.objects.create(username='olivia')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        action.send(olivia, verb='locked', target=task_record)
        action.send(olivia, verb='unlocked', target=task_record)
        self.assertEqual(len(task_record.actions), 2)

    def test_it_should_list_all_actions_related_to_a_record_reviews(self):
        olivia = User.objects.create(username='olivia')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=olivia)
        action.send(olivia, verb='commented', target=review)
        self.assertEqual(len(task_record.actions), 1)

    def test_it_should_list_all_actions_related_to_a_record_and_reviews(self):
        olivia = User.objects.create(username='olivia')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=olivia)
        action.send(olivia, verb='locked', target=task_record)
        action.send(olivia, verb='commented', target=review)
        self.assertEqual(len(task_record.actions), 2)

    def test_has_disagreements_with_two_different_choices(self):
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, choice=self.agree)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, choice=self.disagree)
        self.assertTrue(task_record.has_disagreements)

    def test_hasnt_disagreements_with_two_same_choices(self):
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, choice=self.agree)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, choice=self.agree)
        self.assertFalse(task_record.has_disagreements)

    def test_hasnt_disagreements_with_one_choice(self):
        olivia = User.objects.create(username='olivia')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, choice=self.agree)
        self.assertFalse(task_record.has_disagreements)

    def test_hasnt_disagreements_with_one_choice_and_one_empty_choice(self):
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, choice=self.agree)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, choice=None)
        self.assertFalse(task_record.has_disagreements)

    def test_latest_round_is_correct(self):
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, round=1)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, round=2)
        latest_round = TaskRecordReview.objects.latest_round(task_record)
        self.assertEqual(latest_round, 2)

    def test_latest_round_is_correct_even_with_different_round_order(self):
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, round=2)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, round=1)
        latest_round = TaskRecordReview.objects.latest_round(task_record)
        self.assertEqual(latest_round, 2)

    def test_show_a_pretty_list_of_3_checkers(self):
        ruby = User.objects.create(username='ruby')
        olivia = User.objects.create(username='olivia')
        django = User.objects.create(username='django')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=ruby, round=1)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, round=2)
        TaskRecordReview.objects.create(task_record=task_record, checker=django, round=3)
        self.assertEqual(task_record.checkers_pretty, 'ruby, olivia and django')

    def test_show_a_pretty_list_of_2_checkers(self):
        ruby = User.objects.create(username='ruby')
        olivia = User.objects.create(username='olivia')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=ruby, round=1)
        TaskRecordReview.objects.create(task_record=task_record, checker=olivia, round=2)
        self.assertEqual(task_record.checkers_pretty, 'ruby and olivia')

    def test_show_a_pretty_list_of_1_checker(self):
        ruby = User.objects.create(username='ruby')
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        TaskRecordReview.objects.create(task_record=task_record, checker=ruby, round=1)
        self.assertEqual(task_record.checkers_pretty, 'ruby')

    def test_show_a_pretty_list_of_no_checkers(self):
        task_record = TaskRecord.objects.create(task=self.transactions_task)
        self.assertEqual(task_record.checkers_pretty, 'nobody')
