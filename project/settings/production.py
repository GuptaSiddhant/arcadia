# Settings for deploying to Heroku
from .base import *


DEBUG = config('DEBUG')

sid = config('sid')

ALLOWED_HOSTS = ['arcadiagames.herokuapp.com']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Database and Staticfiles, django-heroku handles the heroku database, secret key and staticfiles
# setups

# Configure Django App for Heroku.
django_heroku.settings(locals(), test_runner=False, allowed_hosts=False)


# Security
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
