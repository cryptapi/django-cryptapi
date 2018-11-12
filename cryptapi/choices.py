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
