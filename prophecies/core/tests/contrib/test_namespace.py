from django.test import TestCase
from prophecies.core.contrib.namespace import ExtendedNamespace, get_path

class TestNamespace(TestCase):


    def test_it_gets_simple_value(self):
        ns = ExtendedNamespace({'foo': 'bar'})
        self.assertEqual(ns.foo, 'bar')


    def test_it_gets_nested_value(self):
        ns = ExtendedNamespace({'foo': {'bar': 'baz'}})
        self.assertEqual(ns.foo.bar, 'baz')


    def test_it_gets_nested_list(self):
        ns = ExtendedNamespace({'foo': {'bar': ['baz']}})
        self.assertEqual(ns.foo.bar[0], 'baz')


    def test_it_gets_nested_list_with_property(self):
        ns = ExtendedNamespace({'foo': {'bar': [{'baz': 'qux'}]}})
        self.assertEqual(ns.foo.bar[0].baz, 'qux')


    def test_it_gets_list(self):
        ns = ExtendedNamespace(['baz'])
        self.assertEqual(ns[0], 'baz')


    def test_it_gets_list_with_nested_property(self):
        ns = ExtendedNamespace([{'foo': 'baz'}])
        self.assertEqual(ns[0].foo, 'baz')


    def test_it_gets_list_with_nested_list(self):
        ns = ExtendedNamespace([{'foo': ['baz', 'bar', 'qux']}])
        self.assertEqual(ns[0].foo[2], 'qux')


    def test_it_gets_path_on_list(self):
        obj = [0, 1, 2]
        self.assertEqual(get_path(obj, 1), 1)
        self.assertEqual(get_path(obj, 2), 2)


    def test_it_gets_default_on_list(self):
        obj = [0, 1, 2]
        self.assertEqual(get_path(obj, 10, 10), 10)


    def test_it_gets_path_on_dict(self):
        obj = {'a': 0, 'b': 1, 'c': 2}
        self.assertEqual(get_path(obj, 'a'), 0)
        self.assertEqual(get_path(obj, 'b'), 1)


    def test_it_gets_default_on_dict(self):
        obj = {'a': 0, 'b': 1, 'c': 2}
        self.assertEqual(get_path(obj, 'd', 3), 3)


    def test_it_gets_path_on_nested_list(self):
        obj = {'a': {'b': {'c': [0, 1, 2]}}}
        self.assertEqual(get_path(obj, 'a.b.c.2'), 2)


    def test_it_gets_path_on_nested_dict(self):
        obj = {'a': {'b': {'c': 2}}}
        self.assertEqual(get_path(obj, 'a.b.c'), 2)


    def test_it_gets_default_on_nested_list(self):
        obj = {'a': {'b': {'c': [0, 1, 2]}}}
        self.assertEqual(get_path(obj, 'a.b.c.10', 10), 10)


    def test_it_gets_default_on_nested_dict(self):
        obj = {'a': {'b': {'c': 2}}}
        self.assertEqual(get_path(obj, 'a.b.c.d', 3), 3)


    def test_it_gets_default_on_int(self):
        obj = 10
        self.assertEqual(get_path(obj, 'a.b.c.d', 3), 3)


    def test_it_gets_default_on_string(self):
        obj = 'foo'
        self.assertEqual(get_path(obj, 'a.b.c.d', 3), 3)
