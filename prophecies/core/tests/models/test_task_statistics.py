from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from prophecies.core.models import Task, TaskRecord, TaskRecordReview, Project


from prophecies.core.models.task_record_review import StatusType


statistics_url = '/api/v1/task-statistics/'

class TestTaskUserStatistics(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        self.project = Project.objects.create(name='Pencil Papers')
        self.paintings = Task.objects.create(name="paintings", project=self.project, rounds=3)
        
        checkers = [self.olivia, self.django]
        self.paintings.checkers.set(checkers)
        
        self.record_foo = TaskRecord.objects.create(task=self.paintings)
        self.record_bar = TaskRecord.objects.create(task=self.paintings)
        # Round 1 is completed at 0% by django and at 100% by olivia
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.PENDING, checker=self.django))
        self.record_foo.reviews.add(TaskRecordReview.objects.create(round=1, status=StatusType.DONE, checker=self.olivia))


    def test_it_returns_all_task_stats(self):
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-statistics/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
    
    
    def test_it_shows_task_checkers_count(self) :
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-statistics/1/')
        data = request.json().get('data')
        self.assertEqual(data["attributes"]["checkersCount"], 2)
        