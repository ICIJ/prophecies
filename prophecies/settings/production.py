import environ
from .base import *
from os.path import exists

root = environ.Path(__file__) - 3
# Read .env from the root path and load environment variables
env = environ.Env()
env_root = root.path('.env').root
# Load the .env file only if it exists
if exists(env_root):
    env.read_env(env_root)


DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = env.bool('DEBUG', default=False)
USE_X_FORWARDED_HOST = False

INSTALLED_APPS.remove('debug_toolbar')
MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env.str('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
