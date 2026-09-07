"""Middlewares for local development. Never active when DEBUG is off."""

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"


def dev_autologin(get_response):
    """Open every request as ``settings.DEV_AUTOLOGIN``, so a dev or demo
    environment needs no login page and no identity provider.

    Wired up in ``prophecies.settings.base`` only when DEBUG is on *and*
    ``DEV_AUTOLOGIN`` names a user, so it cannot be switched on in production.
    """

    def middleware(request):
        # DEBUG is re-checked here: test settings turn it off after the
        # middleware has been wired up.
        if settings.DEBUG and not request.user.is_authenticated:
            user = User.objects.filter(username=settings.DEV_AUTOLOGIN).first()
            if user is not None:
                login(request, user, backend=MODEL_BACKEND)
        return get_response(request)

    return middleware
