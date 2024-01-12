from django.test import TestCase
from prophecies.core.models import Task, Project
from prophecies.core.models.task_template_setting import (
    TaskTemplateSettingForText as ForText,
    TaskTemplateSettingForMedia as ForMedia,
    TaskTemplateSettingForIframe as ForIframe,
)


class TaskTemplateSettingTest(TestCase):
    def setUp(self):
        self.pencil_papers = Project.objects.create(name="Pencil Papers")
        self.art = Task.objects.create(name="Art", project=self.pencil_papers)
        self.setting_media = ForMedia.objects.create(max_width=10)

    def test_copyable_fields(self):
        fields = ForMedia.copyable_fields()
        self.assertIsInstance(fields, list)
        self.assertTrue('max_width' in fields)

    def test_copy_to(self):
        new_setting = ForMedia()
        copied_setting, _ = self.setting_media.copy_to(new_setting, save=False)
        self.assertEqual(copied_setting.max_width, 10)

    def test_convert_to(self):
        converted_setting, _ = self.setting_media.convert_to(ForMedia)
        self.assertEqual(converted_setting.max_width, 10)
        self.assertIsInstance(converted_setting, ForMedia)
