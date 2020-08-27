from django.utils.translation import gettext_lazy as _

TOKENS = [
    ('erc20_usdt', 'ERC-20 USDT', '0xdAC17F958D2ee523a2206206994597C13D831ec7', 6, 4),
    ('erc20_usdc', 'ERC-20 USDC', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 6, 4),
    ('erc20_busd', 'ERC-20 BUSD', '0x4Fabb145d64652a948d72533023f6E7A623C7C53', 18, 16),
    ('erc20_pax', 'ERC-20 PAX', '0x8E870D67F660D95d5be530380D0eC0bd388289E1', 18, 16),
    ('erc20_tusd', 'ERC-20 TUSD', '0x0000000000085d4780B73119b644AE5ecd22b376', 18, 16),
    ('erc20_bnb', 'ERC-20 BNB', '0xB8c77482e45F1F44dE1745F52C74426C631bDD52', 18, 0),
    ('erc20_link', 'ERC-20 ChainLink', '0x514910771AF9Ca656af840dff83E8264EcF986CA', 18, 0),
    ('erc20_cro', 'ERC-20 Crypto.com Coin', '0xA0b73E1Ff0B80914AB6fe0444E65848C4C34450b', 8, 0),
    ('erc20_mkr', 'ERC-20 Maker', '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2', 18, 0),
    ('erc20_nexo', 'ERC-20 NEXO', '0xB62132e35a6c13ee1EE0f84dC5d40bad8d815206', 18, 0),
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
