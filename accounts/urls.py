from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # User URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('profile/', views.profile, name='profile'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-customers/', views.manage_customers, name='manage_customers'),
    path('approve-customer/<int:customer_id>/', views.approve_customer, name='approve_customer'),
    path('deactivate-customer/<int:customer_id>/', views.deactivate_customer, name='deactivate_customer'),
    path('activate-customer/<int:customer_id>/', views.activate_customer, name='activate_customer'),
    path('all-transactions/', views.all_transactions, name='all_transactions'),
    path('reports/', views.reports, name='reports'),
]

