from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.http import urlencode
from social_core.backends.oauth import BaseOAuth2


class XemxOauth2(BaseOAuth2):
    name = 'xemx'
    AUTHORIZATION_URL = '%s/oauth/authorize' % settings.SOCIAL_AUTH_XEMX_HOSTNAME
    ACCESS_TOKEN_URL = '%s/oauth/token' % settings.SOCIAL_AUTH_XEMX_HOSTNAME
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','

    def user_data(self, access_token, *args, **kwargs):
        params = urlencode({ 'access_token': access_token })
        url = ('%s/api/v1/me.json?' % settings.SOCIAL_AUTH_XEMX_HOSTNAME) + params
        return self.get_json(url)

    def get_user_details(self, response):
        try:
            first_name, last_name = response.get('name').split(' ', 1)
        except ValueError:
            first_name = response.get('name', '')
            last_name = ''
        return {
            'username': response.get('uid'),
            'email': response.get('email') or '',
            'first_name': first_name,
            'last_name': last_name,
            'xemx_groups': response.get('groups_by_applications', {}).get('prophecies', []),
        }


def map_xemx_groups(strategy, details, user=None, *args, **kwargs):
    if not user:
        return
    # All Xemx user are "staff"
    user.is_staff = 'icijstaff' in details['xemx_groups']
    user.save()
    # Get groups ids with the same name
    group_ids = Group.objects.filter(name__in=details['xemx_groups']).values_list('id', flat=True)

    # DON'T Replace all existings groups, only add
    # user.groups.set(group_ids)
    for gid in group_ids:
        try:
            user.groups.add(gid)
        except Exception as e:
            print("Trying to add group {} to user {}: ".format(gid, user))
            print(e)
