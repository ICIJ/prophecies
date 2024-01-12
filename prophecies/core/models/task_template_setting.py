from django.db import models
from django.db.models.fields.related import RelatedField
from polymorphic.models import PolymorphicModel


class TaskTemplateSetting(PolymorphicModel):

    """
    Abstract base class for task template settings, using PolymorphicModel
    to allow for different types of template settings.
    """

    def __str__(self):
        if self.__class__ == TaskTemplateSetting:
            return f"Template settings #{self.id}"
        return f"{self.for_type} template settings"

    @property
    def for_type(self):
        if self.__class__ == TaskTemplateSetting:
            return None
        class_name = self.__class__.__name__
        type_name = class_name.rsplit("For", maxsplit=1)[-1]
        return type_name.capitalize() or None

    @classmethod
    def copyable_fields(cls):
        """
        Class method to get the names of fields that can be copied from one
        instance to another.

        Returns:
            list: A list of field names that can be copied.
        """

        def is_field(f):
            return isinstance(f, models.Field)

        def is_related(f):
            return isinstance(f, RelatedField)

        def is_primitive(f):
            return is_field(f) and not is_related(f)

        def is_own(f):
            return f.model is not TaskTemplateSetting

        def is_valid(f):
            return is_primitive(f) and is_own(f)

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
            self.delete()
        return target, save

    def convert_to(self, cls, save=True):
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
        return self.copy_to(cls(), save)


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
