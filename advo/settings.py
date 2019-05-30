"""
Django settings for advo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


ALLOWED_HOSTS = []

ADMINS = (
    ('Tech Editor', 'tech@theharvardadvocate.com')
)

MANAGERS = ADMINS

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'ajax_select',
    'magazine',
    'blog',
    'payments',
    'django_social_share',
    'contacts',
    'redactor',
    'select2',
    'storages',
    'anthology',
    'advertisement',
    'versatileimagefield'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'advo.urls'

WSGI_APPLICATION = 'advo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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
            "advo.context_processors.admin_media",
            'magazine.context_processors.search_typeahead'
        ],
    },
},
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

AJAX_LOOKUP_CHANNELS = {
     'contributor' : ('magazine.lookups', 'ContributorLookup'),
     'tag' : ('magazine.lookups', 'TagLookup'),
}

STRIPE_BUY_PUBLIC_KEY = os.environ.get("STRIPE_BUY_PUBLIC_KEY", "pk_test_7mkjcG8fQj3qmdhCgP92Pq4g")
STRIPE_DONATE_PUBLIC_KEY = os.environ.get("STRIPE_DONATE_PUBLIC_KEY", "pk_test_66u2FQCcD717Ot7UGj1IvEsN")

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'paste_retain_style_properties': "color font-size",
    'content_css': "/static/magazine/css/tinymce_custom.css",
    'theme': "advanced",
    'cleanup_on_startup': False,
    'custom_undo_redo_levels': 10,
}
# Setting up logs
# http://ianalexandr.com/blog/getting-started-with-django-logging-in-5-minutes.html
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': 'advocatemain.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'WARNING',
#         },
#         'magazine': {
#             'handlers': ['file'],
#             'level': 'WARNING',
#         },
#         'payments': {
#             'handlers': ['file'],
#             'level': 'WARNING',
#         },
#     }
# }

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'

try:
    from local_settings import *
except ImportError:
    pass

try:
    from search_settings import *
except ImportError:
    pass


import django
from django.conf import settings
from django.core.mail import send_mail


# Config for API calls to Google Analytics
# Not a secure way of doing this, but this key 
# only works for read-only calls to Google Analytics
ANALYTICS_CONFIG = {
    "type": "service_account",
    "project_id": "advocate-analytics",
    "private_key_id": "da5a9f50a9c56af955df0eabd5bde7764050973d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDjfALo+DqYzOxX\nZa6hO3Y07+PmQ89UyX8RyRjagPT2azERV7yZAPILmEwjECvUm13HaFsWQXzvLFst\nHRiGmmpSpDB4WJtVydX4oXVWjVUJ79Lk534ZX7wnZQ4ZqAB1YbHpEg9KKsyxXOaR\n6uaonNZG5iAWQRSr4rvisvw7a2jpsfH+xZtmG/7qZ44AuRgzbnanrzKoVYg2pGdJ\nf4bxIgUPiTNiyLXLo/5hPX4P2ppKVezs5HIqZRkF9FoIW57WSAvxwbUmm2BOAH5c\nSLxtE8RcQm4OJ0ugDVImGQMfkpNOjWDnGBciNoCRyl0dx0mtyr0Oj/Blw/+F53s/\nneoszH8NAgMBAAECggEAC6RbGcUqaouCRO7FQych44+rYCt0PuiZAjYCeZxD7SCL\nQFH3KvVrbcB7lQfM1nKlGAF1N+xeEnd4qxRkHu9kJZqViHMwb/GGa9UHhkhxY7LM\nXj6iq3XE0VdQo2t/qoI3crAj7C3IkAMrIaid6V8tcC9y0PC/uBRAfVefpQLYOa1y\n9I54hlvj+cq1dRQiWIghQnML/8gGZ7p+U9TZPqDTvNA2OooY4jTo6lH9azf4Zvcf\nkh6D5TF+lDGfPxR2SFHxpraC+Og9/kqI2CjJAeHc9dYptv8bbXkrOfbX14OTDyUR\nt9d0hZwTAzbgyTjjY3mHFv+FPxSnrDJCtf3vaF04AQKBgQD9D6GG/HXIKHols1cA\nQuv2SW+RvLPozulgdPSas2hGodBdvShK6VGYOwlpW3TxGlrlWap66RgcWhYw1qTL\n9KodUYCL2vWQ56QbhJgGSoHx+dWTcFdBCEACbMLnQX7mPyzcXQ8Y/YJNu5sKvtG9\nmy7ycL1phA3C8Meglc1IxFlhAQKBgQDmIFbUsV1fYzrcLrsia/hdq+0CQAwCCcex\nUcgOBHmZ+MsSzb/ofqeljyj1A12ZZIeVJIvJezP4HZRRvxf1x37yFj5I8Gu7qrWa\nDNeMj/StUAVjnGBEQHBKwKiOe6jtbMqLzAtoTxiY3RAHGuaKXaToWANbe3EG76cw\nSF9oSvCSDQKBgQC+LdUSgQBzIBhL5O9pPuHeAWpbeBksyPMSjlKVQGcJTeotyE5T\nney4HwX/q7/Cwi+1VSGNpUd9ZyZuJaFLtd9ykSGt+Su7bpoiJA+sCqqFk2Ayoaax\nNOYF7H69FLetiaTJJxaFjV8z0928wZMWj11Ezf1LIvbEnfcoc+wG16jkAQKBgQC5\nX6OSga1tgUmQxDQKbl8LVcr93QnPOoGZ3P8CC6jI1xj+dK76Ycw6GTAs7iEfx1NQ\nWLgh/RTH8Uvg7cYnPiSMbk6OAt1FtyXCikW3/N5kHem5a+ZAFIhgLwGYhRR27QPb\nyOoHhG+T879NeeXr37NPVlaeArnxlGthAWuZX4SaoQKBgQDbwixLkiZW6z2lo+JK\nQQVnNcJ68Q7qOQqP/IEQXb4XO719EgcUPnuJSMLM3P4ybG0Mp3zbZc9I/BFlp9or\n/clt0vMgCyKN5tY9135ZSo351vdNuRh5ZtGp+HKlTq348cN+oC7czH0SBhjXoNJh\nJIA00CdNJvNONOThfAGKNcgFXA==\n-----END PRIVATE KEY-----\n",
    "client_email": "get-analytics@advocate-analytics.iam.gserviceaccount.com",
    "client_id": "117242232832448157884",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-analytics%40advocate-analytics.iam.gserviceaccount.com"
}

# -----------------------------------------------------------------------------------
# THE PARAMETERS BELOW ARE SET AS ENVIRONMENT VARIABLES ON THE PRODUCTION SERVER
# THESE VALUES SHOULD NOT BE HARDCODED INTO SOURCE CODE

from django.utils.crypto import get_random_string

ALLOWED_HOSTS = ['*']

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = os.getenv('SECRET_KEY', get_random_string(50, chars))

DEBUG = None

if os.getenv('IS_PROD') != 'TRUE':
    DEBUG = True
else:
    DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('RDS_DB_NAME', 'advocate'),
        'USER': os.getenv('RDS_USERNAME', 'root'),
        'PASSWORD': os.getenv('RDS_PASSWORD', 'password'),
        'HOST': os.getenv('RDS_HOSTNAME', 'localhost'),
        'PORT': os.getenv('RDS_PORT', '')
    }
}

# AWS S3 Stuff (for media and static files)
AWS_STORAGE_BUCKET_NAME = 'advo-media'
AWS_S3_REGION_NAME = 'us-east-1'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = os.getenv('MY_AWS_ACCESS_KEY_ID', 'random_id')
AWS_SECRET_ACCESS_KEY = os.getenv('MY_AWS_SECRET_ACCESS_KEY', 'random secret')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
# If we are debugging serve static files locally
if DEBUG == False:
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# Stripe stuff
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')
STRIPE_BUY_SECRET_KEY = os.getenv('STRIPE_BUY_SECRET_KEY')
STRIPE_DONATE_SECRET_KEY = os.getenv('STRIPE_DONATE_SECRET_KEY')

# Email stuff
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tech@theharvardadvocate.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL= 'tech@theharvardadvocate.com'
SERVER_EMAIL = 'webmaster@theharvardadvocate.com'

# Redirect HTTP to HTTPS
SECURE_SSL_REDIRECT = True


# Search settings
import elasticsearch
from requests_aws4auth import AWS4Auth
awsauth = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,'us-east-1','es')

HAYSTACK_CONNECTIONS = {	
    'default': {	
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',	
        'URL': 'https://search-advo-search-tdbbozoee2qmgiowsicqdjyfze.us-east-1.es.amazonaws.com',	
        'INDEX_NAME': 'haystack',	
        'KWARGS': {	
            'port': 443,	
            'http_auth': awsauth,	
            'use_ssl': True,	
            'verify_certs': True,	
            'connection_class': elasticsearch.RequestsHttpConnection	
        },	

     },	
}
