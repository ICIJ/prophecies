import os
from unittest import mock

from django.test import TestCase
from rest_framework.test import APIClient

from prophecies.core.models.setting import Setting


class TestSetting(TestCase):
    client = APIClient()
    fixtures = ['settings.json', 'users.json']

    def test_it_returns_all_settings(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [entity.get('attributes') for entity in request.json().get('data')]
        self.assertIn({'key': 'defaultLocale', 'value': 'en', 'public': False}, attributes)

    @mock.patch.dict(os.environ, {"PROPHECIES_APP_FOO": "bar"})
    def test_it_returns_setting_from_env(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [entity.get('attributes') for entity in request.json().get('data')]
        self.assertIn({'key': 'foo', 'value': 'bar', 'public': False}, attributes)

    @mock.patch.dict(os.environ, {"PROPHECIES_APP_FOO_BAZ": "bar"})
    def test_it_returns_camel_case_setting_from_env(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [entity.get('attributes') for entity in request.json().get('data')]
        self.assertIn({'key': 'fooBaz', 'value': 'bar', 'public': False}, attributes)

    @mock.patch.dict(os.environ, {"PROPHECIES_APP_DEFAULT_LOCALE": "fr"})
    def test_it_returns_setting_from_env_without_overriding_db_values(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/')
        attributes = [entity.get('attributes') for entity in request.json().get('data')]
        self.assertIn({'key': 'defaultLocale', 'value': 'en', 'public': False}, attributes)
        self.assertNotIn({'key': 'defaultLocale', 'value': 'fr', 'public': False}, attributes)

    @mock.patch.dict(os.environ, {"PROPHECIES_APP_DEFAULT_LOCALE": "fr"})
    def test_it_returns_single_setting_from_env_without_overriding_db_values(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/settings/defaultLocale/')
        self.assertEqual(request.json().get('data').get('attributes').get('key'), 'defaultLocale')
        self.assertEqual(request.json().get('data').get('attributes').get('value'), 'en')

    def test_it_return_no_public_settings_for_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/settings/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 0)

    def test_it_return_two_public_settings_for_unauthenticated_request(self):
        Setting.objects.get(key='defaultLocale').publish()
        Setting.objects.get(key='loginUrl').publish()
        self.client.logout()
        request = self.client.get('/api/v1/settings/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_it_return_cannot_retrieve_a_public_setting_for_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/settings/defaultLocale/')
        self.assertEqual(request.status_code, 404)

    def test_it_return_can_retrieve_a_public_setting_for_unauthenticated_request(self):
        Setting.objects.get(key='defaultLocale').publish()
        self.client.logout()
        request = self.client.get('/api/v1/settings/defaultLocale/')
        self.assertEqual(request.status_code, 200)
