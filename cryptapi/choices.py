from django.utils.translation import gettext_lazy as _

STATUS = (
    ('created', _('Created')),
    ('pending', _('Pending')),
    ('insufficient', _('Payment Insufficient')),
    ('received', _('Received')),
    ('done', _('Done')),
)