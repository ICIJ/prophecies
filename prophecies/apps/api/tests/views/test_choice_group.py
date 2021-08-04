from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import ChoiceGroup

class TestChoiceGroup(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.choice_group_foo = ChoiceGroup.objects.create(name='foo')
        self.choice_group_bar = ChoiceGroup.objects.create(name='bar')


    def test_list_returns_all_choice_groups(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/choice-groups/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)


    def test_details_returns_choice_group_foo(self):
        self.client.login(username='olivia', password='olivia')
        id = self.choice_group_foo.id
        request = self.client.get('/api/v1/choice-groups/%s/' % id)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json().get('data').get('attributes').get('name'), 'foo')


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/choice-groups/')
        self.assertEqual(request.status_code, 403)
