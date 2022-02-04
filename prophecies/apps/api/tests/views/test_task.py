from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from prophecies.core.models import ChoiceGroup, Project, Task


class TestTask(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        
        self.project_foo = Project.objects.create(name='foo')
        self.project_bar = Project.objects.create(name='bar')
        self.task_paintings = Task.objects.create(name="paintings", project=self.project_foo)
        self.django = User.objects.get(username='django')
        self.olivia = User.objects.get(username='olivia')
        self.task_paintings.checkers.add(self.django)
        self.task_shops = Task.objects.create(name="shops", project=self.project_foo)
        self.task_immatriculations = Task.objects.create(name="immatriculations", project=self.project_bar)


    def test_it_returns_only_tasks_where_im_a_checker(self):
        self.client.login(username='django', password='django')
        request = self.client.get('/api/v1/tasks/')
        data = request.json().get('data')
        self.assertEqual(len(data), 2)


    def test_details_returns_paintings_task(self):
        self.client.login(username='olivia', password='olivia')
        id = self.task_paintings.id
        request = self.client.get('/api/v1/tasks/%s/' % id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(data['attributes']['name'], 'paintings')


    def test_details_returns_paintings_task(self):
        self.client.login(username='olivia', password='olivia')
        id = self.task_shops.id
        request = self.client.get('/api/v1/tasks/%s/' % id)
        self.assertEqual(request.status_code, 404)
        self.task_shops.checkers.add(self.olivia)
        request = self.client.get('/api/v1/tasks/%s/' % id)
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(data['attributes']['name'], 'shops')


    def test_details_returns_paintings_task_with_choices(self):
        choice_group = ChoiceGroup.objects.create(name='Which option?')
        self.task_paintings.choice_group = choice_group
        self.task_paintings.checkers.add(self.olivia)
        
        self.task_paintings.save()
        self.client.login(username='olivia', password='olivia')
        id = self.task_paintings.id
        request = self.client.get('/api/v1/tasks/%s/' % id, { 'include': 'choiceGroup.choices' })
        self.assertEqual(request.status_code, 200)
        included = request.json().get('included')
        choice_group_entity = next(entity for entity  in included if entity['type'] == 'ChoiceGroup')
        self.assertEqual(choice_group_entity['attributes']['name'], 'Which option?')


    def test_list_reject_unauthenticated_request(self):
        self.client.logout()
        request = self.client.get('/api/v1/tasks/')
        self.assertEqual(request.status_code, 403)
