class CallbackDispatcher:

    def __init__(self, coin, request, payment, raw_data, result=None):
        self.coin = coin
        self._request = request
        self.payment = payment
        self.raw_data = raw_data
        self.result = result

    def callback(self):

        from cryptapi.models import Request, PaymentLog
        from cryptapi.signals import payment_received, payment_complete, payment_pending
        from cryptapi.cryptapi import get_address

        try:
            request = Request.objects.get(
                provider__coin=self.coin,
                id=self._request['id'],
                nonce=self._request['nonce'],
            )

            payment, created = request.payment_set.get_or_create(txid_in__iexact=self.payment['txid_in'])

            [setattr(payment, k, v) for k, v in self.payment.items() if v is not None]

            payment.pending = self.result in ['pending']
            payment.save()

            if payment.pending:
                payment_pending.send_robust(
                    sender=self.__class__,
                    order_id=request.order_id,
                    payment=payment,
                    value=self.payment['value_paid_coin']
                )

                request.status = 'pending'
                request.save()

            else:

                # Notify payment received
                payment_received.send_robust(
                    sender=self.__class__,
                    order_id=request.order_id,
                    payment=payment,
                    value=self.payment['value_paid_coin']
                )

                if request.status not in ['received', 'done']:

                    total_received = self.payment['value_paid_coin']

                    if total_received < request.value_requested:
                        total_received = request.total_confirmed

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

    def __init__(self, request, order_id, coin, value, apikey=None):
        self._request = request
        self.order_id = order_id
        self.coin = coin
        self.value = value
        self.apikey = apikey

    def request(self, cb_params={}, params={}):

        from cryptapi.models import Request, Provider, RequestLog
        from cryptapi.cryptapi import get_address
        from cryptapi.utils import generate_nonce, build_callback_url
        from cryptapi.forms import AddressCreatedForm

        try:
            provider = Provider.objects.get(coin=self.coin, active=True)

            request_model, created = Request.objects.get_or_create(
                provider=provider,
                order_id=self.order_id,
            )

            if created is not None:
                _cb_params = {
                    'request_id': request_model.id,
                    'nonce': generate_nonce(),
                    **cb_params
                }

                cb_url = build_callback_url(self._request, _cb_params)

                _params = {
                    'address': provider.cold_wallet,
                    'callback': cb_url,
                    'pending': 1,
                    **params
                }

                if self.apikey is not None:
                    _params = {
                        'address': provider.cold_wallet,
                        'callback': cb_url,
                        'pending': 1,
                        'apikey': self.apikey,
                        **params
                    }

                response = get_address(self.coin, _params)

                rl = RequestLog(
                    request=request_model,
                    raw_data=response
                )

                rl.save()

                address_form = AddressCreatedForm(data=response, initials=_params)
                if not address_form.is_valid():
                    return None

                request_model.nonce = _cb_params['nonce']
                request_model.address_in = response['address_in']
                request_model.address_out = _params['address']
                request_model.status = 'created'
                request_model.raw_request_url = response['raw_request_url']

                request_model.set_value(self.value)

                request_model.save()

            return request_model

        except Provider.DoesNotExist:
            if not self.coin:
                raise ValueError('No provider provided')

            raise ValueError('Provider not found or not active')

    def address(self, cb_params={}, params={}):
        request = self.request(cb_params, params)

        if request:
            return request.address_in

        return None
