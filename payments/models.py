from django.db import models
from django.core.validators import MinValueValidator
from orders.models import Order
from users.models import User, SellerProfile


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
        ('cancelled', 'Cancelled'),
        ('processing', 'Processing'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Debit/Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('digital_wallet', 'Digital Wallet'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    provider_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='NGN')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=0.00)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.id} for Order #{self.order.order_number}'


class Refund(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    reason = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    provider_refund_id = models.CharField(max_length=255, blank=True, null=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='processed_refunds')
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'refunds'
        ordering = ['-created_at']

    def __str__(self):
        return f'Refund #{self.id} for Payment #{self.payment.id}'


class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
        ('processed', 'Processed'),
    ]

    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider_payout_id = models.CharField(max_length=255, blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(max_length=3, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_details = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=Payment.PAYMENT_METHOD_CHOICES, default='card')

    class Meta:
        db_table = 'payouts'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payout #{self.id} for Seller #{self.seller.id}'


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('refund', 'Refund'),
        ('payout', 'Payout'),
        ('sale', 'Sale'),
        ('fee', 'Fee'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    payout = models.ForeignKey(Payout, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='sale')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20, choices=Payment.PAYMENT_METHOD_CHOICES, default='card')
    metadata = models.JSONField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f'Transaction #{self.id} for Payment #{self.payment.id}'