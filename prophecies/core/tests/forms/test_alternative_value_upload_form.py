from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from prophecies.core.forms import AlternativeValueUploadForm
from prophecies.core.models import AlternativeValue, ChoiceGroup


class AlternativeValueUploadFormTests(TestCase):
    def setUp(self):
        self.choice_group = ChoiceGroup.objects.create(name='Which country?')

    def test_is_valid(self):
        data = {"choice_group": self.choice_group.id}
        files = {'csv_file': self.build_csv_file('name,value')}
        form = AlternativeValueUploadForm(data, files)
        self.assertTrue(form.is_valid())

    def test_missing_choice_group_isnt_valid(self):
        data = {}
        files = {'csv_file': self.build_csv_file('name,value')}
        form = AlternativeValueUploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_missing_csv_file_isnt_valid(self):
        data = {"choice_group": self.choice_group.id}
        files = {}
        form = AlternativeValueUploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_wrong_choice_group_isnt_valid(self):
        data = {"choice_group": -1}
        files = {'csv_file': self.build_csv_file('name,value')}
        form = AlternativeValueUploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_wrong_csv_file_isnt_valid(self):
        data = {"choice_group": self.choice_group.id}
        files = {'csv_file': self.build_csv_file('$ù*%,;')}
        form = AlternativeValueUploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_unknown_columns_csv_file_isnt_valid(self):
        data = {"choice_group": self.choice_group.id}
        files = {'csv_file': self.build_csv_file('unknown')}
        form = AlternativeValueUploadForm(data, files)
        self.assertFalse(form.is_valid())

    def test_it_creates_two_alternative_values(self):
        data = {"choice_group": self.choice_group.id}
        csv_content = '\n'.join([
            'name,value',
            'FOO,foo',
            'BAR,bar',
        ])
        files = {'csv_file': self.build_csv_file(csv_content)}
        form = AlternativeValueUploadForm(data, files)
        form.save()
        self.assertEqual(AlternativeValue.objects.count(), 2)
        self.assertTrue(AlternativeValue.objects.filter(value='foo').exists())
        self.assertTrue(AlternativeValue.objects.filter(value='bar').exists())

    def test_it_creates_three_alternative_values(self):
        data = {"choice_group": self.choice_group.id}
        csv_content = '\n'.join([
            'name,value',
            'GREEN,green',
            'RED,red',
            'YELLOW,yellow',
        ])
        files = {'csv_file': self.build_csv_file(csv_content)}
        form = AlternativeValueUploadForm(data, files)
        form.save()
        self.assertEqual(AlternativeValue.objects.count(), 3)
        self.assertTrue(AlternativeValue.objects.filter(value='green').exists())
        self.assertTrue(AlternativeValue.objects.filter(value='red').exists())
        self.assertTrue(AlternativeValue.objects.filter(value='yellow').exists())

    def build_csv_file(self, content, filename='tmp.csv'):
        return SimpleUploadedFile(filename, bytes(content, 'utf-8'))
