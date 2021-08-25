from django.apps import AppConfig

class PropheciesConfig(AppConfig):
    name = 'prophecies.core'

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import User
        registry.register(User)
        registry.register(self.get_model('TaskRecord'))
        registry.register(self.get_model('TaskRecordReview'))
