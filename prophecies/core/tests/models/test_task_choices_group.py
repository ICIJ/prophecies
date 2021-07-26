from django.test import TestCase
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task
from prophecies.core.models.task_choice import TaskChoice
from prophecies.core.models.task_choices_group import TaskChoicesGroup

class TestTaskChoicesGroup(TestCase):
    def test_instance_to_string_display_choices(self):
        task_choices_group = TaskChoicesGroup.objects.create(name='Which option?')
        self.assertEqual(str(task_choices_group), 'Which option?')
        choice_a = TaskChoice.objects.create(name='a', choices_group=task_choices_group)
        choice_b = TaskChoice.objects.create(name='b', choices_group=task_choices_group)
        self.assertEqual(task_choices_group.choices.count(), 2)
        self.assertEqual(str(task_choices_group), 'Which option? (a | b)')
