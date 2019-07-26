# CryptAPI's Django Library
Django's implementation of CryptAPI's payment gateway

## Requirements:

```
Python >= 3.0
Django >= 2.0
Requests >= 2.20
```



## Install


```
pip install django-cryptapi
```


[on pypi](https://pypi.python.org/pypi/django-cryptapi)
or
[on GitHub](https://github.com/cryptapi/django-cryptapi)

Add to INSTALLED_APPS:

```
INSTALLED_APPS = (
    'cryptapi',
    ...
)
```


Run migrations:

```
python3 manage.py migrate cryptapi
```


Add CryptAPI's URLs to your project's urls.py file:

```
urlpatterns = [
    path('cryptapi/', include('cryptapi.urls')),
    ...
]
```

## Configuration

After the installation you need to set up Providers for each coin you wish to accept.

You need to go into your Django Admin and create a new CryptAPI ``Provider`` for each coin with your cold wallet address where the funds will be forwarded to.

## Usage

### Creating an Invoice

In your order creation view, assuming ``user_order`` is your order object:

```
from cryptapi import Invoice
...
def order_creation_view(request):
    ...
    invoice = Invoice(
        request=request,
        order_id=user_order.id,
        coin='btc',
        value=user_order.value
    )
    
    payment_address = invoice.address()
    
    if payment_address is not None:
        # Show the payment address to the user
        ...
    else:
        # Handle request error, check RequestLogs on Admin
```

Where:

``request`` is Django's view HttpRequest object  
``order_id`` is just your order id  
``coin`` is the coin you wish to use, can be one of: ``['btc', 'eth', 'bch', 'ltc', 'xmr', 'iota']`` and you need to have a ``Provider`` set up for that coin.  
``value`` is an integer of the value of your order, either in satoshi, litoshi, wei, piconero or IOTA


### Getting notified when the user pays

```
from django.dispatch import receiver
from cryptapi.signals import payment_complete

@receiver(payment_complete)
def payment_received(order_id, payment, value):
    # Implement your logic to mark the order as paid and release the goods to the user
    ...
```

Where:  

``order_id`` is the id of the order that you provided earlier, used to fetch your order  
``payment`` is an ``cryptapi.models.Payment`` object with the payment details, such as TXID, number of confirmations, etc.  
``value`` is the value the user paid, either in satoshi, litoshi, wei or IOTA


### Helpers

This library has a couple of helpers to help you get started

``cryptapi.valid_providers()`` is a method that returns a list of tuples of the active providers that you can just feed into the choices of a ``form.ChoiceField``

``cryptapi.get_order_invoices(order_id)`` returns a list of ``cryptapi.models.Request`` objects of your order (you can have multiple objects for the same order if the user mistakenly initiated the payment with another coin)


There's also some template tags which you can import to help you with conversions and the protocols.
You just need to load ``cryptapi_helper`` on your template and use the following tags / filters:  

``{% convert_value coin value %}`` where the coin is one of ``['btc', 'eth', 'bch', 'ltc', 'xmr', 'iota']`` and the value is the value in satoshi, litoshi, wei or IOTA, will convert to the main coin denomination.  


``{{ coin|coin_name }}`` will output the properly formatted cryptocurrency name  

## Help

Need help?  
Contact us @ https://cryptapi.io/contact/