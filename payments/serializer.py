from rest_framework import serializers
from .models import Payment, Refund, Payout, Transaction


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    buyer_email = serializers.EmailField(source='order.buyer.email', read_only=True)

    class Meta:
        model = Payment
        fields = '_all_'
        read_only_fields = ('order', 'created_at', 'updated_at', 'paid_at')


class RefundSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    processed_by_email = serializers.EmailField(source='processed_by.email', read_only=True)

    class Meta:
        model = Refund
        fields = '_all_'
        read_only_fields = ('payment', 'order', 'processed_by', 'created_at', 'updated_at', 'processed_at')


class PayoutSerializer(serializers.ModelSerializer):
    seller_business_name = serializers.CharField(source='seller.business_name', read_only=True)
    seller_user_email = serializers.EmailField(source='seller.user.email', read_only=True)

    class Meta:
        model = Payout
        fields = '_all_'
        read_only_fields = ('seller', 'created_at', 'updated_at', 'processed_at')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '_all_'
        read_only_fields = ('created_at',)