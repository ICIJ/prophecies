import string
import urllib.parse


class URLEncodedFormatter(string.Formatter):

    def format_field(self, value, spec):
        if spec.endswith('u'):
            value = urllib.parse.quote(value)
            spec = spec[:-1] + 's'
        return super().format_field(value, spec)

    def get_value(self, *kwarg):
        try:
            return super().get_value(*kwarg)
        except KeyError:
            return ''

    def get_field(self, *kwarg):
        try:
            return super().get_field(*kwarg)
        except AttributeError:
            return ('', '')
