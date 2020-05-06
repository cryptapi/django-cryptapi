from django import template
from django.template.loader import render_to_string

from cryptapi.helpers import get_coin_multiplier, build_erc681_uri
from cryptapi.utils import build_query_string
from cryptapi.choices import TOKEN_DICT, TOKENS

from decimal import Decimal

register = template.Library()


@register.simple_tag
def convert_value(coin, value):

    _rounded = 0
    multiplier = get_coin_multiplier(coin, default=None)

    if multiplier:
        _rounded = value / multiplier

    return '{}'.format(_rounded).rstrip('0')


@register.filter
def coin_protocol(coin):
    coins = {
        'btc': 'bitcoin:',
        'bch': 'bitcoincash:',
        'ltc': 'litecoin:',
        'xmr': 'monero:',
        'iota': 'iota:',
    }

    return coins.get(coin, '')


@register.simple_tag
def build_payment_uri(coin, address, value):

    value = Decimal(str(value))

    if coin in list(TOKEN_DICT.keys()) + ['eth']:
        return build_erc681_uri(coin, address, value)

    protocol = coin_protocol(coin)
    keys = {
        'btc': 'amount',
        'bch': 'amount',
        'ltc': 'amount',
        'xmr': 'tx_amount',
        'iota': 'amount',
    }

    if protocol:
        uri = address

        if not str(address).startswith('bitcoincash:'):
            uri = protocol + address

        c_value = value

        if coin in ['iota']:
            multiplier = get_coin_multiplier(coin, default=None)

            if multiplier:
                c_value = int(value * multiplier)

        data = {keys[coin]: c_value}

        return "{uri}?{query}".format(uri=uri, query=build_query_string(data))


@register.simple_tag
def generate_qrcode(coin, address, value):
    payment_uri = build_payment_uri(coin, address, value)

    context = {
        'coin': coin,
        'payment_uri': payment_uri,
    }

    return render_to_string('cryptapi/qrcode.html', context=context)


@register.simple_tag
def generate_qrcode_for_request(request):
    coin = request.provider.coin
    address = request.address_in

    multiplier = get_coin_multiplier(coin, default=None)

    if multiplier:
        value = Decimal(request.value_requested) / multiplier

        return generate_qrcode(coin, address, value)

    return ''


@register.filter
def coin_name(coin):
    coins = {
        'btc': 'BTC',
        'bch': 'BCH',
        'ltc': 'LTC',
        'eth': 'ETH',
        'iota': 'MIOTA',
        'xmr': 'XMR',

        # Tokens
        **{t[0]: t[1] for t in TOKENS}
    }

    return coins.get(coin, '')
