# Importing necessary modules from Django admin and local models
from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, OrderShipping, Cart, CartItem


# Define an inline admin class to display OrderItem objects within an Order in the admin panel
class OrderItemInline(admin.TabularInline):
    model = OrderItem  # Specifies the related model (OrderItem)
    extra = 0  # Prevents Django from showing extra empty rows by default
    readonly_fields = ('product_name', 'product_sku', 'price')  # Makes these fields read-only in the inline form


# Register the Order model in Django admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the Order model
    list_display = ('order_number', 'buyer', 'status', 'total_amount', 'created_at')
    # Add filters on the right side of the admin list page
    list_filter = ('status', 'created_at')
    # Allows search functionality for these fields
    search_fields = ('order_number', 'buyer__email')
    # Fields that cannot be edited directly in the admin
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    # Displays related OrderItems inline within the Order admin page
    inlines = [OrderItemInline]


# Register the OrderItem model in Django admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('order', 'product_name', 'quantity', 'price', 'created_at')
    # Adds filters by creation date
    list_filter = ('created_at',)
    # Enables search by order number or product name
    search_fields = ('order__order_number', 'product_name')
    # Makes 'created_at' uneditable
    readonly_fields = ('created_at',)


# Register the ShippingMethod model in Django admin
@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('name', 'price', 'is_active', 'estimated_days')
    # Filter by whether the shipping method is active
    list_filter = ('is_active',)
    # Enable searching by shipping method name
    search_fields = ('name',)


# Register the OrderShipping model in Django admin
@admin.register(OrderShipping)
class OrderShippingAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('order', 'shipping_method', 'tracking_number', 'shipped_at')
    # Add filtering option for shipment date
    list_filter = ('shipped_at',)
    # Enable search by order number or tracking number
    search_fields = ('order__order_number', 'tracking_number')


# ⚠️ Note: The following registration mistakenly uses the same class name twice (CartItemAdmin).
# The first one should manage Cart, not CartItem — we’ll still explain both below.

# Register the Cart model in Django admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):  # Changed class name from CartItemAdmin to CartAdmin for clarity
    list_display = ('user', 'total_items', 'updated_at', 'subtotal')
    readonly_fields = ('created_at', 'updated_at')
    
    
# Register the CartItem model in Django admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # Columns displayed in the CartItem list view
    list_display = ('cart', 'product', 'variant', 'quantity', 'updated_at')
    # Adds filter by last update date
    list_filter = ('updated_at',)
    # Enables search by user's email or product title
    search_fields = ('cart__user__email', 'product__title')


# End of admin configuration — this registers all models to appear in the Django admin panel.