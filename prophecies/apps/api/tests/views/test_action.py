from actstream import action
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class TestAction(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        self.ruby = User.objects.get(username='ruby')

    def test_list_returns_all_actions(self):
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.olivia, verb='unfollow', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_list_returns_actions_with_verb_attribute(self):
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/')
        self.assertEqual(request.status_code, 200)
        firstAction = request.json().get('data')[0]
        self.assertEqual(firstAction.get('attributes').get('verb'), 'added')

    def test_list_returns_actions_with_actor_relationship(self):
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/')
        self.assertEqual(request.status_code, 200)
        firstAction = request.json().get('data')[0]
        self.assertIn('actor', firstAction.get('relationships', {}))

    def test_list_returns_actions_with_target_relationship(self):
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/')
        self.assertEqual(request.status_code, 200)
        firstAction = request.json().get('data')[0]
        self.assertIn('target', firstAction.get('relationships', {}))

    def test_list_returns_actions_including_actor_relationship(self):
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/')
        self.assertEqual(request.status_code, 200)
        firstIncluded = request.json().get('included')[0]
        self.assertEqual(firstIncluded.get('type'), 'User')
        self.assertEqual(firstIncluded.get('id'), '1')
        self.assertEqual(firstIncluded.get('attributes').get('username'), 'olivia')

    def test_list_return_only_olivia_actions(self):
        action.send(self.ruby, verb='added', target=self.django)
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.django, verb='follow', target=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/?filter[user_stream]=%s' % self.olivia.id)
        action_list = request.json().get('data')
        self.assertEqual(len(action_list), 2)
        request = self.client.get('/api/v1/actions/?filter[user_stream]=%s' % self.ruby.id)
        action_list = request.json().get('data')
        self.assertEqual(len(action_list), 1)

    def test_list_return_only_purchased_actions(self):
        action.send(self.olivia, verb='mentioned', target=self.django)
        action.send(self.olivia, verb='added', target=self.django)
        action.send(self.django, verb='purchased', target=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/?filter[verb]=purchased')
        self.assertEqual(request.status_code, 200)
        action_list = request.json().get('data')
        self.assertEqual(len(action_list), 1)

    def test_list_return_only_mentioned_and_purchased_actions(self):
        action.send(self.olivia, verb='mentioned', target=self.django)
        action.send(self.olivia, verb='added', target=self.django)
        action.send(self.django, verb='purchased', target=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/actions/?filter[verb__in]=mentioned,purchased')
        self.assertEqual(request.status_code, 200)
        action_list = request.json().get('data')
        self.assertEqual(len(action_list), 2)
