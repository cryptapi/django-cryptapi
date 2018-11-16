from django.utils.translation import gettext_lazy as _


COINS = (
    ('btc', 'Bitcoin'),
    ('eth', 'Ethereum'),
    ('bch', 'Bitcoin Cash'),
    ('ltc', 'Litecoin'),
    ('iota', 'IOTA'),
)


STATUS = (
    ('created', _('Created')),
    ('insufficient', _('Payment Insufficient')),
    ('received', _('Received')),
    ('done', _('Done')),
)


COIN_MULTIPLIERS = {
    'btc': 100000000,
    'bch': 100000000,
    'ltc': 100000000,
    'eth': 1000000000000000000,
    'iota': 1000000,
}
