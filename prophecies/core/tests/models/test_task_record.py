from django.test import TestCase
from prophecies.core.models import Project, Task, TaskRecord
from prophecies.core.models.task import Task

class TestTaskRecord(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='FinCEN Files')


    def test_it_should_use_task_record_link(self):
        task = Task.objects.create(name='Addresses', project=self.project)
        task_record = TaskRecord.objects.create(task=task, link='https://offshoreleaks.icij.org', original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://offshoreleaks.icij.org')


    def test_it_should_ignore_task_link_template(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={original_value}')
        task_record = TaskRecord.objects.create(task=task, link='https://offshoreleaks.icij.org', original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://offshoreleaks.icij.org')


    def test_it_should_use_task_link_template(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={original_value}')
        task_record = TaskRecord.objects.create(task=task, original_value='foo')
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=foo')


    def test_it_should_use_task_link_template_with_metadata(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata.foo}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": "Paris"})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Paris')


    def test_it_should_use_task_link_template_with_nested_metadata(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata.foo.bar}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": {"bar": "Paris"}})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Paris')


    def test_it_should_use_task_link_template_with_nested_list(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata.foo.bar[1]}')
        task_record = TaskRecord.objects.create(task=task, metadata={"foo": {"bar": ["Paris", "London"]}})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')


    def test_it_should_use_task_link_template_with_canonical_string(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata}')
        task_record = TaskRecord.objects.create(task=task, metadata="London")
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')


    def test_it_should_use_task_link_template_with_a_list(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata[1]}')
        task_record = TaskRecord.objects.create(task=task, metadata=["Paris", "London"])
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')


    def test_it_should_use_task_link_template_with_a_list_of_objects(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata[1].city}')
        task_record = TaskRecord.objects.create(task=task, metadata=[{"city": "Paris"},{"city": "London" }])
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=London')


    def test_it_should_use_task_link_template_with_urlencored_original_value(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={original_value:u}')
        task_record = TaskRecord.objects.create(task=task, original_value='Kuala Lumpur')
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Kuala%20Lumpur')


    def test_it_should_use_task_link_template_with_urlencored_metadata_field(self):
        task = Task.objects.create(name='Addresses', project=self.project, recordLinkTemplate='https://www.openstreetmap.org/search?query={metadata.city:u}')
        task_record = TaskRecord.objects.create(task=task, metadata={'city': 'Kuala Lumpur'})
        self.assertEqual(task_record.computed_link(), 'https://www.openstreetmap.org/search?query=Kuala%20Lumpur')
