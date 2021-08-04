from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from unittest import mock
import os

class TestSetting(TestCase):
    client = APIClient()
    fixtures = ['settings.json', 'users.json']


    def test_it_returns_all_settings(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [ entity.get('attributes') for entity in request.json().get('data') ]
        self.assertIn({ 'key': 'defaultLocale', 'value': 'en' }, attributes)


    @mock.patch.dict(os.environ, {"PROPHECIES_APP_FOO": "bar"})
    def test_it_returns_setting_from_env(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [ entity.get('attributes') for entity in request.json().get('data') ]
        self.assertIn({ 'key': 'foo', 'value': 'bar' }, attributes)


    @mock.patch.dict(os.environ, {"PROPHECIES_APP_FOO_BAZ": "bar"})
    def test_it_returns_camel_case_setting_from_env(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [ entity.get('attributes') for entity in request.json().get('data') ]
        self.assertIn({ 'key': 'fooBaz', 'value': 'bar' }, attributes)


    @mock.patch.dict(os.environ, {"PROPHECIES_APP_DEFAULT_LOCALE": "fr"})
    def test_it_returns_setting_from_env_without_overriding_db_values(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [ entity.get('attributes') for entity in request.json().get('data') ]
        self.assertIn({ 'key': 'defaultLocale', 'value': 'en' }, attributes)
        self.assertNotIn({ 'key': 'defaultLocale', 'value': 'fr' }, attributes)

    @mock.patch.dict(os.environ, {"PROPHECIES_APP_DEFAULT_LOCALE": "fr"})
    def test_it_returns_single_setting_from_env_without_overriding_db_values(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/defaultLocale/')
        self.assertEqual(request.json().get('data').get('attributes').get('key'), 'defaultLocale')
        self.assertEqual(request.json().get('data').get('attributes').get('value'), 'en')


    def test_it_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/settings/')
        self.assertEqual(request.status_code, 403)
