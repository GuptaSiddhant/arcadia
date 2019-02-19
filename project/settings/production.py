# Settings for deploying to Heroku
import django_heroku

from .base import *

# In Production environment (heroku) Django fetches the SECRET_KEY, sid, Debug and DATABASE
# from heroku's environment variables

DEBUG = config('DEBUG') == 'True'

SID = config('sid')

PAYMENT_SECRET_KEY = config('PAYMENT_SECRET_KEY')

GMAIL_SMTP_PW = config('GMAIL_SMTP_PW')

ALLOWED_HOSTS = ['lit-hamlet-73485.herokuapp.com', 'arcadiagames.herokuapp.com']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Gmail SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'arcadiagames.ga@gmail.com'
EMAIL_HOST_PASSWORD = GMAIL_SMTP_PW
EMAIL_USE_TLS = True

# Database and Staticfiles, django-heroku handles the heroku database, secret key and staticfiles
# setups

# Configure Django App for Heroku.
django_heroku.settings(locals(), test_runner=False, allowed_hosts=False)

# Security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 3600  # 1h # 15768000 #6kk
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
