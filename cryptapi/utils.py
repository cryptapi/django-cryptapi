import requests
from django.shortcuts import reverse
from cryptapi.config import CRYPTAPI_URL


def build_callback_url(_r, params):
    base_url = '{scheme}://{host}'.format(scheme=_r.scheme, host=_r.get_host())

    base_request = requests.Request(
        url="{}{}".format(base_url, reverse('cryptapi:callback')),
        params=params
    ).prepare()

    return base_request.url


def process_request(coin, endpoint='create', params=None):
    response = requests.get(
        url="{base_url}{coin}/{endpoint}".format(
            base_url=CRYPTAPI_URL,
            coin=coin,
            endpoint=endpoint,
        ),
        params=params
    )

    return response


def get_active_providers():

    from cryptapi.models import Provider

    provider_qs = Provider.objects.filter(active=True)

    return [(p.coin, p.get_coin_display()) for p in provider_qs]


def get_order_request(order_id):

    from cryptapi.models import Request

    return Request.objects.filter(order_id=order_id)

