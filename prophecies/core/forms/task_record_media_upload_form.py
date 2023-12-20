from io import BytesIO
from typing import Tuple
from pathlib import Path
from zipfile import ZipFile

from django import forms
from django.core.files import File
from django.core.exceptions import ValidationError
from django.db import IntegrityError


from prophecies.core.models import Task, TaskRecordMedia


class TaskRecordMediaUploadForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.all())
    zip_file = forms.FileField(label="ZIP file")
    unique = forms.BooleanField(
        required=False,
        label="Only one per task record",
        help_text="This will delete existing media with the same uid.",
    )
    media_types = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=TaskRecordMedia.MediaType.choices
    )

    # pylint: disable-next=unused-argument
    def save(self, commit: bool = True) -> Tuple[int, int, int]:
        """
        Entry point for saving the form. Validates the form and processes the ZIP file.
        Returns a tuple with counts of created, updated, and ignored records.
        """
        self._validate_form()
        return self._process_zip_file()

    def _validate_form(self) -> None:
        """
        Validates the form. Raises a ValidationError if the form is not valid.
        """
        if not self.is_valid():
            raise ValidationError("Form is not valid.")

    def _process_zip_file(self) -> Tuple[int, int, int]:
        """
        Processes each file in the uploaded ZIP file.
        Returns a tuple with counts of created, updated, and ignored records.
        """
        created_count, updated_count, ignored_count = 0, 0, 0
        with ZipFile(self.cleaned_data["zip_file"], "r") as zip_file:
            for name in zip_file.namelist():
                created, updated, ignored = self._process_file(zip_file, name)
                created_count += created
                updated_count += updated
                ignored_count += ignored
        return created_count, updated_count, ignored_count

    def _process_file(self, zip_file: ZipFile, name: str) -> Tuple[int, int, int]:
        """
        Processes a single file from the ZIP archive.
        Determines if the file should be saved and performs the save operation.
        Returns a tuple with counts of created, updated, and ignored for the file.
        """
        try:
            file = self._extract_file(zip_file, name)
            media_types = self.cleaned_data["media_types"]
            if TaskRecordMedia.file_to_media_type(file) in media_types:
                return self._save_media(file, name)
            return 0, 0, 0
        except (ValidationError, IntegrityError, TaskRecordMedia.DoesNotExist):
            return 0, 0, 1

    def _extract_file(self, zip_file: ZipFile, name: str) -> File:
        """
        Extracts a file from the ZIP file and returns it as a Django File object.
        """
        with zip_file.open(name) as file:
            file_content = file.read()
        return File(BytesIO(file_content), Path(name).name)

    def _save_media(self, file: File, name: str) -> Tuple[int, int, int]:
        """
        Decides whether to create a new media record or update an existing one.
        Returns a tuple with counts of created, updated, and ignored for the file.
        """
        if self.cleaned_data["unique"]:
            return self._update_or_create_media(file, name)
        return self._create_new_media(file), 0, 0

    def _create_new_media(self, file: File) -> int:
        """
        Creates a new TaskRecordMedia record with the given file.
        Returns 1 to indicate one record created.
        """
        TaskRecordMedia(file=file, task=self.cleaned_data["task"]).save()
        return 1

    def _update_or_create_media(self, file: File, name: str) -> Tuple[int, int]:
        """
        Updates an existing TaskRecordMedia record, or creates a new one if it doesn't exist.
        Returns a tuple with counts of created, updated, and ignored for the file.
        """
        defaults = {"file": file}
        task = self.cleaned_data["task"]
        uid = Path(name).stem
        _media, created = TaskRecordMedia.objects.update_or_create(
            task=task, uid=uid, defaults=defaults
        )
        return (1, 0, 0) if created else (0, 1, 0)
