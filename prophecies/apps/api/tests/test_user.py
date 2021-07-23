from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate

class TestSetting(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def test_it_returns_all_users(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users.json')
        self.assertEqual(len(request.json()), 2)


    def test_it_returns_current_user(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users/me.json')
        self.assertEqual(request.json().get('id'), 1)
        self.assertEqual(request.json().get('username'), 'olivia')


    def test_it_returns_another_user(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/users/2.json')
        self.assertEqual(request.json().get('id'), 2)
        self.assertEqual(request.json().get('username'), 'django')


    def test_it_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/users.json')
        self.assertEqual(request.status_code, 403)
