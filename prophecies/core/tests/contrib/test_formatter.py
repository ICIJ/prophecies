from django.test import TestCase
from prophecies.core.contrib.formatter import URLEncodedFormatter

class TestFormatter(TestCase):


    def test_u_converter_urlencodes_value(self):
        formatter = URLEncodedFormatter()
        link = formatter.format('https://duckduckgo.com/?q={0:u}', 'Kuala Lumpur')
        self.assertEqual(link, 'https://duckduckgo.com/?q=Kuala%20Lumpur')


    def test_it_doesnt_urlencodes_value_by_default(self):
        formatter = URLEncodedFormatter()
        link = formatter.format('https://duckduckgo.com/?q={0}', 'Kuala Lumpur')
        self.assertEqual(link, 'https://duckduckgo.com/?q=Kuala Lumpur')


    def test_unkown_fields_are_ignored(self):
        formatter = URLEncodedFormatter()
        link = formatter.format('https://duckduckgo.com/?q={foo}', bar=1)
        self.assertEqual(link, 'https://duckduckgo.com/?q=')


    def test_unkown_field_attributes_are_ignored(self):
        formatter = URLEncodedFormatter()
        link = formatter.format('https://duckduckgo.com/?q={foo.qux}', bar=1)
        self.assertEqual(link, 'https://duckduckgo.com/?q=')
