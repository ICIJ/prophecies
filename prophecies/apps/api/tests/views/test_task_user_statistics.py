from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from prophecies.core.models import Project, Task, TaskRecord, TaskRecordReview


class TestTaskUserStatistics(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        # Get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        # Create project and task
        project = Project.objects.create(name='foo')
        # Add Olivia and Django to the Painting task
        self.paintings = Task.objects.create(name="paintings", project=project)
        self.paintings.checkers.add(self.olivia)
        self.paintings.checkers.add(self.django)
        # Add only Django to the Shops task
        self.shops = Task.objects.create(name="shops", project=project)
        self.shops.checkers.add(self.django)
        # Add a record
        self.task_record_of_paintings = TaskRecord.objects.create(original_value="foo", task=self.paintings)
        self.task_record_of_shops = TaskRecord.objects.create(original_value="bar", task=self.shops)

    def test_it_returns_two_users_statistics(self):
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings, checker=self.olivia, round=1)
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings, checker=self.django, round=1)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-statistics/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 2)

    def test_it_returns_user_statistics_for_assigned_tasks(self):
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings, checker=self.olivia, round=1)
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings, checker=self.django, round=2)
        TaskRecordReview.objects.create(task_record=self.task_record_of_shops, checker=self.django, round=1)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-statistics/')
        self.assertEqual(len(request.json().get('data')), 2)

        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-user-statistics/')
        self.assertEqual(len(request.json().get('data')), 3)
