import string
import secrets
import requests
from math import floor, log10
from django.utils.timezone import now, timedelta
from urllib.parse import urlencode
from django.urls import reverse
from cryptapi.cryptapi import get_supported_coins


def round_sig(x, sig=6):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def generate_nonce(length=32):
    sequence = string.ascii_letters + string.digits
    return ''.join([secrets.choice(sequence) for i in range(length)])


def get_order_request(order_id):
    from cryptapi.models import Request

    return Request.objects.filter(order_id=order_id)


def get_active_providers():
    from cryptapi.models import Provider

    provider_qs = Provider.objects.filter(active=True)

    return [(p.coin, p.get_coin_display()) for p in provider_qs]


# Handles the currencies request and cache them
def get_coins():
    from cryptapi.models import Metadata
    metadata = Metadata.get()

    if metadata is not None and metadata.coins and now() - metadata.last_updated < timedelta(days=1):
        return metadata.coins

    try:
        coins = get_supported_coins()
        Metadata.set('coins', coins)
        return coins

    except ValueError as e:
        return print(e)


# Converts coins list to a tuple
def get_choices_coins():
    coins = ''

    try:
        for ticker, coin in get_coins().items():
            y = list(coins)
            y.append((ticker, coin))
            coins = tuple(y)

        return coins
    except:
        return ()


def build_query_string(data):
    return urlencode(data)


def build_callback_url(_r, params):
    base_url = '{scheme}://{host}{callback_url}'.format(scheme=_r.scheme, host=_r.get_host(), callback_url=reverse('cryptapi:callback'))

    base_request = requests.Request(
        url=base_url,
        params=params
    ).prepare()

    return base_request.url
