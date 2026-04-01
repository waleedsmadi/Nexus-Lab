from django.contrib import admin
from .models import Wallet, Transaction



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance']
    list_display_links = ['user',]
    raw_id_fields = ['user',]
    search_fields = ['user',]



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'amount', 'transaction_type', 'created_at']
    list_filter = ['transaction_type',]
    list_display_links = ['wallet',]
    raw_id_fields = ['wallet',]
