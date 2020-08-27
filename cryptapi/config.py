from django.conf import settings

CRYPTAPI_URL = getattr(settings, 'CRYPTAPI_URL', "https://cryptapi.io/api/")
CALLBACK_BASE_URL = getattr(settings, 'CALLBACK_BASE_URL', None)
