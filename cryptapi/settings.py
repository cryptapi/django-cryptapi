import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '//CrypyAPI_TEST_KEY//'

DEBUG = False

INSTALLED_APPS = [
    'cryptapi',
]

MIDDLEWARE = []

ROOT_URLCONF = 'cryptapi.urls'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'cryptapi.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
