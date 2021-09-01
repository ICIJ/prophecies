import re
from actstream.models import Action
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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
        mentions.append({ 'mention': username, 'user': user })
    return mentions

def get_or_create_mention_action(actor, target, action_object):
    """
    Get or create the action matching with the given target's mention
    """
    actor_content_type = ContentType.objects.get_for_model(actor)
    target_object_content_type = ContentType.objects.get_for_model(target)
    action_object_content_type = ContentType.objects.get_for_model(action_object)
    return Action.objects.get_or_create(verb='mentioned',
        actor_content_type=actor_content_type,
        actor_object_id=actor.id,
        target_content_type=target_object_content_type,
        target_object_id=target.id,
        action_object_content_type=action_object_content_type,
        action_object_object_id=action_object.id)
