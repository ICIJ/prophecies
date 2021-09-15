from django.contrib.auth.models import User
from django.test import TestCase
from prophecies.core.models import Project, Task, TaskChecker
from prophecies.core.models.task_record_review import StatusType

class TestProject(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Pencil Papers')
        self.task_art = Task.objects.create(name='Art', project=self.project, color='#fe6565', rounds=2)
        self.task_prop = Task.objects.create(name='Property', project=self.project, color='#fe6565', rounds=2)
        self.task_jewels = Task.objects.create(name='Jewels', project=self.project, color='#fe6565', rounds=2)
        self.olivia = User.objects.create(username='olivia')
        self.django = User.objects.create(username='django')

    def test_it_returns_members_of_project_if_members_have_one_task(self):
        TaskChecker.objects.create(task=self.task_art, checker=self.django)
        TaskChecker.objects.create(task=self.task_art, checker=self.olivia)
        self.assertTrue(len(self.project.members) == 2)

    def test_it_returns_members_of_project_if_members_have_multiple_tasks(self):
        TaskChecker.objects.create(task=self.task_art, checker=self.django)
        TaskChecker.objects.create(task=self.task_prop, checker=self.django)
        TaskChecker.objects.create(task=self.task_prop, checker=self.olivia)
        TaskChecker.objects.create(task=self.task_jewels, checker=self.olivia)
        self.assertTrue(len(self.project.members) == 2)

    def test_it_returns_members_of_project_if_some_members_have_multiple_tasks(self):
        TaskChecker.objects.create(task=self.task_art, checker=self.django)
        TaskChecker.objects.create(task=self.task_prop, checker=self.olivia)
        TaskChecker.objects.create(task=self.task_jewels, checker=self.olivia)
        self.assertTrue(len(self.project.members) == 2)

    def test_it_returns_empty_query_set_if_members_have_no_tasks(self):
        project = Project.objects.create(name='Crayon Papers')
        task = Task.objects.create(name='Art', project=project, color='#fe6565', rounds=2)
        self.assertTrue(len(project.members) == 0)
