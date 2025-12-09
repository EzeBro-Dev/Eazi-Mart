from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '_all_'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '_all_'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '_all_'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    seller_business_name = serializers.CharField(source='seller.business_name', read_only=True)
    seller_verified = serializers.BooleanField(source='seller.verified', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '_all_'
        read_only_fields = ('seller', 'slug', 'created_at', 'updated_at')


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    seller_business_name = serializers.CharField(source='seller.business_name', read_only=True)
    seller_verified = serializers.BooleanField(source='seller.verified', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'price', 'compare_price', 'currency',
                 'stock', 'status', 'primary_image', 'seller_business_name',
                 'seller_verified', 'average_rating', 'review_count', 'created_at')

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '_all_'