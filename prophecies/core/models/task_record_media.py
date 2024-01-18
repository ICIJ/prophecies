from pathlib import Path
from django.db import models
from django.db.models import signals
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext_lazy as _

import magic

from prophecies.core.models import Task, TaskRecord
from prophecies.core.validators.task_record_media import MimeTypeValidator


def task_record_media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/task/<id>/<filename>
    return f"task/{instance.task.id}/{filename}"


class TaskRecordMediaManager(models.Manager):
    def user_scope(self, user):
        return self.filter(task_record__task__in=user.task.all())


class TaskRecordMedia(models.Model):
    objects = TaskRecordMediaManager()

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="task_record_medias"
    )
    task_record = models.ForeignKey(
        TaskRecord,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="medias",
    )
    file = models.FileField(
        blank=False,
        max_length=500,
        validators=[MimeTypeValidator()],
        upload_to=task_record_media_directory_path,
    )
    uid = models.CharField(blank=False, max_length=500)
    mime_type = models.CharField(blank=False, max_length=128)
    height = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MediaType(models.TextChoices):
        IMAGE = "IMAGE", _("Image (jpg, png, gif, ...)")
        VIDEO = "VIDEO", _("Video (mp4, avi, mov, ...)")

    SUPPORTED_MIME_TYPES = {
        MediaType.IMAGE: (
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/svg+xml",
            "image/webp",
        ),
        MediaType.VIDEO: (
            "video/x-msvideo",
            "video/mp4",
            "video/mpeg",
            "video/ogv",
            "video/webm",
        ),
    }

    @property
    def media_type(self):
        return TaskRecordMedia.mime_to_media_type(self.mime_type)

    @property
    def file_preview_url(self):
        if self.file and self.media_type == TaskRecordMedia.MediaType.IMAGE:
            return f"{self.file.url}"
        return None

    @staticmethod
    def mime_to_media_type(mime_type):
        for key, mime_list in TaskRecordMedia.SUPPORTED_MIME_TYPES.items():
            if mime_type in mime_list:
                return key
        return None

    @staticmethod
    def file_to_media_type(file):
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        return TaskRecordMedia.mime_to_media_type(mime_type)

    @staticmethod
    def mime_types():
        values = TaskRecordMedia.SUPPORTED_MIME_TYPES.values()
        return [mime for types in values for mime in types]

    @staticmethod
    # pylint: disable-next=unused-argument
    def signal_fill_uid(sender, instance, **kwargs):
        instance.uid = instance.uid or Path(instance.file.name).stem

    @staticmethod
    # pylint: disable-next=unused-argument
    def signal_fill_mime_type(sender, instance, **kwargs):
        if instance.file:
            instance.file.seek(0)
            instance.mime_type = magic.from_buffer(instance.file.read(1024), mime=True)

    @staticmethod
    # pylint: disable-next=unused-argument
    def signal_fill_task_record(sender, instance, **kwargs):
        if instance.uid and instance.task_id is not None and instance.task_record_id is None:
            instance.task_record = instance.task.records.filter(
                uid=instance.uid
            ).first()

    @staticmethod
    # pylint: disable-next=unused-argument
    def signal_fill_size(sender, instance, **kwargs):
        if instance.media_type == TaskRecordMedia.MediaType.IMAGE:
            width, height = get_image_dimensions(instance.file)
            instance.width = width
            instance.height = height


signals.post_init.connect(TaskRecordMedia.signal_fill_uid, sender=TaskRecordMedia)
signals.post_init.connect(TaskRecordMedia.signal_fill_mime_type, sender=TaskRecordMedia)
signals.post_init.connect(
    TaskRecordMedia.signal_fill_task_record, sender=TaskRecordMedia
)
signals.post_init.connect(TaskRecordMedia.signal_fill_size, sender=TaskRecordMedia)
