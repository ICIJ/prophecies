from actstream.models import Action
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from prophecies.core.models import Choice, ChoiceGroup, UserNotification, \
    Project, Task, TaskRecord, TaskRecordReview


class TestOperation(TestCase):
    client = APIClient()
    fixtures = ['users.json']

    def setUp(self):
        # Create choices
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        Choice.objects.create(name='Yes', choice_group=choice_group)
        Choice.objects.create(name='No', choice_group=choice_group)
        # Get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        # Create project and task
        project = Project.objects.create(name='foo')
        self.task = Task.objects.create(name="paintings", project=project, choice_group=choice_group)
        self.task.checkers.add(self.olivia)
        self.task.checkers.add(self.django)
        # Add a series of records
        self.task_record_foo = TaskRecord.objects.create(original_value="foo", task=self.task)
        self.task_record_bar = TaskRecord.objects.create(original_value="bar", task=self.task)

    def test_it_bulk_update_notes(self):
        foo_review = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        bar_review = TaskRecordReview.objects.create(task_record=self.task_record_bar, checker=self.django)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": str(foo_review.id), "method": "update", "payload": "10"},
                        {"id": str(bar_review.id), "method": "update", "payload": "10"}
                    ],
                    "payloads": [
                        {
                            "id": "10",
                            "value": {
                                "data": {
                                    "type": "TaskRecordReview",
                                    "attributes": {
                                        "note": "same!"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 200)
        foo_review.refresh_from_db()
        self.assertEqual(foo_review.note, 'same!')
        bar_review.refresh_from_db()
        self.assertEqual(bar_review.note, 'same!')

    def test_it_cannot_bulk_update_notes(self):
        foo_review = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": str(foo_review.id), "method": "update", "payload": "10"}
                    ],
                    "payloads": [
                        {
                            "id": "10",
                            "value": {
                                "data": {
                                    "type": "TaskRecordReview",
                                    "attributes": {
                                        "note": "same!"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='olivia', password='olivia')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 403)

    def test_it_cannot_bulk_update_unknown_record(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": "1000", "method": "update", "payload": "10"}
                    ],
                    "payloads": [
                        {
                            "id": "10",
                            "value": {
                                "data": {
                                    "type": "TaskRecordReview",
                                    "attributes": {
                                        "note": "same!"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 404)

    def test_it_cannot_bulk_update_notes_with_wrong_type(self):
        foo_review = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": str(foo_review.id), "method": "update", "payload": "10"}
                    ],
                    "payloads": [
                        {
                            "id": "10",
                            "value": {
                                "data": {
                                    "type": "TaskRecordReview",
                                    "attributes": {
                                        "note": ['wrong', 'note', 'value']
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 400)

    def test_it_create_operation_with_and_empty_list_of_operations(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [],
                    "payloads": [
                        {"id": 10, "value": {"data": {"type": "TaskRecordReview"}}}
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 200)

    def test_it_create_operation_with_and_empty_list_of_payloads_if_no_operations(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [],
                    "payloads": []
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 200)

    def test_it_cannot_bulk_update_with_unknown_payload(self):
        foo_review = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": str(foo_review.id), "method": "update", "payload": "10"}
                    ],
                    "payloads": []
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 400)

    def test_it_cannot_bulk_update_without_payload_type(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [],
                    "payloads": [
                        {"id": 10, "value": {"data": {}}}
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 400)

    def test_it_cannot_bulk_update_without_a_valid_payload_type(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [],
                    "payloads": [
                        {
                            "id": 10,
                            "value": {
                                "data": {
                                    "type": "Project"
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='django', password='django')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 400)

    def test_it_can_mark_notifications_a_read(self):
        followed = Action.objects.create(actor=self.django, verb='followed', target=self.olivia)
        mentioned = Action.objects.create(actor=self.django, verb='mentioned', target=self.olivia)
        notif_followed = UserNotification.objects.create(action=followed, recipient=self.olivia, read=False)
        notif_mentioned = UserNotification.objects.create(action=mentioned, recipient=self.olivia, read=False)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        {"id": str(notif_followed.id), "method": "update", "payload": "1"},
                        {"id": str(notif_mentioned.id), "method": "update", "payload": "1"}
                    ],
                    "payloads": [
                        {
                            "id": "1",
                            "value": {
                                "data": {
                                    "type": "UserNotification",
                                    "attributes": {
                                        "read": True
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.client.login(username='olivia', password='olivia')
        content_type = 'application/vnd.api+json; ext=bulk'
        request = self.client.post('/api/v1/operations/', payload, content_type=content_type)
        self.assertEqual(request.status_code, 200)
        notif_followed.refresh_from_db()
        self.assertEqual(notif_followed.read, True)
        notif_mentioned.refresh_from_db()
        self.assertEqual(notif_mentioned.read, True)
