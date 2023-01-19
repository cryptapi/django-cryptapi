import json
from decimal import *
from django.http import HttpResponse, JsonResponse
from cryptapi.forms import CallbackForm
from cryptapi.dispatchers import CallbackDispatcher
from cryptapi.models import Payment, Request
import datetime


def callback(_r):
    result = _r.GET.get('result')
    form = CallbackForm(data=_r.GET)

    if form.is_valid():

        # Request data
        coin = form.cleaned_data.get('coin')

        request = {
            'id': form.cleaned_data.get('request_id'),
            'nonce': form.cleaned_data.get('nonce'),
            'address_in': form.cleaned_data.get('address_in'),
            'address_out': form.cleaned_data.get('address_out'),
        }

        # Payment data
        payment = {
            'txid_in': form.cleaned_data.get('txid_in'),
            'value_paid_coin': form.cleaned_data.get('value_coin'),
            'confirmations': form.cleaned_data.get('confirmations'),
            'txid_out': form.cleaned_data.get('txid_out'),
            'value_received_coin': form.cleaned_data.get('value_forwarded_coin'),
            'value_price': form.cleaned_data.get('price'),
            'value_fee_coin': form.cleaned_data.get('fee_coin')
        }

        raw_data = json.dumps(_r.GET)

        dispatcher = CallbackDispatcher(coin, request, payment, raw_data, result=result)

        if dispatcher.callback():
            return HttpResponse('*ok*')

    return HttpResponse('Error')


def status(_r):
    request_id = _r.GET.get('request_id')

    request = Request.objects.get(id=request_id)
    payment_qs = Payment.objects.all().filter(request_id=request_id)

    already_paid = 0
    remaining = request.value_requested
    is_paid = 0
    is_pending = 0

    if request.status == 'done':
        is_paid = 1

    if request.status == 'pending':
        is_pending = 1

    payments = [{
        'coin': p.request.provider.get_coin_display(),
        'value_coin': p.value_paid_coin.normalize(),
        'timestamp': datetime.datetime.strftime(p.timestamp, '%d/%m/%y %H:%M:%S'),
    } for p in payment_qs]

    for p in payments:
        already_paid += p['value_coin']
        remaining -= p['value_coin']

    data = {
        'is_paid': is_paid,
        'is_pending': is_pending,
        'crypto_total': Decimal(request.value_requested).normalize(),
        'already_paid': Decimal(already_paid).normalize(),
        'remaining': Decimal(remaining).normalize(),
        'fiat_symbol': '€',
    }

    return JsonResponse({'status': 'success', 'data': data, 'payments': payments})
