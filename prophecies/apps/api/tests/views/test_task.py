from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task
from prophecies.core.models.choice import Choice
from prophecies.core.models.choice_group import ChoiceGroup



class TestProject(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.project_foo = Project.objects.create(name='foo')
        self.task_paintings = Task.objects.create(name="paintings", project=self.project_foo)
        self.task_shops = Task.objects.create(name="shops", project=self.project_foo)


    def test_it_returns_all_tasks(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/tasks.json')
        self.assertEqual(len(request.json()), 2)


    def test_details_returns_paintings_task(self):
        self.client.login(username='olivia', password='olivia')
        id = self.task_paintings.id
        request = self.client.get('/api/v1/tasks/%s.json' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('name'), 'paintings')


    def test_details_returns_paintings_task(self):
        self.client.login(username='olivia', password='olivia')
        id = self.task_shops.id
        request = self.client.get('/api/v1/tasks/%s.json' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('name'), 'shops')


    def test_details_returns_paintings_task_with_choices(self):
        choice_group = ChoiceGroup.objects.create(name='Which option?')
        self.task_paintings.choice_group = choice_group
        self.task_paintings.save()
        self.client.login(username='olivia', password='olivia')
        id = self.task_paintings.id
        request = self.client.get('/api/v1/tasks/%s.json' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('choice_group').get('name'), 'Which option?')


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/tasks.json')
        self.assertEqual(request.status_code, 403)
