from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Tag, ProductTag



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug' : ('name',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'stock', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'sku')
    prepopulated_fields = {'slug' : ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary', 'order')
    list_filter = ('is_primary',)
    search_fields = ('product__title',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'price', 'stock', 'created_at')
    search_fields = ('product__title', 'sku')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug' : ('name',)}
    search_fields = ('name',)


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('product', 'tag')
    list_filter = ('tag',)
    search_fields = ('product__title', 'tag__name')