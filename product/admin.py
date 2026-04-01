from django.contrib import admin
from .models import Product, ProductImage
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['pk', 'title', 'price', 'quantity','discount', 'available', 'created_at', 'updated_at']
    ordering = ['-created_at']
    list_filter = ['available', 'category']
    list_display_links = ['title',]
    prepopulated_fields = {'slug': ('title',)}




@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'img', 'product', 'created_at', 'updated_at']
    ordering = ['-created_at']

    list_display_links = ['img',]
    raw_id_fields = ['product',]