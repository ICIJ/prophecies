from django.test import TestCase
from prophecies.core.contrib.namespace import ExtendedNamespace

class TestNamespace(TestCase):


    def test_it_get_simple_value(self):
        ns = ExtendedNamespace({'foo': 'bar'})
        self.assertEqual(ns.foo, 'bar')


    def test_it_get_nested_value(self):
        ns = ExtendedNamespace({'foo': {'bar': 'baz'}})
        self.assertEqual(ns.foo.bar, 'baz')


    def test_it_get_nested_list(self):
        ns = ExtendedNamespace({'foo': {'bar': ['baz']}})
        self.assertEqual(ns.foo.bar[0], 'baz')


    def test_it_get_nested_list_with_property(self):
        ns = ExtendedNamespace({'foo': {'bar': [{'baz': 'qux'}]}})
        self.assertEqual(ns.foo.bar[0].baz, 'qux')


    def test_it_get_list(self):
        ns = ExtendedNamespace(['baz'])
        self.assertEqual(ns[0], 'baz')


    def test_it_get_list_with_nested_property(self):
        ns = ExtendedNamespace([{'foo': 'baz'}])
        self.assertEqual(ns[0].foo, 'baz')


    def test_it_get_list_with_nested_list(self):
        ns = ExtendedNamespace([{'foo': ['baz', 'bar', 'qux']}])
        self.assertEqual(ns[0].foo[2], 'qux')
