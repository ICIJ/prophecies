import magic

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MimeTypeValidator:
    messages = {"not_supported": "File type is not supported."}

    @staticmethod
    def allowed_mime_types():
        from prophecies.core.models import TaskRecordMedia

        return TaskRecordMedia.mime_types()

    def __call__(self, file):
        file.seek(0)
        mine_type = magic.from_buffer(file.read(2048), mime=True)
        if mine_type not in self.allowed_mime_types():
            raise ValidationError(self.messages["not_supported"])
