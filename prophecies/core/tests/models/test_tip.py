from actstream.models import Action
from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Notification, Tip

class TestTip(TestCase):
    def setUp(self):
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')

    def test_it_should_returns_no_mentions(self):
        tip = Tip(description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 0)

    def test_it_should_returns_one_mention_with_user(self):
        tip = Tip(description="Hi @django, lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 1)
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)

    def test_it_should_returns_one_mention_with_user_and_one_without_user(self):
        tip = Tip(description="Hi @django, lorem @ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)
        #  Second mention "@ipsum" (match with no existing user)
        self.assertEqual(tip.mentions[1].get('mention'), 'ipsum')
        self.assertEqual(tip.mentions[1].get('user'), None)

    def test_it_should_returns_two_mentions(self):
        tip = Tip(description="Hi @django, it's @olivia lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(tip.mentions[0].get('mention'), 'django')
        self.assertEqual(tip.mentions[0].get('user'), self.django)
        #  Second mention "@olivia"
        self.assertEqual(tip.mentions[1].get('mention'), 'olivia')
        self.assertEqual(tip.mentions[1].get('user'), self.olivia)

    def test_it_should_only_return_one_mention_once(self):
        tip = Tip(description="Hi @olivia, it's @olivia right?")
        self.assertEqual(len(tip.mentions), 1)
        self.assertEqual(tip.mentions[0].get('mention'), 'olivia')
        self.assertEqual(tip.mentions[0].get('user'), self.olivia)

    def test_it_notifies_user_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_once_even_if_mentioned_twice(self):
        Tip.objects.create(description="Hi @olivia, it's @olivia right?", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_two_users_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia and @django!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(Notification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned(self):
        Tip.objects.create(description="Hi @olivia, @olivia and @django!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(Notification.objects.count(), 2)

    def test_it_notifies_two_users_once_when_mentioned_even_after_edits(self):
        tip = Tip.objects.create(description="Hi @olivia, @olivia and @django!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(Notification.objects.count(), 2)
        tip.description = "Hi @olivia and @django!"
        tip.save()
        self.assertEqual(Notification.objects.count(), 2)

    def test_it_doesnt_notify_unkown_user(self):
        Tip.objects.create(description="Hi @caroline!", creator=self.django)
        self.assertEqual(Notification.objects.count(), 0)

    def test_it_doesnt_notify_unkown_user_and_only_known_user(self):
        Tip.objects.create(description="Hi @caroline and @django!", creator=self.django)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.django).count(), 1)

    def test_it_doesnt_notify_unkown_users_and_only_known_user(self):
        Tip.objects.create(description="Hi @caroline, @django and @olivia!", creator=self.django)
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.filter(recipient=self.django).count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)

    def test_it_notifies_user_twice(self):
        Tip.objects.create(description="Hi @olivia and @django!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 1)
        Tip.objects.create(description="Hi again @olivia and @django!", creator=self.django)
        self.assertEqual(Notification.objects.filter(recipient=self.olivia).count(), 2)
