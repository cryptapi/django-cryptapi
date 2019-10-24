from django import template
from cryptapi.helpers import get_coin_multiplier
from cryptapi.utils import build_query_string

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
        'eth': 'ethereum:',
        'xmr': 'monero:',
        'iota': 'iota:',
    }

    return coins.get(coin, '')


@register.simple_tag
def build_payment_uri(coin, address, value):
    protocol = coin_protocol(coin)
    keys = {
        'btc': 'amount',
        'bch': 'amount',
        'ltc': 'amount',
        'eth': 'value',
        'xmr': 'tx_amount',
        'iota': 'amount'
    }

    if protocol:
        uri = address

        if not str(address).startswith('bitcoincash:'):
            uri = protocol + address

        c_value = value

        if coin in ['eth', 'iota']:
            multiplier = get_coin_multiplier(coin, default=None)

            if multiplier:
                c_value = int(value * multiplier)

        data = {keys[coin]: c_value}

        return "{uri}?{query}".format(uri=uri, query=build_query_string(data))


@register.filter
def coin_name(coin):
    coins = {
        'btc': 'BTC',
        'bch': 'BCH',
        'ltc': 'LTC',
        'eth': 'ETH',
        'iota': 'MIOTA',
    }

    return coins.get(coin, '')
