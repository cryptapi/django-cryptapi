import json
from django.http import HttpResponse
from cryptapi.forms import CallbackForm
from cryptapi.dispatchers import CallbackDispatcher


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
            'value_paid': form.cleaned_data.get('value'),
            'value_paid_coin': form.cleaned_data.get('value_coin'),
            'confirmations': form.cleaned_data.get('confirmations'),
            'txid_out': form.cleaned_data.get('txid_out'),
            'value_received': form.cleaned_data.get('value_forwarded'),
            'value_received_coin': form.cleaned_data.get('value_forwarded_coin')
        }

        raw_data = json.dumps(_r.GET)

        dispatcher = CallbackDispatcher(coin, request, payment, raw_data, result=result)

        if dispatcher.callback():
            return HttpResponse('*ok*')

    return HttpResponse('Error')
