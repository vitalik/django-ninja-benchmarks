import sys

sys.path.insert(0, '../..')

from common_django_settings import *  # noqa

ROOT_URLCONF = 'drf.urls'
WSGI_APPLICATION = 'drf.wsgi.application'


INSTALLED_APPS += [
    'rest_framework',
]

# TODO: find a way to get rid of these middlewares for DRF
MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}
