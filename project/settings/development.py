# Settings for local development
from .base import *


DEBUG = True

SID = 'arcadia'

SECRET_KEY = 'oo-wpc9+8k3ec8ldd3jc4sg(q5ec2qu5ubl@#71!n*!f44gz$'

# Default local database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# django-heroku handles the allowed hosts, secret key and staticfiles
# setups
django_heroku.settings(locals(), test_runner=False, databases=False)
