# Settings for local development
import django_heroku

from .base import *

DEBUG = True

SID = 'ar20ga19'

SECRET_KEY = 'oo-wpc9+8k3ec8ldd3jc4sg(q5ec2qu5ubl@#71!n*!f44gz$'
PAYMENT_SECRET_KEY = 'fbd947351c5047a19b47636402760ccc'

# Default local database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Console email backend settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-heroku handles the allowed hosts, secret key and staticfiles
# setups
django_heroku.settings(locals(), test_runner=False, databases=False)
