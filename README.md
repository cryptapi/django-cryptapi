![CryptAPI](https://i.imgur.com/IfMAa7E.png)

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
        request=request,
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
``coin`` is the ticker of the coin you wish to use, any of our supported coins (https://cryptapi.io/pricing/). You need to have a ``Provider`` set up for that coin.  
``value`` is an integer of the value of your order, either in satoshi, litoshi, wei, piconero or IOTA


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


&nbsp;


>#### Important:
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


&nbsp;


### Helpers

This library has a couple of helpers to help you get started

``cryptapi.valid_providers()`` is a method that returns a list of tuples of the active providers that you can just feed into the choices of a ``form.ChoiceField``

``cryptapi.get_order_invoices(order_id)`` returns a list of ``cryptapi.models.Request`` objects of your order (you can have multiple objects for the same order if the user mistakenly initiated the payment with another coin)


### Template Tags
There's also some template tags which you can import to help you with conversions and the protocols.
You just need to load ``cryptapi_helper`` on your template and use the following tags / filters:  

* #### QR code (with `cryptapi.models.Request` object)
If you want the library to generate and display a clickable QR code for you, just use our `generate_qrcode_for_request`, like this:

```djangotemplate
{% generate_qrcode_for_request payment_request %}
```

You just need to feed it the `payment_request` object created with `invoice.request()` 

The QR code that can also be clicked on mobile devices to launch the user's wallet.

* #### QR code (with address, coin and value)
If you want the library to generate and display a clickable QR code for you, just use our `generate_qrcode`, like this:

```djangotemplate
{% generate_qrcode btc 1PE5U4temq1rFzseHHGE2L8smwHCyRbkx3 0.001 %}
```

It takes 3 arguments: the coin, the payment address and the value in the main denomination of the coin, and it will output a neat QR code for your page. 

The QR code that can also be clicked on mobile devices to launch the user's wallet.

##### Example:
```djangotemplate
{% load cryptapi_helper %}
<body>
    <div class="row">
        <div class="col-sm-12">
            {% generate_qrcode btc 1PE5U4temq1rFzseHHGE2L8smwHCyRbkx3 0.001 %}
        </div>
    </div>
</body>
```

* #### Payment URI
If you just want to build a full payment URI to plug into your own QR code, you can use our `build_payment_uri` tag, like so:

```djangotemplate
{% build_payment_uri btc 1PE5U4temq1rFzseHHGE2L8smwHCyRbkx3 0.001 %}
```

It will output: `bitcoin:1PE5U4temq1rFzseHHGE2L8smwHCyRbkx3?amount=0.001`

Same arguments as for the QR code

* #### Helpers

``{% convert_value coin value %}`` where the coin is the coin ticker and the value is the value in satoshi, litoshi, wei or IOTA, will convert to the main coin unit.  


``{{ coin|coin_name }}`` will output the properly formatted cryptocurrency name.


## Help

Need help?  
Contact us @ https://cryptapi.io/contact/