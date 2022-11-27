from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# django-insecure-4_fx@_*=e5uwd7u2n=kc(b+#kd&4%9r_dbpdjy-^g&rboqzd52

# SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + [
    # 'debug_toolbar',
    'django_extensions',
    'wagtail.contrib.styleguide',
]

MIDDLEWARE = MIDDLEWARE + [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ('127.0.0.1',)

try:
    from .local import *
except ImportError:
    pass
