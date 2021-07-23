from .base import *

DEBUG = False
TEMPLATE_DEBUG = False
USE_X_FORWARDED_HOST = False

INSTALLED_APPS.remove('debug_toolbar')
MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')
