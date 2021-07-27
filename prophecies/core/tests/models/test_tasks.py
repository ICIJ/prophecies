from django.test import TestCase
from prophecies.core.models.project import Project
from prophecies.core.models.task import Task
from prophecies.core.contrib.colors import hex_scale_brightness

class TestTask(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Pencil Papers')
        self.task = Task.objects.create(name='Art', project=self.project, color='#fe6565')


    def test_it_returns_3_colors(self):
        self.assertEqual(self.task.colors[0], hex_scale_brightness('#fe6565', 0.75))
        self.assertEqual(self.task.colors[1], hex_scale_brightness('#fe6565', 1.00))
        self.assertEqual(self.task.colors[2], hex_scale_brightness('#fe6565', 1.25))
