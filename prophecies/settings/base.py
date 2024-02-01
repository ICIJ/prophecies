import sys
from os.path import normpath

import environ
import structlog


root = environ.Path(__file__) - 3
project_root = root.path("prophecies")

# Read .env from the root path and load environment variables
env = environ.Env()
env.read_env(root.path(".env").root)

# Build paths inside the project
BASE_DIR = root()

# Add apps/ directory to the Python path
sys.path.append(normpath(project_root.path("apps")))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-+u+8%4g8(^c+6_#hff2#mw!r%-05net!9tap+p4lb*#d5!kzw$",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)
TEMPLATE_DEBUG = env.bool("TEMPLATE_DEBUG", default=DEBUG)

SITE_ID = 1

INTERNAL_IPS = ("127.0.0.1",)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://localhost:8080"]
)

# Application definition

INSTALLED_APPS = [
    "polymorphic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_structlog",
    "drf_spectacular",
    "admin_auto_filters",
    "actstream",
    "cachalot",
    "debug_toolbar",
    "social_django",
    "rest_framework",
    "rest_framework_json_api",
    "django_filters",
    "webpack_loader",
    "colorfield",
    "constance",
    "import_export",
    "constance.backends.database",
    "prophecies.core.PropheciesConfig",
    "prophecies.apps.api",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]

ROOT_URLCONF = "prophecies.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            project_root.path("core", "templates").root,
            project_root.path("apps", "api", "templates").root,
            project_root.path("apps", "frontend", "templates").root,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

FRONTEND_DIR = project_root.path("apps", "frontend")

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": DEBUG,
        "BUNDLE_DIR_NAME": "dist/",  # must end with slash
        "STATS_FILE": FRONTEND_DIR.path("dist", "webpack-stats.json"),
    }
}

WSGI_APPLICATION = "prophecies.wsgi.application"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = env.str("STATIC_URL", default="/static/")
STATIC_ROOT = env.str("STATIC_ROOT", default=project_root.path("run", "static"))

STATICFILES_DIRS = [
    project_root.path("static").root,
    project_root.path("apps", "frontend", "dist").root,
]

# Media Storage
# https://docs.djangoproject.com/en/4.2/topics/files/
# https://django-dbbackup.readthedocs.io/en/master/storage.html

# Allow user to update up to 5000 records at the same time
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000
MEDIA_STORAGE = env.str("MEDIA_STORAGE", "FS").upper()

