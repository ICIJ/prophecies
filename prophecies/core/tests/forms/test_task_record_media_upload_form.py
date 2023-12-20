import zipfile
import io

from pathlib import Path
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from prophecies.core.models import Project, Task, TaskRecordMedia, TaskRecord
from prophecies.core.forms import TaskRecordMediaUploadForm


class TaskRecordMediaUploadFormTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="New Project")
        self.task = Task.objects.create(name="Sample Task", project=self.project)
        self.task_record_foo = TaskRecord.objects.create(task=self.task, uid="foo")
        self.task_record_bar = TaskRecord.objects.create(task=self.task, uid="bar")

    def build_zip_file(self, image_names: list):
        zip_path = "test.zip"
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for name in image_names:
                with io.BytesIO() as img_byte_arr:
                    img = Image.new("RGB", (1, 1), color="white")
                    img.save(img_byte_arr, format="JPEG")
                    zip_file.writestr(name, img_byte_arr.getvalue())
        file = SimpleUploadedFile(
            zip_path, Path(zip_path).read_bytes(), content_type="application/zip"
        )
        Path(zip_path).unlink()
        return file

    def test_valid_form(self):
        data = {"task": self.task.id, "unique": True, "media_types": ["IMAGE"]}
        files = {"zip_file": self.build_zip_file(["foo.jpg"])}
        form = TaskRecordMediaUploadForm(data, files)
        self.assertTrue(form.is_valid())

    def test_media_creation(self):
        data = {"task": self.task.id, "unique": True, "media_types": ["IMAGE"]}
        files = {"zip_file": self.build_zip_file(["foo.jpg", "bar.jpg"])}
        form = TaskRecordMediaUploadForm(data, files)
        form.save()
        self.assertEqual(TaskRecordMedia.objects.count(), 2)

    def test_media_creation_and_one_ignored(self):
        data = {"task": self.task.id, "unique": True, "media_types": ["IMAGE"]}
        files = {"zip_file": self.build_zip_file(["foo.jpg", "ignored.jpg"])}
        form = TaskRecordMediaUploadForm(data, files)
        form.save()
        self.assertEqual(TaskRecordMedia.objects.count(), 1)
        self.assertEqual(TaskRecordMedia.objects.first().uid, "foo")

    def test_no_media_creation_with_video_type(self):
        data = {"task": self.task.id, "unique": True, "media_types": ["VIDEO"]}
        files = {"zip_file": self.build_zip_file(["foo.jpg", "ignored.jpg"])}
        form = TaskRecordMediaUploadForm(data, files)
        form.save()
        self.assertEqual(TaskRecordMedia.objects.count(), 0)

    def test_media_update(self):
        TaskRecordMedia.objects.create(
            task=self.task, uid="foo", task_record=self.task_record_foo
        )
        data = {"task": self.task.id, "unique": True, "media_types": ["IMAGE"]}
        files = {"zip_file": self.build_zip_file(["foo.jpg"])}
        form = TaskRecordMediaUploadForm(data, files)
        form.save()
        self.assertEqual(TaskRecordMedia.objects.count(), 1)
        self.assertEqual(TaskRecordMedia.objects.first().uid, "foo")
