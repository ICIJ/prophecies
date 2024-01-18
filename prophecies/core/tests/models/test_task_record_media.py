import shutil
import tempfile

from pathlib import Path
from PIL import Image

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from prophecies.core.models import Project, TaskRecordMedia, Task, TaskRecord


class TaskRecordMediaModelTests(TestCase):
    def setUp(self):
        project = Project.objects.create(name="New Project")
        self.task = Task.objects.create(name="Sample Task", project=project)
        self.task_record_foo = TaskRecord.objects.create(task=self.task, uid="foo")
        self.task_record_bar = TaskRecord.objects.create(task=self.task, uid="bar")
        self.temp_media_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_media_dir)

    def create_test_image(self, name="test.jpg"):
        img_path = Path(self.temp_media_dir) / name
        with Image.new("RGB", (100, 100)) as img:
            img.save(img_path, "JPEG")
        return img_path

    def test_media_type_property(self):
        img_path = self.create_test_image(name="foo.jpg")
        with open(img_path, "rb") as img_file:
            media = TaskRecordMedia.objects.create(
                task=self.task,
                file=SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                ),
            )
        self.assertEqual(media.media_type, TaskRecordMedia.MediaType.IMAGE)

    def test_file_to_media_type(self):
        img_path = self.create_test_image()
        with open(img_path, "rb") as img_file:
            media_type = TaskRecordMedia.file_to_media_type(
                SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                )
            )
        self.assertEqual(media_type, TaskRecordMedia.MediaType.IMAGE)

    def test_signal_fill_uid(self):
        img_path = self.create_test_image(name="bar.jpg")
        with open(img_path, "rb") as img_file:
            media = TaskRecordMedia.objects.create(
                task=self.task,
                file=SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                ),
            )
        self.assertEqual(media.uid, "bar")

    def test_signal_fill_mime_type(self):
        img_path = self.create_test_image("bar.jpg")
        with open(img_path, "rb") as img_file:
            media = TaskRecordMedia.objects.create(
                task=self.task,
                file=SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                ),
            )
        self.assertEqual(media.mime_type, "image/jpeg")

    def test_signal_fill_task_record(self):
        img_path = self.create_test_image("foo.jpg")
        with open(img_path, "rb") as img_file:
            media = TaskRecordMedia.objects.create(
                task=self.task,
                file=SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                ),
            )
        self.assertEqual(media.task_record, self.task_record_foo)

    def test_signal_fill_size_for_image(self):
        img_path = self.create_test_image("foo.jpg")
        with open(img_path, "rb") as img_file:
            media = TaskRecordMedia.objects.create(
                task=self.task,
                file=SimpleUploadedFile(
                    img_path.name, img_file.read(), content_type="image/jpeg"
                ),
            )
        self.assertEqual(media.width, 100)
        self.assertEqual(media.height, 100)