# S3 Storage Configurations
if MEDIA_STORAGE == "S3":
    MEDIA_ROOT = env.str("MEDIA_ROOT", default="/media/")
    MEDIA_URL = env.str("MEDIA_URL", default="https://{AWS_S3_CUSTOM_DOMAIN}/")

    STORAGES = {
        "default": {
            "BACKEND": "prophecies.core.storages.S3MediaStorage",
            "OPTIONS": {
                "access_key": env("AWS_ACCESS_KEY_ID"),
                "secret_key": env("AWS_SECRET_ACCESS_KEY"),
                "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
                "region_name": env("AWS_S3_REGION_NAME"),
                "default_acl": None,
                "object_parameters": {"CacheControl": "max-age=86400"},
                "signature_version": env.str("AWS_S3_SIGNATURE_VERSION", "s3v4"),
                "querystring_expire": env.str("AWS_QUERYSTRING_EXPIRE", "3600"),
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Filesystem Storage Configurations
else:
    MEDIA_URL = env.str("MEDIA_URL", default="/media/")
    MEDIA_ROOT = env.str("MEDIA_ROOT", default=project_root.path("run", "media"))


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://github.com/jacobian/dj-database-url#url-schema

DATABASES = {
    "default": env.db(default=f'sqlite:///{root.path("db.sqlite3")()}'),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = (
    "prophecies.core.oauth2_provider.OAuth2Provider",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.DjangoModelPermissions",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "PAGE_SIZE": 10,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework_json_api.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework.filters.SearchFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "prophecies.apps.api.filters.DjangoFilterBackendWithoutForm",
    ),
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Prophecies API",
    "DESCRIPTION": """Prophecies is a platform to fact check data collaboratively. 
    It is a free open-source software developed by the International Consortium of Investigative Journalists (ICIJ).
    """,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": '/api/v1',
}

JSON_API_FORMAT_FIELD_NAMES = "camelize"

USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST", default=DEBUG)

# Xemx configuration using python-socual-auth
# https://python-social-auth.readthedocs.io

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ["username", "first_name", "last_name", "email"]
SOCIAL_AUTH_IMMUTABLE_USER_FIELDS = [
    "username",
    "email",
]
SOCIAL_AUTH_URL_NAMESPACE = env.str("SOCIAL_AUTH_URL_NAMESPACE", default="sso")
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_SANITIZE_REDIRECTS = not DEBUG
SOCIAL_AUTH_LOGIN_URL = env.str("SOCIAL_AUTH_LOGIN_URL", default="/login/provider/")

# All OAuth2 provider's settings
SOCIAL_AUTH_PROVIDER_HOSTNAME = env.str("SOCIAL_AUTH_PROVIDER_HOSTNAME", default="")
SOCIAL_AUTH_PROVIDER_KEY = env.str("SOCIAL_AUTH_PROVIDER_KEY", default="")
SOCIAL_AUTH_PROVIDER_SECRET = env.str("SOCIAL_AUTH_PROVIDER_SECRET", default="")
SOCIAL_AUTH_PROVIDER_PROFILE_URL = env.str(
    "SOCIAL_AUTH_PROVIDER_PROFILE_URL",
    default=f"{SOCIAL_AUTH_PROVIDER_HOSTNAME}/api/v1/me.json?",
)
SOCIAL_AUTH_PROVIDER_AUTHORIZATION_URL = env.str(
    "SOCIAL_AUTH_PROVIDER_AUTHORIZATION_URL",
    default=f"{SOCIAL_AUTH_PROVIDER_HOSTNAME}/oauth/authorize",
)
SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_URL = env.str(
    "SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_URL",
    default=f"{SOCIAL_AUTH_PROVIDER_HOSTNAME}/oauth/token",
)
SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_METHOD = env.str(
    "SOCIAL_AUTH_PROVIDER_ACCESS_TOKEN_METHOD", default="POST"
)
SOCIAL_AUTH_PROVIDER_USERNAME_FIELD = env.str(
    "SOCIAL_AUTH_PROVIDER_USERNAME_FIELD", default="username"
)
SOCIAL_AUTH_PROVIDER_GROUPS_FIELD = env.str(
    "SOCIAL_AUTH_PROVIDER_GROUPS_FIELD", default="groups"
)
SOCIAL_AUTH_PROVIDER_STAFF_GROUP = env.str(
    "SOCIAL_AUTH_PROVIDER_STAFF_GROUP", default="staff"
)

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    "social_core.pipeline.social_auth.social_details",
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    "social_core.pipeline.social_auth.social_uid",
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    "social_core.pipeline.social_auth.auth_allowed",
    # Checks if the current social-account is already associated in the site.
    "social_core.pipeline.social_auth.social_user",
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    "social_core.pipeline.user.get_username",
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',
    # Create a user account if we haven't found one yet.
    "social_core.pipeline.user.create_user",
    # Create the record that associates the social account with the user.
    "social_core.pipeline.social_auth.associate_user",
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    "social_core.pipeline.social_auth.load_extra_data",
    # Update the user record with any changed info from the auth service.
    "social_core.pipeline.user.user_details",
    # Map Provider Groups to Django Groups using their names
    "prophecies.core.oauth2_provider.map_provider_groups",
)

# Activity Stream settings
# https://django-activity-stream.readthedocs.io/en/latest/configuration.html

ACTSTREAM_SETTINGS = {
    "FETCH_RELATIONS": True,
    "USE_JSONFIELD": True,
    "MANAGER": "prophecies.core.managers.ExtendedActionManager",
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Cache
# https://docs.djangoproject.com/en/4.2/topics/cache/
# https://django-environ.readthedocs.io/en/latest/types.html#environ-env-cache-url

CACHES = {
    "default": env.cache(
        "CACHE_URL", default=f"filecache://{project_root.path('run', 'cache')}"
    )
}

# Dynamique settings
# https://django-constance.readthedocs.io/en/latest/backends.html#database
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_CACHE_BACKEND = env.str(
    "CONSTANCE_DATABASE_CACHE_BACKEND", default="default"
)
CONSTANCE_CONFIG = {
    "appName": ("Prophecies", "Name of the app to display publicaly"),
    "avatarUrlTemplate": (
        "https://www.gravatar.com/avatar/{{ emailMd5 }}?d=mp",
        "Template to build the avatar URL",
    ),
    "defaultLocale": ("en", 'Define locale code (ie. "en", "fr", "jp", ...)'),
    "helpLink": (
        "https://github.com/ICIJ/prophecies/issues/new",
        "Link to the support",
    ),
    "helpDescription": (
        "Any trouble logging in?",
        "Help text for the login page. Must be public.",
    ),
    "loginUrl": (SOCIAL_AUTH_LOGIN_URL, "Link to create a user session"),
    "loginWelcome": (
        "Welcome to Prophecies",
        "Title for the login page. Must be public.",
    ),
    "loginAccountDescription": (
        "Use your account to continue:",
        "Account description for the login page. Must be public.",
    ),
    "loginAccountButton": ("Login", "Login button for the login page. Must be public."),
    "logoutUrl": ("/admin/logout/?next=/", "Link to logout"),
    "orgName": ("ICIJ", "Name of the organization deploying this app"),
}

# A list of explictly public variables
CONSTANCE_PUBLIC_KEYS = env.list("CONSTANCE_PUBLIC_KEYS", default=["loginUrl"])

# Either or not we should activate Django Admin native login. Activate by
# default in DEBUG mode.
DJANGO_ADMIN_LOGIN = env.bool("DJANGO_ADMIN_LOGIN", default=DEBUG)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Logging
# https://docs.djangoproject.com/en/4.2/ref/logging/
# https://django-structlog.readthedocs.io/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "DEBUG"),
        },
        "core": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "DEBUG"),
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
