from actstream import action
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

class TestSetting(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def test_list_returns_all_users(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users/')
        self.assertEqual(len(request.json().get('data')), 2)


    def test_me_returns_current_user(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users/me/')
        self.assertEqual(request.json().get('data').get('id'), '1')
        self.assertEqual(request.json().get('data').get('attributes').get('username'), 'olivia')


    def test_get_returns_another_user(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/users/2/')
        self.assertEqual(request.json().get('data').get('id'), '2')
        self.assertEqual(request.json().get('data').get('attributes').get('username'), 'django')


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/users/')
        self.assertEqual(request.status_code, 403)


    def test_get_has_email_md5_field_only(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users/me/')
        email = 'engineering@icij.org'
        email_md5 = '628e9a99d87799e9d434b63d2c3744ca'
        self.assertEqual(request.json().get('data').get('attributes').get('email'), None)
        self.assertEqual(request.json().get('data').get('attributes').get('emailMd5'), email_md5)

    def test_get_user_actions(self):
        olivia = User.objects.get(pk=1)
        action.send(olivia, verb='locked')
        action.send(olivia, verb='unlocked')
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/users/1/relationships/actions/')
        self.assertEqual(len(request.json().get('data')), 2)
