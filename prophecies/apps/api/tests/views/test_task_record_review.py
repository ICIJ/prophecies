from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, TaskRecord, TaskRecordReview


class TestTaskRecordReview(TestCase):
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
        self.task_record_baz = TaskRecord.objects.create(original_value="baz", task=self.task)
        self.task_record_qux = TaskRecord.objects.create(original_value="qux", task=self.task)
        # And finally get our two users (from the fixtures)
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')


    def test_it_returns_two_task_record_reviews_for_olivia(self):
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.olivia)
        TaskRecordReview.objects.create(task_record=self.task_record_bar, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-record-reviews/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 2)


    def test_it_returns_one_task_record_review_for_django(self):
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 1)


    def test_it_returns_all_task_record_reviews_for_each_user(self):
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        TaskRecordReview.objects.create(task_record=self.task_record_bar, checker=self.olivia)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/')
        data = request.json().get('data')
        self.assertEqual(len(data), 2)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-record-reviews/')
        data = request.json().get('data')
        self.assertEqual(len(data), 2)


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/task-record-reviews/')
        self.assertEqual(request.status_code, 403)


    def test_it_returns_django_task_record_review(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        relationships = data.get('relationships')
        self.assertEqual(relationships['taskRecord']['data']['id'], str(self.task_record_foo.id))


    def test_it_returns_task_record_with_link_from_task(self):
        self.task.recordLinkTemplate = 'https://icij.org/{original_value:u}.json'
        self.task.save()
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        included = request.json().get('included')
        relationships = data.get('relationships')
        task_record_entity = next(entity for entity  in included if entity['type'] == 'TaskRecord' and entity['id'] == str(self.task_record_foo.id))
        self.assertEqual(task_record_entity['attributes']['link'], 'https://icij.org/foo.json')


    def test_it_returns_task_record_with_a_choice_field(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        data = request.json().get('data')
        relationships = data.get('relationships')
        self.assertTrue('choice' in relationships)
        self.assertEqual(data.get('attributes').get('status'), 'PENDING')


    def test_it_returns_task_record_with_choice_id(self):
        choice = self.task.choice_group.choices.first()
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django, choice=choice)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        data = request.json().get('data')
        self.assertEqual(data.get('relationships').get('choice').get('data').get('id'), str(choice.id))
        self.assertEqual(data.get('attributes').get('status'), 'DONE')


    def test_it_cannot_found_task_record_with_normal_user(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo)
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        self.assertEqual(request.status_code, 403)


    def test_it_returns_number_of_task_record_reviews_for_olivia_by_task(self):
        TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.olivia)
        TaskRecordReview.objects.create(task_record=self.task_record_bar, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-record-reviews/')
        self.assertEqual(request.status_code, 200)
        countBy = request.json().get('meta').get('countBy')
        self.assertEqual(len(countBy), 1)
        self.assertEqual(countBy[0]['taskId'], 1)
        self.assertEqual(countBy[0]['count'], 2)


    def test_it_cannot_set_task_record_choice_with_normal_user(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)


    def test_it_cannot_set_task_record_choice_with_superuser(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo)
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)


    def test_it_sets_task_record_choice_with_checker_as_superuser(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.olivia)
        self.client.login(username='olivia', password='olivia')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        data = request.json().get('data')
        self.assertTrue(data.get('relationships').get('choice') is not None)
        self.assertEqual(data.get('attributes').get('status'), 'DONE')


    def test_it_sets_task_record_choice_with_checker_as_normal_user(self):
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)
        request = self.client.get('/api/v1/task-record-reviews/%s/' % attribution.id)
        data = request.json().get('data')
        self.assertTrue(data.get('relationships').get('choice') is not None)
        self.assertEqual(data.get('attributes').get('status'), 'DONE')


    def test_it_cannot_make_changes_to_locked_record_except_note(self):
        self.task_record_foo.locked = True
        self.task_record_foo.save()
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'attributes': {
                },
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)

    def test_it_can_make_changes_to_note_on_locked_record(self):
        task_record_with_note = TaskRecord.objects.create(original_value="foo", task=self.task)
        task_record_with_note.locked = True
        task_record_with_note.save()
        attribution = TaskRecordReview.objects.create(task_record=task_record_with_note, checker=self.django, note='this is a note')
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'attributes': {
                    'note': 'this is an edited note'
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 200)

    def test_it_can_only_make_changes_to_note_on_locked_record(self):
        task_record_with_note = TaskRecord.objects.create(original_value="foo", task=self.task)
        task_record_with_note.locked = True
        task_record_with_note.save()
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        choice_yes = Choice.objects.create(name='Yes', choice_group=choice_group)
        choice_no = Choice.objects.create(name='No', choice_group=choice_group)
        attribution = TaskRecordReview.objects.create(task_record=task_record_with_note, checker=self.django, note='this is a note')
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'attributes': {
                    'note': 'this is an edited note'
                },
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)


    def test_it_cannot_make_changes_to_a_record_from_locked_task(self):
        self.task.lock()
        attribution = TaskRecordReview.objects.create(task_record=self.task_record_foo, checker=self.django)
        self.client.login(username='django', password='django')
        payload = {
            'data': {
                'type': 'TaskRecordReview',
                'id': attribution.id,
                'relationships': {
                    'choice': {
                        'data': {
                            'type': 'Choice',
                            'id': self.task.choice_group.choices.first().id
                        }
                    }
                }
            }
        }
        request = self.client.put('/api/v1/task-record-reviews/%s/' % attribution.id, payload, content_type='application/vnd.api+json')
        self.assertEqual(request.status_code, 403)
