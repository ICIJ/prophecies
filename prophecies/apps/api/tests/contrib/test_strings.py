from django.test import TestCase
from prophecies.apps.api.contrib.strings import to_camel_case

class TestStrings(TestCase):

    def test_it_convert_snake_case_to_camel_case(self):
        str = to_camel_case('foo_bar')
        self.assertEqual(str, 'fooBar')

    def test_it_convert_uppercase_to_camel_case(self):
        str = to_camel_case('FOO_BAR')
        self.assertEqual(str, 'fooBar')

    def test_it_convert_single_uppercase_word_to_camel_case(self):
        str = to_camel_case('FOO')
        self.assertEqual(str, 'foo')

    def test_it_convert_single_lower_word_to_camel_case(self):
        str = to_camel_case('foo')
        self.assertEqual(str, 'foo')

    def test_it_convert_dot_words_to_camel_case(self):
        str = to_camel_case('foo.bar')
        self.assertEqual(str, 'fooBar')

    def test_it_convert_space_words_to_camel_case(self):
        str = to_camel_case('foo BAR')
        self.assertEqual(str, 'fooBar')

    def test_it_convert_kebad_case_to_camel_case(self):
        str = to_camel_case('foo-bar-baz')
        self.assertEqual(str, 'fooBarBaz')
