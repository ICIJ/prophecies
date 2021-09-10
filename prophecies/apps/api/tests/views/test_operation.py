from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, TaskRecord, TaskRecordReview


class TestOperation(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        # Create choices
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        Choice.objects.create(name='Yes', choice_group=choice_group)
        Choice.objects.create(name='No', choice_group=choice_group)
        # Create project and task
        project = Project.objects.create(name='foo')
        self.task = Task.objects.create(name="paintings", project=project, choice_group=choice_group)
        # Add a series of records
        self.task_record_foo = TaskRecord.objects.create(original_value="foo", task=self.task)
        self.task_record_bar = TaskRecord.objects.create(original_value="bar", task=self.task)
        # And finally get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')


    def test_it_bulk_update_notes(self):
        foo_review = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        bar_review = TaskRecordReview.objects.create(task_record=self.task_record_bar, checker=self.django)
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        { "id": str(foo_review.id), "method": "update", "payload": "10" },
                        { "id": str(bar_review.id), "method": "update", "payload": "10" }
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
                        { "id": str(foo_review.id), "method": "update", "payload": "10" }
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
        self.assertEqual(request.status_code, 404)


    def test_it_cannot_bulk_update_unknown_record(self):
        payload = {
            "data": {
                "type": "Operation",
                "attributes": {
                    "operations": [
                        { "id": "1000", "method": "update", "payload": "10" }
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
                        { "id": str(foo_review.id), "method": "update", "payload": "10" }
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
                        { "id": 10, "value": { "data": { "type": "TaskRecordReview" } } }
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
                        { "id": str(foo_review.id), "method": "update", "payload": "10" }
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
                        { "id": 10, "value": { "data": { } } }
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