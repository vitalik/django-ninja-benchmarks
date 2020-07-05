import sys

sys.path.insert(0, '../..')

from common_django_settings import *  # noqa

ROOT_URLCONF = 'djninja.urls'
WSGI_APPLICATION = 'djninja.wsgi.application'

