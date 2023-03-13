import re

from actstream.models import Action
from django.contrib.auth.models import User

from prophecies.core.models import UserNotification


def list_mentions(content):
    """
    Returns a list of unique mentions, with their corresponding User.
    """
    usernames = re.findall("@([a-zA-Z0-9]{1,15})", str(content))
    if len(usernames) > 1:
        # Create a list of unique usernames
        usernames = list(dict.fromkeys(usernames))
    mentions = []
    for username in usernames:
        user = User.objects.filter(username=username).first()
        mentions.append({'mention': username, 'user': user})
    return mentions


def get_or_create_mention_action(actor, target, action_object, data={}):
    """
    Get or create the action matching with the given target's mention
    """
    if not actor or not target:
        return [None, False]
    actor_params = Action.objects.filter_actor_params(actor)
    target_params = Action.objects.filter_target_params(target)
    action_object_params = Action.objects.filter_action_object_params(action_object)
    verb_params = {'verb': 'mentioned', 'data': data}
    params = {**verb_params, **actor_params, **target_params, **action_object_params}
    return Action.objects.get_or_create(**params)


def mentioned(text, object_type):
    return re.findall(f'(?i)@{object_type}', str(text))


def notify_mentioned_users(author, users, action_object):
    for user in users:
        if author != user:
            action, created = get_or_create_mention_action(author, user, action_object)
            if created:
                UserNotification.objects.create(recipient=user, action=action)
