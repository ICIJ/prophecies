from django.contrib.auth.models import User
from django.test import TestCase

from prophecies.core.forms.task_form import TaskForm
from prophecies.core.models import Project, Task, ChoiceGroup, TaskRecord, TaskRecordReview


class TaskFormTests(TestCase):

    def setUp(self):
        self.olivia = User.objects.create(username='olivia')
        self.project = Project.objects.create(name='Pencil Papers')
        self.correctness = ChoiceGroup.objects.create(name='Is it correct?')
        self.colorness = ChoiceGroup.objects.create(name='Is it red or blue?')
        self.task = Task.objects.create(name='Art', project=self.project, description="toto", color='#fe6565', rounds=2)
        self.task_record_blue = TaskRecord.objects.create(original_value='blue', task=self.task)
        self.task.checkers.add(self.olivia)
        self.data = TaskForm(instance=self.task).initial

    def test_form_is_valid(self):
        data = TaskForm(instance=self.task).initial
        form = TaskForm(data=data, instance=self.task)
        self.assertEqual(form.instance, self.task)
        self.assertTrue(form.is_valid())

    def test_select_choice_group_for_the_first_time(self):
        self.task.choice_group = None
        data = TaskForm(instance=self.task).initial
        form = TaskForm(data=data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()

        data['choice_group'] = self.correctness
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())

    def test_allow_change_choice_group_when_the_task_has_no_review(self):
        self.task.choice_group = self.correctness
        data = TaskForm(instance=self.task).initial
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()

        data['choice_group'] = self.colorness
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()

        data['choice_group'] = self.correctness
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()

    def test_prevent_change_choice_group_when_the_task_has_reviews(self):
        TaskRecordReview.objects.create(task_record=self.task_record_blue)
        self.task.choice_group = self.correctness
        data = TaskForm(instance=self.task).initial
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()

        data['choice_group'] = self.colorness
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.fields['choice_group'].disabled)
        self.assertTrue(form.is_valid())

        data['choice_group'] = self.correctness
        form = TaskForm(data, instance=self.task)
        self.assertTrue(form.is_valid())
        form.save()
