from actstream.models import Action
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LevelType(models.TextChoices):
    INFO = 'INFO', _('Info')
    ERROR = 'ERROR', _('Error')
    SUCCESS = 'SUCCESS', _('Success')
    WARNING = 'WARNING', _('Warning')


class UserNotificationQuerySet(models.QuerySet):

    def read(self):
        """
        Return only read items.
        """
        return self.filter(read=True)

    def unread(self):
        """
        Return only unread items.
        """
        return self.filter(read=False)

    def mark_as_read(self):
        """
        Mark as read any unread messages in the current queryset.
        """
        return self.unread().update(read=True)

    def user_scope(self, user):
        return self.filter(recipient=user)


class UserNotificationManager(models.Manager):

    def read(self):
        """
        Return only read items.
        """
        return self.get_queryset().read()

    def unread(self):
        """
        Return only unread items.
        """
        return self.get_queryset().unread()

    def mark_as_read(self):
        """
        Mark as read any unread messages in the current queryset.
        """
        return self.get_queryset().mark_as_read()

    def user_scope(self, user):
        return self.get_queryset().user_scope(user)

    def get_queryset(self) -> UserNotificationQuerySet:
        return UserNotificationQuerySet(model=self.model, using=self._db, hints=self._hints)


class UserNotification(models.Model):
    objects = UserNotificationManager()

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    level = models.CharField(blank=True, choices=LevelType.choices, default=LevelType.INFO, max_length=7)
    description = models.CharField(max_length=100, blank=True, null=True)
    read = models.BooleanField(default=False, blank=False, db_index=True)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("recipient_id", "action_id"),)

    def mark_as_read(self):
        self.read = True
        self.save()

    def save(self, *args, **kwargs):
        if self.read and self.read_at is None:
            self.read_at = timezone.now()
        super().save(*args, **kwargs)
