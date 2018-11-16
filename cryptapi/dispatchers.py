
class CallbackDispatcher:

    def __init__(self, coin, request, payment, raw_data):
        self.coin = coin
        self.request = request
        self.payment = payment
        self.raw_data = raw_data

    def callback(self):

        from cryptapi.models import Request, PaymentLog
        from cryptapi.signals import payment_received, payment_complete

        try:
            request = Request.objects.get(
                provider__coin=self.coin,
                id=self.request['id'],
                nonce=self.request['nonce'],
            )

            payment, created = request.payment_set.get_or_create(txid_in__iexact=self.payment['txid_in'])

            if created:
                [setattr(payment, k, v) for k, v in self.payment.items()]

                payment.save()

                # Notify payment received
                payment_received.send_robust(
                    sender=self.__class__,
                    order_id=request.order_id,
                    payment=payment,
                    value=self.payment['value_paid']
                )

                if request.status not in ['received', 'done']:

                    total_received = self.payment['value_paid']

                    if total_received < request.value_requested:
                        total_received_list = request.payment_set.all().values_list('value_paid', flat=True)
                        total_received = sum(total_received_list)

                    if total_received < request.value_requested:
                        request.status = 'insufficient'
                    else:
                        request.status = 'received'

                        # Notify payment complete
                        payment_complete.send_robust(
                            sender=self.__class__,
                            order_id=request.order_id,
                            payment=payment,
                            value=total_received
                        )

                    request.save()

                pl = PaymentLog(
                    payment=payment,
                    raw_data=self.raw_data
                )

                pl.save()

                if request.status in ['received']:
                    request.status = 'done'
                    request.save()

            return True

        except Request.DoesNotExist:
            pass

        return False


class RequestDispatcher:

    def __init__(self, request, order_id, coin, value):
        self.request = request
        self.order_id = order_id
        self.coin = coin
        self.value = value

    def address(self):

        from cryptapi.models import Request, Provider, RequestLog
        from cryptapi.utils import build_callback_url, process_request
        from cryptapi.helpers import generate_nonce
        from cryptapi.forms import AddressCreatedForm

        try:
            provider = Provider.objects.get(coin=self.coin, active=True)

            request_model, created = Request.objects.get_or_create(
                provider=provider,
                order_id=self.order_id,
            )

            if created:

                cb_params = {
                    'request_id': request_model.id,
                    'nonce': generate_nonce(),
                }

                cb_url = build_callback_url(self.request, cb_params)

                params = {
                    'callback': cb_url,
                    'address': provider.cold_wallet
                }

                raw_response = process_request(self.coin, 'create', params)

                rl = RequestLog(
                    request=request_model,
                    raw_data=raw_response.text
                )

                rl.save()

                initials = {
                    'address_out': provider.cold_wallet,
                    'callback_url': cb_url,
                }

                response = raw_response.json()

                address_form = AddressCreatedForm(data=response, initials=initials)
                if not address_form.is_valid():
                    return None

                request_model.nonce = cb_params['nonce']
                request_model.address_in = response['address_in']
                request_model.address_out = provider.cold_wallet
                request_model.value_requested = self.value
                request_model.status = 'created'
                request_model.raw_request_url = raw_response.url

                request_model.save()

            return request_model.address_in

        except Provider.DoesNotExist:
            if not self.coin:
                raise ValueError('No provider provided')

            raise ValueError('Provider not found or not active')
