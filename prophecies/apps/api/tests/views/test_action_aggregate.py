from actstream import action
from django.contrib.auth.models import User
from prophecies.core.filters import ActionAggregateFilter
from prophecies.core.models import Choice, ChoiceGroup, Project, Task, ActionAggregate

from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
import time_machine
import datetime as dt


action_aggregates_url = '/api/v1/action-aggregates/'

class TestActionAggregate(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        # Create choices
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        Choice.objects.create(name='Yes', choice_group=choice_group)
        Choice.objects.create(name='No', choice_group=choice_group)
        # Create project and task
        project = Project.objects.create(name='foo')
        project_bar = Project.objects.create(name='bar')
        self.task = Task.objects.create(name="paintings", project=project_bar, choice_group=choice_group)
        self.task_shops = Task.objects.create(name="shops", project=project, choice_group=choice_group)

        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')
        self.ruby = User.objects.get(username='ruby')
        self.task_shops.checkers.add(self.ruby)
        self.task_shops.checkers.add(self.olivia)
        self.task.checkers.add(self.olivia)
        
        

    def test_create_aggregated_action_post_save_on_action(self):
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        self.client.login(username='olivia', password='olivia')

        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),1)

        first_aggregate_attributes= action_aggregates[0].get('attributes')
        self.assertEqual(first_aggregate_attributes.get('count'),1)

    def test_update_aggregated_action_using_streams(self):
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        self.client.login(username='olivia', password='olivia')

        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),1)
        first_aggregate_attributes= action_aggregates[0].get('attributes')
        self.assertEqual(first_aggregate_attributes.get('count'),2)

    def test_aggregation_by_task(self):
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task_shops.id)
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task_shops.id)

        self.client.login(username='olivia', password='olivia')
        request = self.client.get(action_aggregates_url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_the_relationships_user_and_task_exists(self):
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get(action_aggregates_url)
        data = request.json().get('data')
        relationships = data[0].get('relationships')
        self.assertEqual(relationships['user']['data']['id'], str(self.olivia.id))
        self.assertEqual(relationships['task']['data']['id'], str(self.task.id))


    def test_the_relationships_user_and_task_exists(self):
        action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get(action_aggregates_url)
        data = request.json().get('data')
        relationships = data[0].get('relationships')
        self.assertEqual(relationships['user']['data']['id'], str(self.olivia.id))
        self.assertEqual(relationships['task']['data']['id'], str(self.task.id))

    def test_aggregate_on_two_days(self):
        with time_machine.travel(0, tick=False) as traveller:
            action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
            traveller.shift(dt.timedelta(days=1))
            action.send(self.olivia, verb='follow', target=self.django, task_id=self.task.id)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get(action_aggregates_url)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_access_only_records_of_my_projects(self):
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task_shops.id)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),2)
        
        self.client.login(username='ruby', password='ruby')
        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),1)
       
    def test_send_only_one_action_when_aggregate_is_updated(self):
        self.client.login(username=self.olivia, password='olivia')
        request = self.client.get('/api/v1/actions/?filter[verb]=created-aggregate')
        data = request.json().get('data')
        self.assertEqual(len(data), 0)
        my_agg = ActionAggregate.objects.create( verb='reviewed',date=timezone.now(),user=self.olivia, task=self.task,count=50 )
        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),1)
        
        request = self.client.get('/api/v1/actions/?filter[verb]=created-aggregate')
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        
        my_agg.count= 60
        my_agg.save()
        
        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),1)
        
        request = self.client.get('/api/v1/actions/?filter[verb]=created-aggregate')
        data = request.json().get('data')
        self.assertEqual(len(data), 1) 
        
    def test_send_two_actions_created_aggregate_when_two_aggregates_are_created(self):
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task_shops.id)
        self.client.login(username='olivia', password='olivia')
        
        request = self.client.get(action_aggregates_url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),2)
        
        request = self.client.get('/api/v1/actions/?filter[verb]=created-aggregate')
        data = request.json().get('data')
        self.assertEqual(len(data), 2)
        
        
       
    def test_filters_on_date_range(self):
        yesterday = dt.date.today() - dt.timedelta(days=1)
        lastweek = dt.date.today() - dt.timedelta(days=7)
        lastmonth = dt.date.today() - dt.timedelta(days=30)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id, timestamp=yesterday)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task.id, timestamp=lastweek)
        action.send(self.olivia, verb='added', target=self.django, task_id=self.task_shops.id, timestamp=lastmonth)
        f = ActionAggregateFilter({'date_after': lastweek,'date_before':yesterday})
        self.assertEqual(len(f.qs),2)
            
        
        self.client.login(username='olivia', password='olivia')
        url = '/api/v1/action-aggregates/?date_after=%s&date_before=%s' % (str(lastweek),str(yesterday))
        request = self.client.get(url)
        action_aggregates = request.json().get('data')
        self.assertEqual(len(action_aggregates),2)
        
        