from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem, ShippingMethod


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '_all_'
        read_only_fields = ('order', 'product_name', 'product_sku', 'price')

    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        first_image = obj.product.images.first()
        if first_image:
            return first_image.image.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_email = serializers.EmailField(source='buyer.email', read_only=True)
    shipping_info = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '_all_'
        read_only_fields = ('order_number', 'buyer', 'created_at', 'updated_at')

    def get_shipping_info(self, obj):
        shipping_info = getattr(obj, 'shipping_info', None)
        if shipping_info:
            from orders.serializer import OrderShippingSerializer
            return OrderShippingSerializer(shipping_info).data
        return None


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = '_all_'
        read_only_fields = ('cart', 'created_at', 'updated_at')

    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        first_image = obj.product.images.first()
        if first_image:
            return first_image.image.url
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = '_all_'
        read_only_fields = ('user', 'created_at', 'updated_at')


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '_all_'


class OrderShippingSerializer(serializers.ModelSerializer):
    shipping_method_name = serializers.CharField(source='shipping_method.name', read_only=True)

    class Meta:
        model = Order
        fields = '_all_'