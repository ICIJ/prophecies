import csv
import io
from typing import Tuple
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from prophecies.core.models import TaskRecordMedia
from prophecies.core.forms import TaskRecordMediaUploadZipForm


class TaskRecordMediaUploadCSVForm(TaskRecordMediaUploadZipForm):
    def _read_file_as_csv(self):
        """
        Reads the uploaded CSV file and returns a CSV reader object.
        """
        csv_file = self.cleaned_data["file"]
        stream = io.StringIO(csv_file.read().decode("UTF8"), newline=None)
        return csv.DictReader(stream)

    def _process_row(self, row: dict) -> Tuple[int, int, int]:
        """
        Processes a single row from the CSV file.
        Returns a tuple with counts of created, updated, and ignored rows.
        """
        try:
            file = row.get("file", None)
            file_url = row.get("file_url", None)
            mime_type = row.get("mime_type", None)
            name = row.get("uid", None)
            task_record_id = row.get("task_record", row.get("task_record_id", None))
            if not file and not file_url:
                raise ValidationError(
                    "Etheir a file (`file` column) or a file URL (`file_url` column) is required in the CSV row."
                )
            if not name and not task_record_id:
                raise ValidationError(
                    # pylint: disable=line-too-long
                    "Either a unique identifier (`uid` column) or a task record ID (`task_record` or `task_record_id` column) is required in the CSV row."
                )
            return self._save_media(name, file, file_url, mime_type, task_record_id)
        except (ValidationError, IntegrityError, TaskRecordMedia.DoesNotExist):
            return 0, 0, 1

    def _process_form_file(self) -> Tuple[int, int, int]:
        """
        Processes each row in the  CSV file.
        Returns a tuple with counts of created, updated, and ignored rows.
        """
        created_count, updated_count, ignored_count = 0, 0, 0
        for row in self._read_file_as_csv():
            created, updated, ignored = self._process_row(row)
            created_count += created
            updated_count += updated
            ignored_count += ignored
        return created_count, updated_count, ignored_count
