from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'total_quantity', 'status', 'is_paid', 'created_at']
    ordering = ['-created_at']
    list_filter = ['is_paid', 'status']
    raw_id_fields = ['user']
    list_display_links = ['user']
    search_fields = ['user']




@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price_at_purchase']
    raw_id_fields = ['order', 'product']
    search_fields = ['order']
    list_display_links = ['order']