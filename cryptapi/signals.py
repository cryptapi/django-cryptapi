from django.dispatch import Signal

payment_received = Signal(providing_args=['order_id', 'payment', 'value'])
payment_complete = Signal(providing_args=['order_id', 'payment', 'value'])
