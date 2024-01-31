import structlog

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

root = environ.Path(__file__) - 3
# Read .env from the root path and load environment variables
env = environ.Env()
env.read_env(root.path(".env").root)

DEBUG = env.bool("DEBUG", default=False)
TEMPLATE_DEBUG = env.bool("DEBUG", default=False)
USE_X_FORWARDED_HOST = False

INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

# Logging
# https://docs.djangoproject.com/en/4.2/ref/logging/
# https://django-structlog.readthedocs.io/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "INFO"),
        },
        "core": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Cache
# https://docs.djangoproject.com/en/4.2/topics/cache/
# https://django-environ.readthedocs.io/en/latest/types.html#environ-env-cache-url
CACHES = {
    "default": env.cache("CACHE_URL", default="filecache:///code/prophecies/run/cache/")
}
