from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Tip

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
        self.assertEqual(getattr(tip.mentions[0], 'mention'), 'django')
        self.assertEqual(getattr(tip.mentions[0], 'user'), self.django)

    def test_it_should_returns_one_mention_with_user_and_one_without_user(self):
        tip = Tip(description="Hi @django, lorem @ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(getattr(tip.mentions[0], 'mention'), 'django')
        self.assertEqual(getattr(tip.mentions[0], 'user'), self.django)
        #  Second mention "@ipsum" (match with no existing user)
        self.assertEqual(getattr(tip.mentions[1], 'mention'), 'ipsum')
        self.assertEqual(getattr(tip.mentions[1], 'user'), None)

    def test_it_should_returns_two_mentions(self):
        tip = Tip(description="Hi @django, it's @olivia lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        self.assertEqual(len(tip.mentions), 2)
        #  First mention "@django"
        self.assertEqual(getattr(tip.mentions[0], 'mention'), 'django')
        self.assertEqual(getattr(tip.mentions[0], 'user'), self.django)
        #  Second mention "@olivia"
        self.assertEqual(getattr(tip.mentions[1], 'mention'), 'olivia')
        self.assertEqual(getattr(tip.mentions[1], 'user'), self.olivia)

    def test_it_should_only_return_one_mention_once(self):
        tip = Tip(description="Hi @olivia, it's @olivia right?")
        self.assertEqual(len(tip.mentions), 1)
        self.assertEqual(getattr(tip.mentions[0], 'mention'), 'olivia')
        self.assertEqual(getattr(tip.mentions[0], 'user'), self.olivia)
