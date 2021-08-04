from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task

class TestProject(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.project_foo = Project.objects.create(name='foo')
        self.project_bar = Project.objects.create(name='bar')


    def test_list_returns_all_projects(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/projects/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)


    def test_details_returns_project_foo(self):
        self.client.login(username='olivia', password='olivia')
        id = self.project_foo.id
        request = self.client.get('/api/v1/projects/%s/' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('data').get('attributes').get('name'), 'foo')


    def test_details_returns_project_bar(self):
        self.client.login(username='olivia', password='olivia')
        id = self.project_bar.id
        request = self.client.get('/api/v1/projects/%s/' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('data').get('attributes').get('name'), 'bar')


    def test_details_returns_project_foo_tasks(self):
        self.client.login(username='olivia', password='olivia')
        Task.objects.create(name="paintings", project=self.project_foo)
        id = self.project_foo.id
        request = self.client.get('/api/v1/projects/%s/tasks/' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 1)


    def test_details_returns_project_bar_tasks(self):
        self.client.login(username='olivia', password='olivia')
        Task.objects.create(name="addresses", project=self.project_bar)
        Task.objects.create(name="transactions", project=self.project_bar)
        id = self.project_bar.id
        request = self.client.get('/api/v1/projects/%s/tasks/' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/projects/')
        self.assertEqual(request.status_code, 403)
