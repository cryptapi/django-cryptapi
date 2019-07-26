import json
from django.http import HttpResponse
from cryptapi.forms import CallbackForm, BaseCallbackForm
from cryptapi.dispatchers import CallbackDispatcher


def callback(_r):

    pending = _r.GET.get('pending', False)

    if not pending:
        form = CallbackForm(data=_r.GET)
    else:
        form = BaseCallbackForm(data=_r.GET)

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
            'confirmations': form.cleaned_data.get('confirmations'),
        }

        if not pending:
            payment['txid_out'] = form.cleaned_data.get('txid_out')
            payment['value_received'] = form.cleaned_data.get('value_forwarded')

        raw_data = json.dumps(_r.GET)

        dispatcher = CallbackDispatcher(coin, request, payment, raw_data, pending=pending)

        if dispatcher.callback():
            return HttpResponse('*ok*')

    return HttpResponse('Error')
