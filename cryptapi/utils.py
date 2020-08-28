import requests
from django.shortcuts import reverse
from cryptapi.config import CRYPTAPI_URL, CALLBACK_BASE_URL
from urllib.parse import urlencode


def build_query_string(data):
    return urlencode(data)


def build_callback_url(_r, params):

    base_url = CALLBACK_BASE_URL
    if not base_url:
        base_url = '{scheme}://{host}'.format(scheme=_r.scheme, host=_r.get_host())

    base_request = requests.Request(
        url="{}{}".format(base_url, reverse('cryptapi:callback')),
        params=params
    ).prepare()

    return base_request.url


def process_request(coin, endpoint='create', params=None):
    response = requests.get(
        url="{base_url}{coin}/{endpoint}/".format(
            base_url=CRYPTAPI_URL,
            coin=coin.replace('_', '/'),
            endpoint=endpoint,
        ),
        params=params,
        headers={'Host': 'cryptapi.io'},
    )

    return response


def info(coin):
    _info = process_request(coin, endpoint='info')

    if _info:
        return _info.json()

    return None


def get_active_providers():

    from cryptapi.models import Provider

    provider_qs = Provider.objects.filter(active=True)

    return [(p.coin, p.get_coin_display()) for p in provider_qs]


def get_order_request(order_id):

    from cryptapi.models import Request

    return Request.objects.filter(order_id=order_id)

