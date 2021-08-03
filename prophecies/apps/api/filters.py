from rest_framework_json_api.django_filters import DjangoFilterBackend

class DjangoFilterBackendWithoutForm(DjangoFilterBackend):
    """
    A simple class to disable filter form in the DRF Browsable API
    """
    def to_html(self, *args, **kwargs):
        return None
