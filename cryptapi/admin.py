from django.contrib import admin
from cryptapi.models import Provider, Request, Payment, RequestLog, PaymentLog


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProviderAdmin(admin.ModelAdmin):
    add_fieldsets = (
        ('Coin', {
            'fields': ('coin',),
            'description': 'Select provider coin'
        }),
        ('Cold Wallet', {
            'fields': ('cold_wallet',),
            'description': "Insert your cold wallet's address"
        }),
        ('Active', {
            'fields': ('active',),
            'description': "Enable this provider"
        }),
    )

    fieldsets = (
        ('Coin', {
            'fields': ('coin', ),
            'description': 'Select provider coin'
        }),
        ('Cold Wallet', {
            'fields': ('cold_wallet', ),
            'description': "Insert your cold wallet's address"
        }),
        ('Active', {
            'fields': (('active',), ('last_updated', ), ),
            'description': "Enable this provider"
        }),
    )

    readonly_fields = ('last_updated', )


admin.site.register(Provider)
admin.site.register(Request, ReadOnlyAdmin)
admin.site.register(RequestLog, ReadOnlyAdmin)
admin.site.register(Payment, ReadOnlyAdmin)
admin.site.register(PaymentLog, ReadOnlyAdmin)
