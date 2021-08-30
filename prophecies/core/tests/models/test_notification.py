from actstream.models import Action
from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Notification

class TestNotification(TestCase):

    def setUp(self):
        self.django = User.objects.create(username='django')
        self.olivia = User.objects.create(username='olivia')


    def test_it_mark_notification_as_read(self):
        action = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        notification = Notification.objects.create(action=action, recipient=self.olivia)
        self.assertFalse(notification.read)
        notification.mark_as_read()
        self.assertTrue(notification.read)


    def test_it_add_time_to_notification_when_marked_as_read(self):
        action = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        notification = Notification.objects.create(action=action, recipient=self.olivia)
        self.assertTrue(notification.read_at is None)
        notification.mark_as_read()
        self.assertTrue(notification.read_at is not None)


    def test_it_add_time_to_notification_when_marked_as_read_during_creation(self):
        action = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        notification = Notification.objects.create(action=action, recipient=self.olivia, read=True)
        notification.mark_as_read()
        self.assertTrue(notification.read_at is not None)


    def test_it_gets_all_unread_notifications(self):
        followed = Action.objects.create(actor=self.django, verb='followed', target=self.olivia)
        mentioned = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        Notification.objects.create(action=followed, recipient=self.olivia, read=False)
        Notification.objects.create(action=mentioned, recipient=self.olivia, read=True)
        self.assertTrue(Notification.objects.unread().count(), 1)
        self.assertFalse(Notification.objects.unread().first().read)


    def test_it_gets_all_read_notifications(self):
        followed = Action.objects.create(actor=self.django, verb='followed', target=self.olivia)
        mentioned = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        Notification.objects.create(action=followed, recipient=self.olivia, read=False)
        Notification.objects.create(action=mentioned, recipient=self.olivia, read=True)
        self.assertTrue(Notification.objects.read().count(), 1)
        self.assertTrue(Notification.objects.read().first().read)


    def test_it_gets_mark_notifications_as_read(self):
        followed = Action.objects.create(actor=self.django, verb='followed', target=self.olivia)
        mentioned = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        Notification.objects.create(action=followed, recipient=self.olivia)
        Notification.objects.create(action=mentioned, recipient=self.olivia)
        self.assertEqual(Notification.objects.read().count(), 0)
        Notification.objects.mark_as_read()
        self.assertEqual(Notification.objects.read().count(), 2)
