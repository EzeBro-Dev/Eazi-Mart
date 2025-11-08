from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    is_seller = models.BooleanField(_('is seller'), default=False)
    is_buyer = models.BooleanField(_('is buyer'), default=True)
    email_verified = models.BooleanField(_('email verified'), default=False)
    phone_verified = models.BooleanField(_('phone verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'


    def __str__(self):
        return self.email
    

class SellerProfile(models.Model):

    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile',
    )

    business_name = models.CharField(_('business Name'), max_length=255, blank=True, null=True)
    business_description = models.TextField(blank=True)
    business_address = models.TextField(blank=True)
    business_phone = models.CharField(_('business phone'), max_length=20, blank=True, null=True)
    verified = models.BooleanField(_('verified'), default=False)
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default='pending'
    )
    kyc_documents = models.JSONField(default=dict, blank=True)  # Store file URLs
    payout_info = models.JSONField(default=dict, blank=True) # Bank/Stripe details
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'seller_profile'

    def __str__(self):
        return f"{self.business_name} - {self.user.email}"
    

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
        ('both', 'Both'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES,
        default='shipping'
    )
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'addresses'


    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"