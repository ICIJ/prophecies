import logging

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = False
TEMPLATE_DEBUG = False
USE_X_FORWARDED_HOST = False

# Deinstall Django Debug Toolbar
INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

# Ensure nothing is cached during test

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Hide all constance keys by default
CONSTANCE_PUBLIC_KEYS = []

logging.disable(logging.CRITICAL)
