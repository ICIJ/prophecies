from os.path import normpath
import sys
import environ

root = environ.Path(__file__) - 3
project_root = root.path('prophecies')

# Read .env from the root path and load environment variables
env = environ.Env()
env.read_env(root.path('.env').root)

# Build paths inside the project
BASE_DIR = root()

# Add apps/ directory to the Python path
sys.path.append(normpath(project_root.path('apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='django-insecure-+u+8%4g8(^c+6_#hff2#mw!r%-05net!9tap+p4lb*#d5!kzw$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

INTERNAL_IPS = ('127.0.0.1', )

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'social_django',
    'debug_toolbar',
    'rest_framework',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'prophecies.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            project_root.path('core', 'templates').root,
            project_root.path('apps', 'api', 'templates').root,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'prophecies.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# https://github.com/jacobian/dj-database-url#url-schema

DATABASES = {
    'default': env.db(default='sqlite:///%s' % root.path('db.sqlite3')()),
    'test_dpv': env.db(default='sqlite:///%s' % root.path('test_dpv.sqlite3')())
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    'prophecies.core.xemx.XemxOauth2',
    'django.contrib.auth.backends.ModelBackend',
)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Xemx configuration using python-socual-auth
# https://python-social-auth.readthedocs.io

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'last_name', 'email']
SOCIAL_AUTH_URL_NAMESPACE = 'sso'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/api'
SOCIAL_AUTH_LOGIN_URL = '/login/xemx'
SOCIAL_AUTH_XEMX_KEY = env.str('SOCIAL_AUTH_XEMX_KEY', default='')
SOCIAL_AUTH_XEMX_SECRET = env.str('SOCIAL_AUTH_XEMX_SECRET', default='')
SOCIAL_AUTH_XEMX_HOSTNAME = env.str('SOCIAL_AUTH_XEMX_HOSTNAME', default='http://localhost:3001')

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',
    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',
    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',
    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',
    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
    # Map Xemx Groups to Django Groups using their names
    'prophecies.core.xemx.map_xemx_groups',
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Cache
# https://docs.djangoproject.com/en/2.2/topics/cache/
# https://django-environ.readthedocs.io/en/latest/index.html#multiple-redis-cache-locations
CACHES = {
    'default': env.cache('CACHE_URL', default='dummycache://')
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = env.str('STATIC_URL', default='/static/')
STATIC_ROOT = env.str('STATIC_ROOT', default=project_root.path('run', 'static'))

STATICFILES_DIRS = [
    project_root.path('static').root,
    # Add app's static dir here, for instance:
    # project_root.path('apps', 'exampleapp', 'static').root,
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
