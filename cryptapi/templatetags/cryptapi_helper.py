from django import template

register = template.Library()


@register.inclusion_tag('cryptapi/payment.html', takes_context=True)
def generate_payment_template(context):
    return {
        'req': context['req'],
        'qrcode': context['qrcode'],
        'fiat': context['fiat'],
    }