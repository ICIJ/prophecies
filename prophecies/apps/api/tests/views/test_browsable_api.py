from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class TestBrowsableApi(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def test_it_renders_the_browsable_api_for_an_authenticated_user(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-records/', headers={'accept': 'text/html'})
        self.assertEqual(request.status_code, 200)

    def test_it_renders_the_browsable_api_for_an_anonymous_user(self):
        request = self.client.get('/api/v1/task-records/', headers={'accept': 'text/html'})
        self.assertEqual(request.status_code, 403)
