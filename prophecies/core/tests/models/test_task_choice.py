from django.test import TestCase
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task
from prophecies.core.models.task_choice import TaskChoice
from prophecies.core.models.task_choices_group import TaskChoicesGroup

class TestTaskChoice(TestCase):
    def setUp(self):
        self.task_choices_group = TaskChoicesGroup.objects.create(name='Which option?')


    def test_it_uses_name_as_value_when_none_provided(self):
        choice_a = TaskChoice.objects.create(name='a', choices_group=self.task_choices_group)
        choice_b = TaskChoice.objects.create(name='b', choices_group=self.task_choices_group)
        self.assertEqual(choice_a.value, 'a')
        self.assertEqual(choice_b.value, 'b')


    def test_it_doesnt_use_name_as_value_when_one_provided(self):
        task_choices_group = TaskChoicesGroup.objects.create(name='Which option?')
        choice_a = TaskChoice.objects.create(name='a', value='A', choices_group=self.task_choices_group)
        choice_b = TaskChoice.objects.create(name='b', value='B', choices_group=self.task_choices_group)
        self.assertEqual(choice_a.value, 'A')
        self.assertEqual(choice_b.value, 'B')
