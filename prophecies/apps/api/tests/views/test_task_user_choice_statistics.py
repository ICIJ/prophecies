from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from prophecies.core.models import Project, Task, TaskRecord, TaskRecordReview, ChoiceGroup, Choice


class TestTaskUserChoiceStatistics(TestCase):
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
        # Add Olivia and Django to the Painting task
        self.paintings = Task.objects.create(name="paintings", project=project, choice_group=choice_group)
        self.paintings.checkers.add(self.olivia)
        self.paintings.checkers.add(self.django)
        # Add a record
        self.task_record_of_paintings_foo = TaskRecord.objects.create(original_value="foo", task=self.paintings)
        self.task_record_of_paintings_bar = TaskRecord.objects.create(original_value="bar", task=self.paintings)

    def test_it_returns_count_for_a_choice_olivia_made_on_a_task(self):
        choice1 = self.paintings.choice_group.choices.first()
        
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1, choice=choice1)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('attributes').get('count'),1)
        
    def test_it_returns_stats_for_two_rounds(self):
        choice = self.paintings.choice_group.choices.first()
        
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1, choice=choice)
        TaskRecordReview.objects.get_or_create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=2, choice=choice)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        self.assertEqual(request.status_code, 200)
        data = request.json().get('data')
        self.assertEqual(len(data), 2)
        #round1
        self.assertEqual(data[0].get('attributes').get('count'),1)
        #round2
        self.assertEqual(data[1].get('attributes').get('count'),1)
        
    def test_it_updates_counts_when_olivia_changes_her_mind_on_the_same_review(self):
        choice1 = self.paintings.choice_group.choices.first()
        choice2 = self.paintings.choice_group.choices.all()[1]
        
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1, choice=choice1)
        
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('relationships').get('choice').get('data').get('id'),str(choice1.id))
        self.assertEqual(data[0].get('attributes').get('count'),1)
        
        trr,_=TaskRecordReview.objects.get_or_create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1)
        trr.choice=choice2
        trr.save()
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('relationships').get('choice').get('data').get('id'),str(choice2.id))
        self.assertEqual(data[0].get('attributes').get('count'),1)



    def test_it_returns_a_count_of_two_when_olivia_use_twice_same_choice_on_same_round(self):
        choice = self.paintings.choice_group.choices.first()
        
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1, choice=choice)
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_bar, checker=self.olivia, round=1, choice=choice)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('relationships').get('choice').get('data').get('id'),str(choice.id))
        self.assertEqual(data[0].get('attributes').get('count'),2)

    def test_it_returns_no_stats_if_olivia_cancel_her_review(self):
        choice = self.paintings.choice_group.choices.first()
        
        TaskRecordReview.objects.create(task_record=self.task_record_of_paintings_foo, checker=self.olivia, round=1, choice=choice)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/task-user-choice-statistics/')
        data = request.json().get('data')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('relationships').get('choice').get('data').get('id'),str(choice.id))
        self.assertEqual(data[0].get('attributes').get('count'),2)
        
        