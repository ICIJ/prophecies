from actstream import action
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

class TestActionAggregation(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')

    
    def test_list_returns_all_action_aggregations(self):
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.olivia, verb='unfollow', target=self.django)
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.olivia, verb='unfollow', target=self.django)

        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/action-aggregations/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)
