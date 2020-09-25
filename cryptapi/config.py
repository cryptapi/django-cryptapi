from django.conf import settings

CRYPTAPI_URL = getattr(settings, 'CRYPTAPI_URL', "https://api.cryptapi.io/")
CRYPTAPI_HOST = 'api.cryptapi.io'
CALLBACK_BASE_URL = getattr(settings, 'CALLBACK_BASE_URL', None)
