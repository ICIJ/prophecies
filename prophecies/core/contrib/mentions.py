import re
from django.contrib.auth.models import User

def list_mentions(content):
    """
    Returns a list of unique mentions, with their corresponding User.
    """
    usernames = re.findall("@([a-zA-Z0-9]{1,15})", content)
    if len(usernames) > 1:
        # Create a list of unique usernames
        usernames = list(dict.fromkeys(usernames))
    mentions = []
    for username in usernames:
        user = User.objects.filter(username=username).first()
        mentions.append({ 'mention': username, 'user': user })
    return mentions
