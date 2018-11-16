import string
import random
from math import floor, log10
from cryptapi.choices import COIN_MULTIPLIERS


def get_coin_multiplier(coin, default=None):
    return COIN_MULTIPLIERS.get(coin, default)


def round_sig(x, sig=4):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def generate_nonce(length=32):

    # Not cryptographically secure, but good enough for generating nonces

    sequence = string.ascii_letters + string.digits

    return ''.join([random.choice(sequence) for i in range(length)])
