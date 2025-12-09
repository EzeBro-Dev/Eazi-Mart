from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, SellerProfile, UserProfile, Address


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 
                 'password', 'password2', 'is_seller', 'is_buyer')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class SellerProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = SellerProfile
        fields = '_all_'
        read_only_fields = ('user', 'verified', 'kyc_status', 'created_at', 'updated_at')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '_all_'
        read_only_fields = ('user', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    seller_profile = SellerProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number',
                 'is_seller', 'is_buyer', 'email_verified', 'phone_verified',
                 'profile', 'seller_profile', 'addresses', 'date_joined')
        read_only_fields = ('id', 'email_verified', 'phone_verified', 'date_joined')