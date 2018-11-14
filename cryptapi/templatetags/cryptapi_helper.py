from django import template

register = template.Library()


@register.simple_tag
def convert_value(coin, value):

    _rounded = 0

    if coin == 'btc' or coin == 'ltc' or coin == 'bch':
        _rounded = value / 100000000

    if coin == 'eth':
        _rounded = value / 1000000000000000000

    if coin == 'iota':
        _rounded = value / 1000000

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
