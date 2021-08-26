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
