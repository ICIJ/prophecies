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
        self.setting_text = ForText.objects.create(task=self.art)
        self.setting_media = ForMedia.objects.create(task=self.art, max_width=10)
        self.setting_iframe = ForIframe.objects.create(task=self.art, max_width=20)

    def test_copyable_fields(self):
        fields = ForText.copyable_fields()
        self.assertIsInstance(fields, list)

    def test_copy_to(self):
        new_setting = ForMedia()
        copied_setting = self.setting_media.copy_to(new_setting, save=False)
        self.assertEqual(copied_setting.max_width, 10)

    def test_convert_to(self):
        converted_setting = self.setting_media.convert_to(ForMedia)
        self.assertEqual(converted_setting.max_width, 10)
        self.assertIsInstance(converted_setting, ForMedia)

    def test_convert_or_create_false_with_existing_task(self):
        iframe_setting, created = self.setting_media.convert_or_create(ForIframe)
        self.assertFalse(created)
        self.assertEqual(iframe_setting.max_width, 10)

    def test_convert_or_create_true_with_new_task(self):
        shop = Task.objects.create(name="Shop", project=self.pencil_papers)
        setting_text = ForText.objects.create(task=shop)
        _, created = setting_text.convert_or_create(ForIframe)
        self.assertTrue(created)
