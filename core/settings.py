import os

import stripe
from dj_database_url import config as db_config

from core.helpers import DotEnvReader, EnvValue

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DotEnvReader(os.path.join(BASE_DIR, '.env')).read()

stripe.api_key = os.getenv('STRIPE_API_KEY')

# If true, runs the celery server in the same process of the Django app
CELERY_ALWAYS_EAGER = EnvValue('CELERY_ALWAYS_EAGER', False).to_bool()
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

PRODUCTION = EnvValue('PRODUCTION', False).to_bool()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = EnvValue('DEBUG', not PRODUCTION).to_bool()

ALLOWED_HOSTS = EnvValue('ALLOWED_HOSTS', '' if PRODUCTION else '*').to_list()

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'rest_framework',
]

LOCAL_APPS = [
    'core',
    'app',
]

INSTALLED_APPS = LOCAL_APPS + THIRD_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {'default': db_config()}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'core', 'locale'),
]

AUTH_USER_MODEL = 'app.User'
