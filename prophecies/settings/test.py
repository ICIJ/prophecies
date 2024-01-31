import logging

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = False
TEMPLATE_DEBUG = False
USE_X_FORWARDED_HOST = False

INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

logging.disable(logging.CRITICAL)
