from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SellerProfile, Address

# Register your models here.
@admin.register(User)

class CustomerAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_seller', 'is_buyer', 'is_staff', 'is_active')
    list_filter = ('is_seller', 'is_buyer', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permission', {'fields': ('is_seller', 'is_buyer', 'is_staff', 'is_active', 'phone_number')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_seller', 'is_buyer', 'is_staff', 'is_active')
        })
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'kyc_status', 'verified', 'created_at', 'updated_at')
    list_filter = ('kyc_status', 'verified')
    search_fields = ('business_name', 'user_email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Address)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'country', 'is_default', 'address_type')
    list_filter = ('country', 'address_type', 'is_default')
    search_fields = ('user__email', 'street_address', 'city')