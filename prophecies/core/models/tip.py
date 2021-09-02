from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from prophecies.core.models import Project, Task, UserNotification
from prophecies.core.contrib.mentions import list_mentions, get_or_create_mention_action

class Tip(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tip name", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def mentions(self):
        """
        Returns a list of unique mentions, with their corresponding User.
        """
        return list_mentions(self.description)

    @staticmethod
    def signal_notify_mentioned_users(sender, instance, **kwargs):
        for mention in instance.mentions:
            user = mention.get('user')
            if user is not None:
                action, created = get_or_create_mention_action(instance.creator, user, instance)
                if created:
                    UserNotification.objects.create(recipient=user, action=action)


signals.post_save.connect(Tip.signal_notify_mentioned_users, sender=Tip)
