from django import forms
from .choices import COINS


class CallbackForm(forms.Form):

    # Request data
    request_id = forms.IntegerField()
    nonce = forms.CharField(max_length=32)
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    coin = forms.ChoiceField(choices=COINS)

    # Payment data
    txid_in = forms.CharField(max_length=256)
    txid_out = forms.CharField(max_length=256)
    confirmations = forms.IntegerField()
    value = forms.DecimalField(max_digits=65, decimal_places=0)
    value_forwarded = forms.DecimalField(max_digits=65, decimal_places=0)


class AddressCreatedForm(forms.Form):
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    callback_url = forms.CharField(max_length=16384)
    status = forms.CharField(max_length=16)

    def __init__(self, initials, *args, **kwargs):
        super(AddressCreatedForm, self).__init__(*args, **kwargs)
        self.initials = initials

    def clean_address_out(self):
        if self.cleaned_data['address_out'] != self.initials['address_out']:
            raise forms.ValidationError

        return self.cleaned_data['address_out']

    def clean_callback_url(self):
        if self.cleaned_data['callback_url'] != self.initials['callback_url']:
            raise forms.ValidationError

        return self.cleaned_data['callback_url']

    def clean_status(self):
        if self.cleaned_data['status'] != 'success':
            raise forms.ValidationError

        return self.cleaned_data['status']
