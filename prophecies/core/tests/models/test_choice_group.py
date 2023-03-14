from django.test import TestCase
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task
from prophecies.core.models.choice import Choice
from prophecies.core.models.choice_group import ChoiceGroup


class TestChoiceGroup(TestCase):
    def test_instance_to_string_display_choices(self):
        choice_group = ChoiceGroup.objects.create(name='Which option?')
        self.assertEqual(str(choice_group), 'Which option?')
        choice_a = Choice.objects.create(name='a', choice_group=choice_group)
        choice_b = Choice.objects.create(name='b', choice_group=choice_group)
        self.assertEqual(choice_group.choices.count(), 2)
        self.assertEqual(str(choice_group), 'Which option? (a | b)')
