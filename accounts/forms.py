from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Account, Transaction
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Address'
    }))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    pincode = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Pincode'
    }))
    account_type = forms.ChoiceField(choices=Account.ACCOUNT_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    initial_deposit = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        required=True,
        validators=[MinValueValidator(Decimal('500.00'))],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum ₹500',
            'min': '500',
            'step': '0.01'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class DepositForm(forms.Form):
    """Form for deposit transactions"""
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount',
            'min': '0.01',
            'step': '0.01'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Transaction description (optional)'
        })
    )


class WithdrawForm(forms.Form):
    """Form for withdrawal transactions"""
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount',
            'min': '0.01',
            'step': '0.01'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Transaction description (optional)'
        })
    )


class TransferForm(forms.Form):
    """Form for transfer transactions"""
    to_account_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient account number'
        })
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount',
            'min': '0.01',
            'step': '0.01'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Transaction description (optional)'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating customer profile"""
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'city', 'state', 'pincode']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
        }

