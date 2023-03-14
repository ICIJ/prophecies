from actstream.models import Action
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import UserNotification


class TestUserNotification(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        django = User.objects.get(username='django')
        olivia = User.objects.get(username='olivia')
        followed = Action.objects.create(actor=django, verb='followed', target=olivia)
        followed_back = Action.objects.create(actor=olivia, verb='followed', target=django)
        mentioned = Action.objects.create(actor=django, verb='mentioned', target=olivia)
        self.followed = UserNotification.objects.create(action=followed, recipient=olivia, read=False)
        self.followed_back = UserNotification.objects.create(action=followed_back, recipient=django, read=False)
        self.mentioned = UserNotification.objects.create(action=mentioned, recipient=olivia, read=False)

    def test_list_returns_olvias_notifications(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/user-notifications/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_list_returns_djangos_notifications(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/user-notifications/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 1)

    def test_list_doesnt_return_olvia_in_included_objects(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        try:
            next(i for i in included if i['type'] == 'User' and i['id'] == '1')
            self.fail('API returned olivia in included objects')
        except StopIteration:
            pass

    def test_list_doesnt_return_django_in_included_objects(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        with self.assertRaises(StopIteration):
            next(i for i in included if i['type'] == 'User' and i['id'] == '2')

    def test_list_returns_mentioned_action_in_included_objects_for_olivia(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        with self.assertRaises(StopIteration):
            next(i for i in included if i['type'] == 'User' and i['id'] == '1')

    def test_list_doesnt_return_mentioned_action_in_included_objects_for_django(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        with self.assertRaises(StopIteration):
            next(i for i in included if i['type'] == 'Action' and i['attributes']['verb'] == 'mentioned')

    def test_list_returns_mentioned_action_in_included_objects_for_olivia(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        try:
            next(i for i in included if i['type'] == 'Action' and i['attributes']['verb'] == 'mentioned')
        except StopIteration:
            self.fail('API did not returns "mentioned" Action in included objects')

    def test_list_returns_followed_action_in_included_objects_for_django(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/user-notifications/', {'include': 'action.actor'})
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        try:
            next(i for i in included if i['type'] == 'Action' and i['attributes']['verb'] == 'followed')
        except StopIteration:
            self.fail('API did not returns "followed" Action in included objects')

    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/user-notifications/')
        self.assertEqual(request.status_code, 403)

    def test_it_cannot_mark_followed_notification_as_read_with_django_user(self):
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed.id,
                'attributes': {
                    'read': True
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 404)

    def test_it_can_mark_followed_notification_as_read_with_olivia_user(self):
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed.id,
                'attributes': {
                    'read': True
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)

    def test_it_cannot_mark_followed_back_notification_as_read_with_olivia_user(self):
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed_back.id,
                'attributes': {
                    'read': True
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed_back.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 404)

    def test_it_can_mark_followed_back_notification_as_read_with_django_user(self):
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed_back.id,
                'attributes': {
                    'read': True
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed_back.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)

    def test_it_mark_notification_as_read_correctly(self):
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed.id,
                'attributes': {
                    'read': True
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed.id, payload,
                                  content_type='application/vnd.api+json')
        self.followed.refresh_from_db()
        self.assertTrue(self.followed.read)
        self.assertTrue(self.followed.read_at is not None)

    def test_it_cannot_set_read_at_attribute(self):
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'UserNotification',
                'id': self.followed.id,
                'attributes': {
                    'readAt': '2021-09-01'
                }
            }
        }
        request = self.client.put('/api/v1/user-notifications/%s/' % self.followed.id, payload,
                                  content_type='application/vnd.api+json')
        self.followed.refresh_from_db()
        self.assertTrue(self.followed.read_at is None)
