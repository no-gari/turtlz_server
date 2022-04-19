from django.contrib import admin
from api.commerce.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at']
    readonly_fields = ['user', 'merchant_uid', 'amount', 'status', 'created_at']
