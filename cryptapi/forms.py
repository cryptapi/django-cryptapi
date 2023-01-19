from django import forms
from .models import Provider
from .utils import get_choices_coins


class CreateProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ('active', 'coin', 'cold_wallet')
        widgets = {
            'coin': forms.Select(attrs={}, choices=get_choices_coins())
        }


class CallbackForm(forms.Form):
    # Request data
    request_id = forms.IntegerField()
    nonce = forms.CharField(max_length=32)
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    coin = forms.ChoiceField(choices=get_choices_coins())

    # Payment data
    txid_in = forms.CharField(max_length=256)
    confirmations = forms.IntegerField()
    value_coin = forms.DecimalField(max_digits=65, decimal_places=18)
    price = forms.DecimalField(max_digits=65, decimal_places=18)
    fee_coin = forms.DecimalField(max_digits=65, decimal_places=18)

    # May be blank
    txid_out = forms.CharField(max_length=256, required=False)
    value_forwarded_coin = forms.DecimalField(max_digits=65, decimal_places=18, required=False)


class AddressCreatedForm(forms.Form):
    address_in = forms.CharField(max_length=128)
    address_out = forms.CharField(max_length=128)
    callback_url = forms.CharField(max_length=8192)
    status = forms.CharField(max_length=16)

    def __init__(self, initials, *args, **kwargs):
        super(AddressCreatedForm, self).__init__(*args, **kwargs)
        self.initials = initials

    def clean_callback_url(self):
        if self.cleaned_data['callback_url'] != self.initials['callback']:
            raise forms.ValidationError('Callback URL mismatch')

        return self.cleaned_data['callback_url']

    def clean_status(self):
        if self.cleaned_data['status'] != 'success':
            raise forms.ValidationError('Status error')

        return self.cleaned_data['status']
