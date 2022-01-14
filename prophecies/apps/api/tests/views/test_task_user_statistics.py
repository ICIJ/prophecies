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
        self.task = Task.objects.create(name="paintings", project=project)
        self.task.checkers.add(self.olivia)
        self.task.checkers.add(self.django)
        # Add a record
        self.task_record_foo = TaskRecord.objects.create(original_value="foo", task=self.task)


    def test_it_returns_two_users_statistics(self):
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.olivia, round=1)
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django, round=1)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-statistics/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 2)
        