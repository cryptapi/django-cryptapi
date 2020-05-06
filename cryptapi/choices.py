from django.utils.translation import gettext_lazy as _

TOKENS = [
    ('erc20_usdt', 'ERC-20 USDT', '0xdAC17F958D2ee523a2206206994597C13D831ec7', 6, 4),
    ('erc20_bcz', 'ERC-20 BECAZ', '0x08399ab5eBBE96870B289754A7bD21E7EC8c6FCb', 18, 0),
]

TOKEN_DICT = {t[0]: t for t in TOKENS}


COINS = [
    ('btc', 'Bitcoin'),
    ('eth', 'Ethereum'),
    ('bch', 'Bitcoin Cash'),
    ('ltc', 'Litecoin'),
    ('iota', 'IOTA'),
    ('xmr', 'Monero'),
] + [(t[0], t[1]) for t in TOKENS]  # Tokens


STATUS = (
    ('created', _('Created')),
    ('pending', _('Pending')),
    ('insufficient', _('Payment Insufficient')),
    ('received', _('Received')),
    ('done', _('Done')),
)


COIN_MULTIPLIERS = {
    'btc': 10**8,
    'bch': 10**8,
    'ltc': 10**8,
    'eth': 10**18,
    'iota': 10**6,
    'xmr': 10**12,

    # Tokens
    **{t[0]: 10**t[3] for t in TOKENS}
}
