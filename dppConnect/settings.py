"""
Django settings for dppConnect project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',cast=bool)

ALLOWED_HOSTS = ['localhost','*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'django_cron',
    'django_extensions',
    'django_tables2',
    'django_filters',
    'bootstrap3',
    'main',
    'ckeditor',
    'ckeditor_uploader',
    'feedback',
    'survey',
    'bootstrapform',
    'debug_toolbar',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CSP_DEFAULT_SRC = ["'self'", '127.0.0.1:8000', "'unsafe-inline'", "https://dpp-static.s3.amazonaws.com"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'", "https://dpp-static.s3.amazonaws.com"]
CSP_SCRIPT_SRC = [
    "https://stackpath.bootstrapcdn.com",
    "https://cdn.jsdelivr.net",
    "https://code.jquery.com",
    "https://dpp-static.s3.amazonaws.com",
    "'self'",
    "'unsafe-inline'",
]
CSP_IMG_SRC = ["'self'", "https://dpp-static.s3.amazonaws.com",]
CSP_FRAME_ANCESTORS = ("'self'", 'https://engage.aps.org')
CSP_INCLUDE_NONCE_IN = ('script-src', )

CRON_CLASSES = [
    "main.parser.MyCronJob",
    # ...
]

CORS_ALLOWED_ORIGINS = [
"https://dpp-static.s3.amazonaws.com/static/",
"http://localhost:8080",
]


ROOT_URLCONF = 'dppConnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'dppConnect.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if config('LOCAL',cast=bool):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

if not config('LOCAL',cast=bool):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

##############################################
### Static files (CSS, JavaScript, Images) ###
##############################################
if config('LOCAL',cast=bool):
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
else:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = 'public-read'

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'dppConnect.storage_backends.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, PUBLIC_MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = 'dppConnect.storage_backends.PublicMediaStorage'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    AWS_QUERYSTRING_AUTH = False

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

##########################
### CK Editor settings ###
##########################
#CKEDITOR_BASEPATH = STATIC_URL+"/ckeditor/"
X_FRAME_OPTIONS = 'SAMEORIGIN'
CKEDITOR_UPLOAD_PATH = "uploads/"
#CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js'
CKEDITOR_CONFIGS = {
    'myconfig': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline'],'/',
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image','Table','HorizontalRule','Smiley','SpecialChar'],
            ['RemoveFormat', 'Source']
        ]
    },
}

####################
### EMAIL CONFIG ###
####################
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

CSV_DIRECTORY = Path("csv") # Define the directory where csv are exported
TEX_DIRECTORY = Path("tex") # Define the directory where tex files and pdf are exported


#####################
### CELERY CONFIG ###
#####################
REDIS_PSWD = config('REDIS_PSWD')
CELERY_BROKER_URL = 'redis://:'+REDIS_PSWD+ '@localhost:6379'
CELERY_RESULT_BACKEND = 'django-db' #'redis://:'+REDIS_PSWD+'@localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

