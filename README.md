[<img src="https://i.imgur.com/IfMAa7E.png" width="300"/>](image.png)


# CryptAPI's Django Library
Django's implementation of CryptAPI's payment gateway

## Requirements:

```
Python >= 3.0
Django >= 2.0
Requests >= 2.20
```



## Install


```shell script
pip install django-cryptapi
```


[on pypi](https://pypi.python.org/pypi/django-cryptapi)
or
[on GitHub](https://github.com/cryptapi/django-cryptapi)

Add to INSTALLED_APPS:

```python
INSTALLED_APPS = (
    'cryptapi',
    ...
)
```


Run migrations:

```shell script
python3 manage.py migrate cryptapi
```

Collect static files:

```shell script
python3 manage.py collectstatic
```

Add CryptAPI's URLs to your project's urls.py file:

```python
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

* ##### If you want the address generated:

```python
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

* ##### If you want the `cryptapi.models.Request` object:

```python
from cryptapi import Invoice
...
def order_creation_view(request):
    ...
    invoice = Invoice(
        request=request, # This if your view request. It's meant to create the callback URL
        order_id=user_order.id,
        coin='btc',
        value=user_order.value
    )
    
    payment_request = invoice.request()
    
    if payment_request is not None:
        # Show the payment address to the user
        ...
    else:
        # Handle request error, check RequestLogs on Admin
```

#### Where:

``request`` is Django's view HttpRequest object  

``order_id`` is just your order id  

``coin`` is the ticker of the coin you wish to use, any of our supported coins (https://cryptapi.io/cryptocurrencies/). You need to have a ``Provider`` set up for that coin.  

``value`` is an integer of the value of your order, either in satoshi, litoshi, wei, piconero or IOTA

&nbsp;

### Getting notified when the user pays

```python
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


#### Important:
>
>Don't forget to import your signals file. 
>
>On your App's `apps.py` file:
>
>```python
>class MyAppConfig(AppConfig):
>    name = 'MyApp'
>    
>    def ready(self):
>        super(MyAppConfig, self).ready()
>
>        # noinspection PyUnresolvedReferences
>        import MyApp.signals
>```
>[django docs](https://docs.djangoproject.com/en/3.0/topics/signals/#django.dispatch.receiver)



### Using our provided interface

Create a view in ``views.py``

```python
def payment(_r, request_id):
    try:
        req = Request.objects.get(id=request_id)
        coin = req.provider.coin

        qrcode = get_qrcode(coin, req.address_in)

        fiat = get_conversion(coin, 'eur', req.value_requested)

        print(fiat)

        ctx = {
            'req': req,
            'qrcode': qrcode,
            'fiat': fiat['value_coin']
        }

        return render(_r, 'payment.html', context=ctx)

    except Request.DoesNotExist:
        pass

    return redirect('store:request')
```
In your template HTML

```djangotemplate
{% extends 'base.html' %}
{% load cryptapi_helper %}
{% block content %}
    {% generate_payment_template %}
{% endblock %}
```

&nbsp;


### Helpers

This library has a couple of helpers to help you get started. They are present in the file ``utils.py``.

``cryptapi.valid_providers()`` is a method that returns a list of tuples of the active providers that you can just feed into the choices of a ``form.ChoiceField``

``cryptapi.get_order_invoices(order_id)`` returns a list of ``cryptapi.models.Request`` objects of your order (you can have multiple objects for the same order if the user mistakenly initiated the payment with another coin or if he mistakenly didn't send the full payment)

``cryptapi.callback_url(_r, params)`` build your callback URL to provide to ``get_request``. Should be used inside a view since ``_r = request``

&nbsp;

### CryptAPI Helper

This is the helper responsible for the connections ot the API itself. All these functions are in the ``cryptapi.py`` file. 

``get_info(coin)`` returns the information of all cryptocurrencies or just if ``coin=''`` or a specific cryptocurrency if ``coin='ltc'`` for example. [docs](https://docs.cryptapi.io/#operation/info)

``get_supported_coins()`` returns all the support cryptocurrencies. You can consult them in this [list](https://cryptapi.io/fees/). 

``get_logs(coin, callback_url)`` returns all the callback logs related to a request. ``callback_url`` should be the callback provided to our API. [docs](https://docs.cryptapi.io/#operation/logs)

``get_qrcode(coin, address, value, size)`` returns a PNG of a QR Code with the address for payment. [docs](https://docs.cryptapi.io/tag/Bitcoin#operation/btcqrcode)

``get_conversion(origin, to, value)`` returns the converted value in the parameter ``value_coin`` to the currency you wish, FIAT or Cryptocurrency.

``get_estimate(coin)`` returns the estimation of the blockchain fees for the cryptocurrency specified in the parameter ``coin``. E.g: ``get_estimate('trc20_usdt')`` [docs](https://docs.cryptapi.io/#operation/estimate)

``get_address(coin, address_out, callback_url, pending, api_key)`` requests a payment address to CryptAPI. If you don't wish to use [BlockBee](https://dash.blockbee.io/), you can leave ``api_key`` empty. [docs](https://docs.cryptapi.io/#operation/create)

&nbsp;

### How to use the QR code (with address, coin and value)

To generate a QR Code you must use ``get_qrcode`` in your view and feed the parameters to your template. To generate a QR Code image you must place content of the API response after ``data:image/png;base64,{{qr_code}}`` so the browser generates the QR Code.
```djangotemplate
<img src="data:image/png;base64,{{ qrcode.qr_code }}" alt="Payment QR Code"/>
```

You can also make the QR Code clickable.

```djangotemplate
<a href='{{ qrcode.payment_uri }}'>
    <img src="data:image/png;base64,{{ qrcode.qr_code }}" alt="Payment QR Code"/>
</a>
```

You can also add a value to the QR Code setting the ``value`` parameter to the value of your order (e.g ``0.2 LTC``). This may not function correctly in some wallets. **Use at your own risk.**

## What is the Store application?

We made the ``store`` application to provide you with code examples on how to implement our service. It also has the code for our suggested UI (both CSS and HTML).


## Help

Need help?  
Contact us @ https://cryptapi.io/contacts/


### Changelog 

#### 0.1.2
* Version bump

#### 0.1.3
* Pending transactions (through the `payment_pending` signal)
* Monero

#### 0.1.5
* Fixed bug with MySQL database varchar length limitations
* Added build payment URI tag, to help you generate payment URIs to feed into any QR Code generator

#### 0.2.0
* Added ERC-20 token support
* Added payment QR code
* Improved documentation
* Fixed bugs

#### 0.2.7
* Added coin info helper

#### 0.3.1
* New API URL
* New general info API

#### 0.4.0
* Support for BlockBee
* Fetch all supported cryptocurrencies and cache them
* Updated API Helper
* Added conversion endpoint
* Added support for BlockBee API Key
* Added UI for payments
* Added store application to provide examples on how to implement
* General improvements
* Fixed bugs

#### 0.4.1
* Minor bugfixes

#### 0.4.2
* Minor fixes
* Signals now use the value_coin
* Removed deprecated fields from the payment model

#### 0.4.3
* Minor fixes