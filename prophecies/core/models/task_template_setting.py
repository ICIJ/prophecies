from django.db import models
from django.db.models.fields.related import RelatedField
from polymorphic.models import PolymorphicModel
from prophecies.core.models.task import Task


class TaskTemplateSetting(PolymorphicModel):
    """
    Abstract base class for task template settings, using PolymorphicModel
    to allow for different types of template settings.
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        related_name="template_setting",
    )

    class Meta:
        unique_together = (
            "task_id",
            "polymorphic_ctype",
        )

    def __str__(self):
        if not self.task:
            return "Template settings"
        if not issubclass(self.__class__, TaskTemplateSetting):
            return f"Template settings for {self.task} task"
        return f"{self.for_type} template settings for {self.task} task"

    @property
    def for_type(self):
        if not issubclass(self.__class__, TaskTemplateSetting):
            return None
        return self.__class__.__name__.split("TaskTemplateSettingFor")[-1].capitalize()

    @classmethod
    def copyable_fields(cls):
        """
        Class method to get the names of fields that can be copied from one
        instance to another.

        Returns:
            list: A list of field names that can be copied.
        """
        is_field = lambda f: isinstance(f, models.Field)
        is_related = lambda f: isinstance(f, RelatedField)
        is_primitive = lambda f: is_field(f) and not is_related(f)
        is_own = lambda f: f.model is not TaskTemplateSetting
        is_valid = lambda f: is_primitive(f) and is_own(f)
        return [f.name for f in cls._meta.get_fields() if is_valid(f)]

    def copy_to(self, target, save=True):
        """
        Copies the values of the copyable fields from this instance to the target instance.

        Args:
            target (TaskTemplateSetting): The target instance where the fields should be copied to.
            save (bool): If True, the target instance is saved after copying the fields.

        Returns:
            TaskTemplateSetting: The target instance after copying the fields.
        """
        for field in target.copyable_fields():
            if field in self.copyable_fields():
                setattr(target, field, getattr(self, field))
        if save:
            target.save()
        return target

    def convert_to(self, cls):
        """
        Converts this instance to an instance of the given TaskTemplateSetting subclass.

        Args:
            cls (TaskTemplateSetting): The subclass to which this instance should be converted.

        Raises:
            ValueError: If the given class is not a subclass of TaskTemplateSetting.

        Returns:
            TaskTemplateSetting: A new instance of the given subclass with copied fields.
        """
        if not issubclass(cls, TaskTemplateSetting):
            raise ValueError(f"Cannot convert to {cls.__class__.__name__}")
        return self.copy_to(cls())

    def convert_or_create(self, cls, delete=True):
        """
        Converts this instance to an instance of the given subclass, or creates a new instance if not existing.

        Args:
            cls (TaskTemplateSetting): The subclass to which this instance should be converted or created.
            delete (bool): If True, this instance is deleted after conversion.

        Returns:
            tuple: A tuple containing the new or found instance and a boolean indicating if it was created.
        """
        new_instance, created = cls.objects.get_or_create(task=self.task)
        new_instance = self.copy_to(new_instance)
        if delete:
            self.delete()
        return (new_instance, created)


class TaskTemplateSettingForText(TaskTemplateSetting):
    """
    TaskTemplateSetting subclass for text-related settings.
    """


class TaskTemplateSettingForMedia(TaskTemplateSetting):
    """
    TaskTemplateSetting subclass for media-related settings,
    with additional fields for media dimensions and display preferences.
    """

    max_width = models.IntegerField(null=True, blank=True)
    max_height = models.IntegerField(null=True, blank=True)
    display_original_value = models.BooleanField(default=True)


class TaskTemplateSettingForIframe(TaskTemplateSetting):
    """
    TaskTemplateSetting subclass for iframe-related settings, similar to media settings.
    """

    max_width = models.IntegerField(null=True, blank=True)
    max_height = models.IntegerField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)
    display_original_value = models.BooleanField(default=True)
