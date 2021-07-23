from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate

class TestSetting(TestCase):
    client = APIClient()
    fixtures = ['settings.json', 'users.json']


    def test_it_returns_all_settings(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings.json')
        self.assertIn({ 'key': 'defaultLocale', 'value': 'en' }, request.json())


    def test_it_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/settings.json')
        self.assertEqual(request.status_code, 403)
