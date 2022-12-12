from django.dispatch import Signal

payment_pending = Signal(['order_id', 'payment', 'value'])
payment_received = Signal(['order_id', 'payment', 'value'])
payment_complete = Signal(['order_id', 'payment', 'value'])
