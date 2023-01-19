from django.db import models
from django.db.models import Sum
from django.db.utils import OperationalError
from django.utils.translation import gettext_lazy as _
from .choices import STATUS
from .cryptapi import get_supported_coins


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    coin = models.CharField(_('Coin'), max_length=16, unique=True)
    cold_wallet = models.CharField(_('Cold Wallet'), max_length=128)
    active = models.BooleanField(_('Active'), default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_coin_display(self):
        coin_display = ''

        coins = Metadata.get().coins.items()

        if coins is None:
            coins = get_supported_coins().items()

        for ticker, coin in coins:
            if ticker == self.coin:
                coin_display = coin

        if coin_display is None:
            return self.coin.upper()

        return coin_display

    def __str__(self):
        return "{}".format(self.get_coin_display())


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(_('Order ID'), default='', max_length=128)
    nonce = models.CharField(_('Nonce'), max_length=32, default='')
    address_in = models.CharField(_('Payment Address'), max_length=128, default='', null=True)
    address_out = models.CharField(_('Receiving Address'), max_length=128, default='', null=True)
    value_requested = models.DecimalField(_('Value Requested'), default=0, max_digits=65, decimal_places=18)
    status = models.CharField(_('Status'), choices=STATUS, max_length=16, default='', null=True)
    raw_request_url = models.CharField(_('Request URL'), max_length=8192, default='', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        qs = self.payment_set.all()

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    @property
    def total_pending(self):
        qs = self.payment_set.filter(pending=True)

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    @property
    def total_confirmed(self):
        qs = self.payment_set.filter(pending=False)

        if qs.exists():
            return qs.aggregate(sum=Sum('value_paid')).get('sum', 0)

        return 0

    def set_value(self, value, commit=False):
        _coin = self.provider.get_coin_display()

        self.value_requested = value

        if commit:
            self.save()

    def __str__(self):
        return "#{}, {}#{}, {} ({})".format(self.id, _('Order'), self.order_id, self.get_status_display(), self.timestamp.strftime('%x %X'))

    class Meta:
        unique_together = (('provider', 'order_id'),)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    value_paid_coin = models.DecimalField(_('Value Paid Coin'), default=0, max_digits=65, decimal_places=18)
    value_received_coin = models.DecimalField(_('Value Received Coin'), default=0, max_digits=65, decimal_places=18)
    value_fee_coin = models.DecimalField(_('Fee Coin'), default=0, max_digits=65, decimal_places=18,
                                         help_text="CryptAPI Fee.")
    value_price = models.DecimalField(_('Price Coin in USD'), default=0, max_digits=65, decimal_places=18,
                                      help_text="Coin price in USD at the time of receiving.")
    txid_in = models.CharField(_('TXID in'), max_length=256, default='')
    txid_out = models.CharField(_('TXID out'), max_length=256, default='')
    pending = models.BooleanField(default=True)
    confirmations = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def coin(self):
        return self.request.provider.get_coin_display()

    def __str__(self):
        return "#{}, {}, {} ({})".format(self.request.id, self.value_paid_coin, self.request.provider.get_coin_display(), self.timestamp.strftime('%x %X'))


class RequestLog(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.request_id, self.timestamp.strftime('%x %X'))


class PaymentLog(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    raw_data = models.CharField(max_length=8192)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#{} ({})".format(self.payment_id, self.timestamp.strftime('%x %X'))


class Metadata(models.Model):
    id = models.AutoField(primary_key=True)
    coins = models.JSONField(default=dict, max_length=5048)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#{}'.format(self.id)

    @classmethod
    def get(cls, key=None, default=None):
        try:
            try:
                _metadata = cls.objects.get(id=1)

                if key:
                    return getattr(_metadata, key, default)

                return _metadata

            except cls.DoesNotExist:
                pass
        except OperationalError:
            pass

        return default

    @classmethod
    def set(cls, key, value):
        try:
            _settings, created = cls.objects.get_or_create(id=1)
            setattr(_settings, key, value)
            _settings.save()
        except OperationalError:
            pass

    class Meta:
        verbose_name = verbose_name_plural = 'Meta Data'
