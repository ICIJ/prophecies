from django.test import TestCase
from prophecies.core.models.choice import Choice
from prophecies.core.models.choice_group import ChoiceGroup


class TestChoice(TestCase):
    def setUp(self):
        self.choice_group = ChoiceGroup.objects.create(name='Which option?')

    def test_it_uses_name_as_value_when_none_provided(self):
        choice_a = Choice.objects.create(name='a', choice_group=self.choice_group)
        choice_b = Choice.objects.create(name='b', choice_group=self.choice_group)
        self.assertEqual(choice_a.value, 'a')
        self.assertEqual(choice_b.value, 'b')

    def test_it_doesnt_use_name_as_value_when_one_provided(self):
        ChoiceGroup.objects.create(name='Which option?')
        choice_a = Choice.objects.create(name='a', value='A', choice_group=self.choice_group)
        choice_b = Choice.objects.create(name='b', value='B', choice_group=self.choice_group)
        self.assertEqual(choice_a.value, 'A')
        self.assertEqual(choice_b.value, 'B')
