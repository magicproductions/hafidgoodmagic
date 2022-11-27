from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-#(f2k(&nnv)1@cva#uwf4(vz=83vm-v#yiy*8c%dh02^&mm-v'

ALLOWED_HOSTS = ['localhost', 'hafidgoodmagic.com', '*']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE"  : "django.db.backends.postgresql_psycopg2",
        "NAME"    : 'hafidgoodmagic',
        "USER"    : 'hafidgoodmagic',
        "PASSWORD": '#yiy*8c%dh02^&mm',
        "HOST"    : 'localhost',
        "PORT"    : '5432',
    }
}

# DJANGO SECURITY SETTINGS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

cwd = os.getcwd()
CACHES = {
    'default': {
        'BACKEND' : 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': f'{cwd}/.cache'
    }
}

sentry_sdk.init(
    dsn="https://f56a3e431a4445bfb632ab1a7193d1c3@o4504228834115584.ingest.sentry.io/4504228837523456",
    integrations=[
        DjangoIntegration(),
    ],
    
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

try:
    from .local import *
except ImportError:
    pass
