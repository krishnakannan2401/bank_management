from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import random
import string


class Customer(models.Model):
    """Customer model extending Django User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.username}"
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Account(models.Model):
    """Bank Account model"""
    ACCOUNT_TYPE_CHOICES = [
        ('Saving', 'Saving'),
        ('Current', 'Current'),
    ]
    
    account_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='account')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='Saving')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), 
                                  validators=[MinValueValidator(Decimal('0.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            # Generate unique account number
            while True:
                account_num = ''.join(random.choices(string.digits, k=12))
                if not Account.objects.filter(account_number=account_num).exists():
                    self.account_number = account_num
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.account_number} - {self.customer.user.username}"
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Transaction(models.Model):
    """Transaction model for deposits, withdrawals, and transfers"""
    TRANSACTION_TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer', 'Transfer'),
    ]
    
    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, 
                                validators=[MinValueValidator(Decimal('0.01'))])
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # For transfer transactions
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='received_transactions')
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Generate unique transaction ID
            while True:
                trans_id = 'TXN' + ''.join(random.choices(string.digits, k=10))
                if not Transaction.objects.filter(transaction_id=trans_id).exists():
                    self.transaction_id = trans_id
                    break
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - ₹{self.amount}"
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']

