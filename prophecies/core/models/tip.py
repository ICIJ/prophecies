from actstream import action
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from prophecies.core.models import Project, Task, UserNotification
from prophecies.core.contrib.mentions import list_mentions, get_or_create_mention_action, mentioned, notify_mentioned_users


class TipQuerySet(models.QuerySet):

    def general(self):
        return self.filter(task_id__isnull=True, project_id__isnull=True).distinct().all()
    
    def general_in_project(self):
        return self.filter(task_id__isnull=True, project_id__isnull=False).distinct().all()

    def user_scope(self, user):
        return self.filter(task__checkers=user).distinct().all() | self.general() | self.general_in_project()
    
    
class TipManager(models.Manager):
    
    def general(self):
        return self.get_queryset().general()
    
    def general_in_project(self):
        return self.get_queryset().general_in_project()

    def user_scope(self, user):
        return self.get_queryset().user_scope(user)
    
    def get_queryset(self) -> TipQuerySet:
        return TipQuerySet(model=self.model, using=self._db, hints=self._hints)


class Tip(models.Model):
    objects = TipManager()

    name = models.CharField(max_length=100, verbose_name="Tip name", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        if not self.name:
            return 'untitled tip'
        return self.name


    @property
    def mentions(self):
        """
        Returns a list of unique mentions, with their corresponding User.
        """
        return list_mentions(self.description)


    @property
    def mentioned_project(self):
        if mentioned(self.description, 'project'):
            try:
                return self.project
            except AttributeError:
                return None


    @property
    def mentioned_task(self):
        if mentioned(self.description, 'task'):
            try:
                return self.task
            except AttributeError:
                return None


    @staticmethod
    def signal_notify_mentioned_users(sender, instance, **kwargs):
        for mention in instance.mentions:
            user = mention.get('user')
            if user is not None:
                action, created = get_or_create_mention_action(instance.creator, user, instance)
                if created:
                    UserNotification.objects.create(recipient=user, action=action)


    @staticmethod
    def signal_notify_members_in_mentioned_project(sender, instance, **kwargs):
        project = instance.mentioned_project
        if project is not None:
            notify_mentioned_users(instance.creator, project.members, instance)


    @staticmethod
    def signal_notify_task_checkers_in_mentioned_task(sender, instance, **kwargs):
        task = instance.mentioned_task
        if task is not None:
            notify_mentioned_users(instance.creator, task.checkers.all(), instance)

    
    @staticmethod
    def signal_fill_project_from_task(sender, instance, **kwargs):
        if not instance.project and instance.task:
            instance.project = instance.task.project
    
    @staticmethod
    def signal_constraint_task_relationship_to_project(sender, instance, **kwargs):
        if instance.project and instance.task and instance.project != instance.task.project:
            instance.task = None
    
    @staticmethod
    def signal_tip_creation(sender, instance, created,**kwargs):
        if instance.creator:
            if created :
                action.send(instance.creator, verb='tip-created', data=instance.name, target=instance)
            else:
                action.send(instance.creator, verb='tip-updated', data=instance.name, target=instance)

signals.pre_save.connect(Tip.signal_fill_project_from_task, sender=Tip)
signals.pre_save.connect(Tip.signal_constraint_task_relationship_to_project, sender=Tip)
signals.post_save.connect(Tip.signal_notify_mentioned_users, sender=Tip)
signals.post_save.connect(Tip.signal_notify_members_in_mentioned_project, sender=Tip)
signals.post_save.connect(Tip.signal_notify_task_checkers_in_mentioned_task, sender=Tip)
signals.post_save.connect(Tip.signal_tip_creation, sender=Tip)
