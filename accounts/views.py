from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Customer, Account, Transaction
from .forms import (
    UserRegistrationForm, DepositForm, WithdrawForm, 
    TransferForm, ProfileUpdateForm
)
from django.conf import settings


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser


def home(request):
    """Home page"""
    return render(request, 'accounts/home.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            customer = Customer.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )
            # Create account with initial deposit
            initial_deposit = form.cleaned_data['initial_deposit']
            account = Account.objects.create(
                customer=customer,
                account_type=form.cleaned_data['account_type'],
                balance=initial_deposit
            )
            # Create initial deposit transaction
            Transaction.objects.create(
                account=account,
                transaction_type='Deposit',
                amount=initial_deposit,
                balance_after_transaction=initial_deposit,
                description='Initial deposit'
            )
            messages.success(request, 'Account created successfully! Please wait for admin approval.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if customer is approved
            try:
                customer = Customer.objects.get(user=user)
                if not customer.is_approved:
                    messages.warning(request, 'Your account is pending approval. Please wait for admin approval.')
                    return render(request, 'accounts/login.html')
            except Customer.DoesNotExist:
                pass
            
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    """User dashboard"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        # Get recent transactions
        recent_transactions = Transaction.objects.filter(account=account)[:5]
        
        context = {
            'customer': customer,
            'account': account,
            'recent_transactions': recent_transactions,
        }
        return render(request, 'accounts/dashboard.html', context)
    except (Customer.DoesNotExist, Account.DoesNotExist):
        messages.error(request, 'Account not found. Please contact administrator.')
        return redirect('home')


@login_required
def deposit(request):
    """Deposit money view"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        if not customer.is_approved:
            messages.error(request, 'Your account is not approved yet.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                description = form.cleaned_data.get('description', 'Deposit')
                
                with transaction.atomic():
                    account.balance += amount
                    account.save()
                    
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=amount,
                        balance_after_transaction=account.balance,
                        description=description
                    )
                
                messages.success(request, f'Successfully deposited ₹{amount}. New balance: ₹{account.balance}')
                return redirect('dashboard')
        else:
            form = DepositForm()
        
        return render(request, 'accounts/deposit.html', {'form': form, 'account': account})
    except (Customer.DoesNotExist, Account.DoesNotExist):
        messages.error(request, 'Account not found.')
        return redirect('dashboard')


@login_required
def withdraw(request):
    """Withdraw money view"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        if not customer.is_approved:
            messages.error(request, 'Your account is not approved yet.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                description = form.cleaned_data.get('description', 'Withdrawal')
                
                if amount > account.balance:
                    messages.error(request, 'Insufficient balance!')
                    return render(request, 'accounts/withdraw.html', {'form': form, 'account': account})
                
                with transaction.atomic():
                    account.balance -= amount
                    account.save()
                    
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Withdraw',
                        amount=amount,
                        balance_after_transaction=account.balance,
                        description=description
                    )
                
                messages.success(request, f'Successfully withdrew ₹{amount}. New balance: ₹{account.balance}')
                return redirect('dashboard')
        else:
            form = WithdrawForm()
        
        return render(request, 'accounts/withdraw.html', {'form': form, 'account': account})
    except (Customer.DoesNotExist, Account.DoesNotExist):
        messages.error(request, 'Account not found.')
        return redirect('dashboard')


@login_required
def transfer(request):
    """Transfer money view"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        if not customer.is_approved:
            messages.error(request, 'Your account is not approved yet.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = TransferForm(request.POST)
            if form.is_valid():
                to_account_number = form.cleaned_data['to_account_number']
                amount = form.cleaned_data['amount']
                description = form.cleaned_data.get('description', 'Transfer')
                
                if amount > account.balance:
                    messages.error(request, 'Insufficient balance!')
                    return render(request, 'accounts/transfer.html', {'form': form, 'account': account})
                
                try:
                    to_account = Account.objects.get(account_number=to_account_number, is_active=True)
                    if to_account == account:
                        messages.error(request, 'Cannot transfer to your own account!')
                        return render(request, 'accounts/transfer.html', {'form': form, 'account': account})
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account not found or inactive!')
                    return render(request, 'accounts/transfer.html', {'form': form, 'account': account})
                
                with transaction.atomic():
                    # Deduct from sender
                    account.balance -= amount
                    account.save()
                    
                    # Add to recipient
                    to_account.balance += amount
                    to_account.save()
                    
                    # Create transactions
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Transfer',
                        amount=amount,
                        balance_after_transaction=account.balance,
                        description=f'Transfer to {to_account_number} - {description}',
                        to_account=to_account
                    )
                    
                    Transaction.objects.create(
                        account=to_account,
                        transaction_type='Transfer',
                        amount=amount,
                        balance_after_transaction=to_account.balance,
                        description=f'Transfer from {account.account_number} - {description}',
                        to_account=account
                    )
                
                messages.success(request, f'Successfully transferred ₹{amount} to account {to_account_number}')
                return redirect('dashboard')
        else:
            form = TransferForm()
        
        return render(request, 'accounts/transfer.html', {'form': form, 'account': account})
    except (Customer.DoesNotExist, Account.DoesNotExist):
        messages.error(request, 'Account not found.')
        return redirect('dashboard')


@login_required
def transaction_history(request):
    """Transaction history view"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        transactions = Transaction.objects.filter(account=account).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'accounts/transaction_history.html', {
            'page_obj': page_obj,
            'account': account
        })
    except (Customer.DoesNotExist, Account.DoesNotExist):
        messages.error(request, 'Account not found.')
        return redirect('dashboard')


@login_required
def profile(request):
    """User profile view"""
    try:
        customer = Customer.objects.get(user=request.user)
        account = Account.objects.get(customer=customer)
        
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, instance=customer)
            if form.is_valid():
                customer = form.save()
                # Update user info
                user = request.user
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.email = request.POST.get('email', user.email)
                user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            form = ProfileUpdateForm(instance=customer)
            form.fields['first_name'].initial = request.user.first_name
            form.fields['last_name'].initial = request.user.last_name
            form.fields['email'].initial = request.user.email
        
        return render(request, 'accounts/profile.html', {
            'form': form,
            'customer': customer,
            'account': account
        })
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('dashboard')


# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard"""
    total_customers = Customer.objects.count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum('balance'))['balance__sum'] or Decimal('0.00')
    
    total_deposits = Transaction.objects.filter(transaction_type='Deposit').aggregate(
        Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_withdrawals = Transaction.objects.filter(transaction_type='Withdraw').aggregate(
        Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    pending_approvals = Customer.objects.filter(is_approved=False).count()
    recent_transactions = Transaction.objects.all()[:10]
    
    context = {
        'total_customers': total_customers,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'pending_approvals': pending_approvals,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def manage_customers(request):
    """Admin view to manage customers"""
    search_query = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search_query:
        customers = customers.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/manage_customers.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
@user_passes_test(is_admin)
def approve_customer(request, customer_id):
    """Approve customer account"""
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_approved = True
    customer.save()
    messages.success(request, f'Customer {customer.user.username} approved successfully!')
    return redirect('manage_customers')


@login_required
@user_passes_test(is_admin)
def deactivate_customer(request, customer_id):
    """Deactivate customer account"""
    customer = get_object_or_404(Customer, id=customer_id)
    try:
        account = Account.objects.get(customer=customer)
        account.is_active = False
        account.save()
        messages.success(request, f'Account {account.account_number} deactivated successfully!')
    except Account.DoesNotExist:
        messages.error(request, 'Account not found.')
    return redirect('manage_customers')


@login_required
@user_passes_test(is_admin)
def activate_customer(request, customer_id):
    """Activate customer account"""
    customer = get_object_or_404(Customer, id=customer_id)
    try:
        account = Account.objects.get(customer=customer)
        account.is_active = True
        account.save()
        messages.success(request, f'Account {account.account_number} activated successfully!')
    except Account.DoesNotExist:
        messages.error(request, 'Account not found.')
    return redirect('manage_customers')


@login_required
@user_passes_test(is_admin)
def all_transactions(request):
    """Admin view all transactions"""
    search_query = request.GET.get('search', '')
    transactions = Transaction.objects.all().order_by('-created_at')
    
    if search_query:
        transactions = transactions.filter(
            Q(transaction_id__icontains=search_query) |
            Q(account__account_number__icontains=search_query) |
            Q(account__customer__user__username__icontains=search_query)
        )
    
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/all_transactions.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


@login_required
@user_passes_test(is_admin)
def reports(request):
    """Admin reports view"""
    total_deposits = Transaction.objects.filter(transaction_type='Deposit').aggregate(
        Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_withdrawals = Transaction.objects.filter(transaction_type='Withdraw').aggregate(
        Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_transfers = Transaction.objects.filter(transaction_type='Transfer').aggregate(
        Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    total_balance = Account.objects.aggregate(Sum('balance'))['balance__sum'] or Decimal('0.00')
    
    active_accounts = Account.objects.filter(is_active=True).count()
    inactive_accounts = Account.objects.filter(is_active=False).count()
    
    context = {
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_transfers': total_transfers,
        'total_balance': total_balance,
        'active_accounts': active_accounts,
        'inactive_accounts': inactive_accounts,
    }
    return render(request, 'accounts/reports.html', context)

