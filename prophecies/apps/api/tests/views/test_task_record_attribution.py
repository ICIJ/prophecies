from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, TaskRecord, TaskRecordAttribution


class TestTaskRecordAttribution(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        # Create choices
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        Choice.objects.create(name='Yes', choice_group=choice_group)
        Choice.objects.create(name='No', choice_group=choice_group)
        # Create project and task
        project = Project.objects.create(name='foo')
        self.task = Task.objects.create(name="paintings", project=project, choice_group=choice_group)
        # Add a series of records
        self.task_record_foo = TaskRecord.objects.create(original_value="foo", task=self.task)
        self.task_record_bar = TaskRecord.objects.create(original_value="bar", task=self.task)
        self.task_record_baz = TaskRecord.objects.create(original_value="baz", task=self.task)
        self.task_record_qux = TaskRecord.objects.create(original_value="qux", task=self.task)
        # And finally get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')


    def test_it_returns_two_task_record_attributions_for_olivia(self):
        TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.olivia)
        TaskRecordAttribution.objects.create(task_record=self.task_record_bar, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-record-attributions.json')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), 2)


    def test_it_returns_one_task_record_attribution_for_django(self):
        TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions.json')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json()), 1)


    def test_it_returns_one_task_record_attribution_for_each_user(self):
        TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        TaskRecordAttribution.objects.create(task_record=self.task_record_bar, checker=self.olivia)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions.json')
        self.assertEqual(len(request.json()), 1)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-record-attributions.json')
        self.assertEqual(len(request.json()), 1)


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/task-record-attributions.json')
        self.assertEqual(request.status_code, 403)


    def test_it_returns_django_task_record_attribution(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('task_record').get('id'), self.task_record_foo.id)


    def test_it_returns_task_record_with_link_from_task(self):
        self.task.recordLinkTemplate = 'https://icij.org/{original_value:u}.json'
        self.task.save()
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('task_record').get('link'), 'https://icij.org/foo.json')


    def test_it_returns_task_record_with_a_choice_field(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertTrue('choice' in request.json())
        self.assertEqual(request.json().get('status'), 'PENDING')


    def test_it_returns_task_record_with_choice_id(self):
        choice = self.task.choice_group.choices.first()
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django, choice=choice)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertEqual(request.json().get('choice'), choice.id)
        self.assertEqual(request.json().get('status'), 'DONE')


    def test_it_cannot_found_task_record_with_normal_user(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertEqual(request.status_code, 404)


    def test_it_cannot_set_task_record_choice_with_normal_user(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo)
        self.client.login(username='django', password='django')
        payload = {'choice': self.task.choice_group.choices.first().id}
        request = self.client.put('/api/v1/task-record-attributions/%s.json' % attribution.id, payload, content_type='application/json')
        self.assertEqual(request.status_code, 404)


    def test_it_cannot_set_task_record_choice_with_superuser(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo)
        self.client.login(username='olivia', password='olivia')
        payload = {'choice': self.task.choice_group.choices.first().id}
        request = self.client.put('/api/v1/task-record-attributions/%s.json' % attribution.id, payload, content_type='application/json')
        self.assertEqual(request.status_code, 404)
        

    def test_it_sets_task_record_choice_with_checker_as_superuser(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        payload = {'choice': self.task.choice_group.choices.first().id}
        request = self.client.put('/api/v1/task-record-attributions/%s.json' % attribution.id, payload, content_type='application/json')
        self.assertEqual(request.status_code, 200)
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertTrue(request.json().get('choice') is not None)
        self.assertEqual(request.json().get('status'), 'DONE')


    def test_it_sets_task_record_choice_with_checker_as_normal_user(self):
        attribution = TaskRecordAttribution.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {'choice': self.task.choice_group.choices.first().id}
        request = self.client.put('/api/v1/task-record-attributions/%s.json' % attribution.id, payload, content_type='application/json')
        self.assertEqual(request.status_code, 200)
        request = self.client.get('/api/v1/task-record-attributions/%s.json' % attribution.id)
        self.assertTrue(request.json().get('choice') is not None)
        self.assertEqual(request.json().get('status'), 'DONE')
