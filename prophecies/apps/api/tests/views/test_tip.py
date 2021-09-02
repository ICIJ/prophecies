from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import Project, Task, Tip

class TestTip(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        self.project_foo = Project.objects.create(name='foo')
        self.task_paintings = Task.objects.create(name='paintings', project=self.project_foo)
        self.tip_bar = Tip.objects.create(name='bar', description='@user try this', task=self.task_paintings, project=self.project_foo)
        self.tip_top = Tip.objects.create(name='top', description='@user try this instead', task=self.task_paintings, project=self.project_foo)

    def test_it_returns_all_tips(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/tips/')
        data = request.json().get('data')
        self.assertEqual(len(data), 2)

    def test_details_returns_bar_tip(self):
        self.client.login(username='olivia', password='olivia')
        id = self.tip_bar.id
        request = self.client.get('/api/v1/tips/%s/' % id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(data['attributes']['name'], 'bar')

    def test_details_returns_top_tip(self):
        self.client.login(username='olivia', password='olivia')
        id = self.tip_top.id
        request = self.client.get('/api/v1/tips/%s/' % id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(data['attributes']['name'], 'top')

    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/tips/')
        self.assertEqual(request.status_code, 403)
