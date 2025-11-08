from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product, ProductVariant


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('returned', 'Returned'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='NGN')
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
    customer_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']


    def __str__(self):
        return f"Order #{self.order_number} by {self.buyer.email}"
    

    def save(self, *args, **kwargs):
        if not self.order_number:

            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        super().save(*args, **kwargs)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=200)
    product_sku = models.CharField(max_length=100)
    attributes = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'order_items'


    def __str__(self):
        return f"{self.product_name} * {self.quantity}"
    

    @property
    def total_price(self):
        return self.quantity * self.price



class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    estimated_days = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'shipping_methods'
    

    def __str__(self):
        return self.name
    

class OrderShipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_info')
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.PROTECT)
    tracking_number = models.CharField(max_length=100, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'shipping_info'



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'carts'


    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product', 'variant']


    def __str__(self):
        return f"{self.product.title} * {self.quantity}"
    

    def unit_price(self):
        if self.variant:
            return self.variant.price
        return self.product.price
    

    @property
    def total_price(self):
        return self.unit_price * self.quantity