from django.contrib import admin
from .models import Customer, Account, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    list_editable = ['is_approved']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'customer', 'account_type', 'balance', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['account_number', 'customer__user__username']
    list_editable = ['is_active']
    readonly_fields = ['account_number', 'created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'account', 'transaction_type', 'amount', 'balance_after_transaction', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['transaction_id', 'account__account_number']
    readonly_fields = ['transaction_id', 'created_at']
    date_hierarchy = 'created_at'

