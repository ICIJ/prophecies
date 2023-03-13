from django.test import TestCase

from prophecies.core.models.setting import Setting, SettingVisibility


class TestSetting(TestCase):

    def test_a_setting_is_private_by_default(self):
        self.assertTrue(Setting.objects.create(key='foo').private)

    def test_a_setting_is_not_public_by_default(self):
        self.assertFalse(Setting.objects.create(key='foo').public)

    def test_a_setting_can_be_published(self):
        foo = Setting.objects.create(key='bar')
        foo.publish()
        self.assertTrue(foo.public)

    def test_a_setting_can_be_unpublished(self):
        foo = Setting.objects.create(key='fuz')
        visibility = SettingVisibility.objects.create(setting=foo, public=True)
        self.assertTrue(foo.public)
        foo.unpublish()
        self.assertFalse(foo.public)

    def test_a_setting_can_be_published_using_a_setter(self):
        foo = Setting.objects.create(key='fuz')
        foo.public = True
        self.assertTrue(foo.public)

    def test_a_setting_can_be_unpublished_using_a_setter(self):
        foo = Setting.objects.create(key='fuz')
        visibility = SettingVisibility.objects.create(setting=foo, public=True)
        foo.public = False
        self.assertFalse(foo.public)

    def test_a_setting_can_be_published_using_a_setter_without_saving(self):
        foo = Setting.objects.create(key='fuz')
        foo.public = True
        foo.refresh_from_db()
        self.assertFalse(foo.public)

    def test_a_setting_can_be_published_using_a_setter_and_persisted_after_save(self):
        foo = Setting.objects.create(key='fuz')
        foo.public = True
        foo.save()
        foo.refresh_from_db()
        self.assertTrue(foo.public)
