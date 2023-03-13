from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, TaskRecord, TaskRecordReview


class TestTaskRecord(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        # Create choices
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        Choice.objects.create(name='Yes', choice_group=choice_group)
        Choice.objects.create(name='No', choice_group=choice_group)
        # And finally get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        # Create project and task
        project = Project.objects.create(name='foo')
        self.task = Task.objects.create(name="paintings", project=project, choice_group=choice_group)
        self.task.checkers.add(self.django)
        self.task.checkers.add(self.olivia)

    def test_he_cannot_lock_non_assigned_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': True
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)

    def test_he_can_lock_assigned_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': True
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)

    def test_record_is_locked_by_user_automaticaly(self):
        task_record = TaskRecord.objects.create(task=self.task)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': True
                }
            }
        }
        self.client.put('/api/v1/task-records/%s/' % task_record.id, payload, content_type='application/vnd.api+json')
        request = self.client.get('/api/v1/task-records/%s/' % task_record.id)
        data = request.json().get('data')
        self.assertTrue(data.get('attributes').get('locked'))
        self.assertEqual(data.get('relationships').get('lockedBy').get('data').get('id'), str(self.django.id))

    def test_he_cannot_lock_already_locked_record(self):
        task_record = TaskRecord.objects.create(task=self.task, locked=True)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': True
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 400)

    def test_she_cannot_unlock_record_she_didnt_lock(self):
        task_record = TaskRecord.objects.create(task=self.task, locked_by=self.django, locked=True)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': False
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 400)

    def test_she_can_unlock_record_she_locked(self):
        task_record = TaskRecord.objects.create(task=self.task, locked_by=self.olivia, locked=True)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': False
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)

    def test_she_cannot_unlock_already_unlocked_record(self):
        task_record = TaskRecord.objects.create(task=self.task, locked_by=None, locked=False)
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': False
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 400)

    def test_he_cannot_lock_record_from_locked_task(self):
        task_record = TaskRecord.objects.create(task=self.task)
        self.task.lock()
        review = TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'locked': True
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)

    def test_olivia_bookmarked_a_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        task_record.bookmarked_by.add(self.olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.django)

        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-records/%s/' % task_record.id)
        data = request.json().get('data')
        self.assertTrue(data.get('attributes').get('bookmarked'))

    def test_django_didnt_bookmark_a_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        task_record.bookmarked_by.add(self.olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.olivia)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.django)

        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-records/%s/' % task_record.id)
        data = request.json().get('data')
        self.assertFalse(data.get('attributes').get('bookmarked'))

    def test_he_can_unbookmark_a_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'bookmarked': True
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)
        self.assertTrue(task_record.bookmarked_by.filter(id=self.django.id).exists())

    def test_he_can_unbookmark_a_record(self):
        task_record = TaskRecord.objects.create(task=self.task)
        task_record.bookmarked_by.add(self.django)
        TaskRecordReview.objects.create(task_record=task_record, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecord',
                'id': task_record.id,
                'attributes': {
                    'bookmarked': False
                }
            }
        }
        request = self.client.put('/api/v1/task-records/%s/' % task_record.id, payload,
                                  content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)
        self.assertFalse(task_record.bookmarked_by.filter(id=self.django.id).exists())
