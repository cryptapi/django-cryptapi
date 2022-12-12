import requests

CRYPTAPI_URL = 'https://api.cryptapi.io/'
BLOCKBEE_URL = 'https://api.blockbee.io/'
CRYPTAPI_HOST = 'api.cryptapi.io'
BLOCKBEE_HOST = 'api.blockbee.io'


def get_info(coin=''):
    _info = process_request(coin, endpoint='info')

    if _info:
        return _info

    return None


def get_supported_coins():
    _info = get_info('')

    _info.pop('fee_tiers', None)

    _coins = {}

    for ticker, coin_info in _info.items():

        if 'coin' in coin_info.keys():
            _coins[ticker] = coin_info['coin']
        else:
            for token, token_info in coin_info.items():
                _coins[ticker + '_' + token] = token_info['coin'] + ' (' + ticker.upper() + ')'

    return _coins


def get_logs(coin, callback_url):
    if coin is None or callback_url is None:
        return None

    params = {
        'callback': callback_url
    }

    _logs = process_request(coin, endpoint='logs', params=params)

    if _logs:
        return _logs

    return None


def get_qrcode(coin, address, value='', size=300):
    if coin is None:
        return None

    params = {
        'address': address,
        'size': size
    }

    if value:
        params = {
            'address': address,
            'size': size,
            'value': value
        }

    _qrcode = process_request(coin, endpoint='qrcode', params=params)

    if _qrcode:
        return _qrcode

    return None


def get_conversion(origin, to, value):
    params = {
        'from': origin,
        'to': to,
        'value': value
    }

    _value = process_request('', endpoint='convert', params=params)

    if _value:
        return _value

    return None


def get_estimate(coin):
    params = {
        'addresses': 1,  # Change this according your number of addresses
        'priority': 'default'  # Change this according the priority you want to define
    }

    _estimate = process_request(coin, endpoint='estimate', params=params)

    if _estimate:
        return _estimate

    return None


def get_address(coin, params):
    _address = process_request(coin, endpoint='create', params=params)

    if _address:
        return _address

    return None


def process_request(coin='', endpoint='', params=None):
    if coin != '':
        coin += '/'

    if params is not None and 'apikey' in params:

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=BLOCKBEE_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': BLOCKBEE_HOST},
        )
    else:

        response = requests.get(
            url="{base_url}{coin}{endpoint}/".format(
                base_url=CRYPTAPI_URL,
                coin=coin.replace('_', '/'),
                endpoint=endpoint,
            ),
            params=params,
            headers={'Host': CRYPTAPI_HOST},
        )

    url = response.url

    response = response.json()

    if endpoint == 'create':
        response['raw_request_url'] = url  # For debugging purposes

    return response
