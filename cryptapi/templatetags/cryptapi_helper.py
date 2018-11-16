from django import template
from cryptapi.utils import get_coin_multiplier

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
        'btc': 'bitcoin',
        'bch': 'bitcoincash',
        'ltc': 'litecoin',
        'eth': 'ethereum',
        'iota': 'iota',
    }

    return coins.get(coin, '')


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
