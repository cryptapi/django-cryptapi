from cryptapi.meta import VERSION
from cryptapi.dispatchers import RequestDispatcher as Invoice  # noqa
from cryptapi.utils import get_active_providers as valid_providers, get_order_request as get_order_invoices, info as coin_info  # noqa
from cryptapi.helpers import get_coin_multiplier, round_sig

__version__ = str(VERSION)

