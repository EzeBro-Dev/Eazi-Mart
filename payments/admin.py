from django.contrib import admin
from .models import Payment, Refund, Payout, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'status', 'amount', 'currency', 'fee_amount', 'net_amount', 'created_at', 'updated_at', 'paid_at')
    list_filter = ('status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('order__order_number', 'payment_id')
    readonly_fields = ('created_at', 'updated_at', 'paid_at')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'refund_id', 'amount', 'currency', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order__order_number', 'refund_id')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('order', 'payout_id', 'amount', 'currency', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order__order_number', 'payout_seller__business_name')
    readonly_fields = ('created_at', 'updated_at')