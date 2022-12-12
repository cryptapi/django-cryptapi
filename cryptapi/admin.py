from django.contrib import admin
from .models import Provider, Request, Payment, RequestLog, PaymentLog, Metadata
from .forms import CreateProviderForm


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
    readonly_fields = ['last_updated']
    form = CreateProviderForm


class MetadataAdmin(ReadOnlyAdmin):
    list_display = ('__str__', 'last_updated',)


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Request, ReadOnlyAdmin)
admin.site.register(RequestLog, ReadOnlyAdmin)
admin.site.register(Payment, ReadOnlyAdmin)
admin.site.register(PaymentLog, ReadOnlyAdmin)
admin.site.register(Metadata, MetadataAdmin)