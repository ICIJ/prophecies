from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.http import urlencode
from social_core.backends.oauth import BaseOAuth2

from prophecies.core.contrib.namespace import get_path


class OAuth2Provider(BaseOAuth2):
    name = 'provider'
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_PROVIDER_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = settings.SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_METHOD
    SCOPE_SEPARATOR = ','

    def user_data(self, access_token, *args, **kwargs):
        params = urlencode({'access_token': access_token})
        url = settings.SOCIAL_AUTH_PROVIDER_PROFILE_URL + params
        return self.get_json(url)

    def get_user_details(self, response):
        try:
            first_name, last_name = response.get('name').split(' ', 1)
        except ValueError:
            first_name = response.get('name', '')
            last_name = ''
        return {
            'username': get_path(response, settings.SOCIAL_AUTH_PROVIDER_USERNAME_FIELD),
            'email': response.get('email') or '',
            'first_name': first_name,
            'last_name': last_name,
            'provider_groups': get_path(response, settings.SOCIAL_AUTH_PROVIDER_GROUPS_FIELD, []),
        }


def map_provider_groups(strategy, details, user=None, *args, **kwargs):
    if not user:
        return
    user.is_staff = settings.SOCIAL_AUTH_PROVIDER_STAFF_GROUP in details['provider_groups']
    user.save()
    # Get groups ids with the same name
    group_ids = Group.objects.filter(name__in=details['provider_groups']).values_list('id', flat=True)
    # DON'T Replace all existings groups, only add
    # user.groups.set(group_ids)
    for gid in group_ids:
        try:
            user.groups.add(gid)
        except Exception as e:
            print("Trying to add group {} to user {} failed.".format(gid, user))
