# 🏦 Bank Management System

A comprehensive web-based Bank Management System built with Django and MySQL that allows users to efficiently manage all banking operations online.

## 📋 Project Overview

This system enables both customers and bank administrators to manage bank accounts, view transaction details, deposit and withdraw money, and maintain customer information securely.

## 🎯 Features

### User Module
- ✅ Create a new account (with minimum ₹500 initial deposit)
- ✅ Select account type (Saving or Current)
- ✅ Secure login & logout
- ✅ View account balance and profile details
- ✅ Deposit and withdraw money
- ✅ Transfer money to other accounts
- ✅ View transaction history
- ✅ Update profile information

### Admin Module
- ✅ Login using admin credentials
- ✅ View, approve, or deactivate user accounts
- ✅ View all customer transactions
- ✅ Generate reports for total deposits, withdrawals, and balances
- ✅ Search functionality for customers and transactions

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python (Django Framework)
- **Database**: MySQL
- **Server**: Django's built-in development server
- **OS**: Windows 11

## 📦 Installation & Setup

### Prerequisites

1. **Python 3.8+** installed on your system
2. **MySQL Server** installed and running
3. **pip** (Python package manager)

### Step 1: Clone or Download the Project

Navigate to the project directory:
```bash
cd bank_project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient`, you may need to:
- Install MySQL development libraries
- On Windows, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
- Or use `pip install pymysql` and configure it in settings.py

### Step 4: Configure MySQL Database

1. Open MySQL and create a new database:
```sql
CREATE DATABASE bank_management_db;
```

2. Update database settings in `bankproject/settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bank_management_db',
        'USER': 'root',          # Your MySQL username
        'PASSWORD': '',          # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. This account will have access to:
- Django admin panel (`/admin/`)
- Admin dashboard (`/admin-dashboard/`)
- All admin features

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## 🚀 Usage Guide

### For Customers

1. **Register a New Account:**
   - Click on "Register" from the home page
   - Fill in all required information
   - Select account type (Saving or Current)
   - Make initial deposit (minimum ₹500)
   - Wait for admin approval

2. **Login:**
   - Use your username and password to login
   - Once approved, you can access all features

3. **Dashboard:**
   - View account balance
   - See recent transactions
   - Quick access to all banking operations

4. **Transactions:**
   - **Deposit:** Add money to your account
   - **Withdraw:** Remove money (balance must be sufficient)
   - **Transfer:** Send money to another account using account number

5. **Profile:**
   - Update personal information
   - View account details

### For Administrators

1. **Login:**
   - Use superuser credentials to login
   - You'll be redirected to the admin dashboard

2. **Manage Customers:**
   - View all registered customers
   - Approve pending accounts
   - Activate/Deactivate accounts
   - Search customers by name, username, or phone

3. **View Transactions:**
   - See all transactions across all accounts
   - Search by transaction ID, account number, or username

4. **Reports:**
   - View total deposits, withdrawals, and transfers
   - See total bank balance
   - View account statistics

## 📁 Project Structure

```
bank_project/
├── manage.py
├── requirements.txt
├── README.md
├── bankproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── templates/
│   ├── base.html
│   └── accounts/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── deposit.html
│       ├── withdraw.html
│       ├── transfer.html
│       ├── transaction_history.html
│       ├── profile.html
│       ├── admin_dashboard.html
│       ├── manage_customers.html
│       ├── all_transactions.html
│       └── reports.html
└── static/
    └── (static files if any)
```

## 🔒 Security Features

- Password hashing using Django's built-in authentication
- CSRF protection on all forms
- User authentication and authorization
- Secure session management
- Admin approval system for new accounts

## 📊 Database Schema

### Models

1. **Customer** - Extends Django User model
   - User information
   - Contact details
   - Approval status

2. **Account** - Bank account information
   - Unique account number (auto-generated)
   - Account type (Saving/Current)
   - Balance
   - Active status

3. **Transaction** - Transaction records
   - Unique transaction ID (auto-generated)
   - Transaction type (Deposit/Withdraw/Transfer)
   - Amount and balance after transaction
   - Timestamp

## 🐛 Troubleshooting

### MySQL Connection Issues

If you encounter MySQL connection errors:
1. Ensure MySQL server is running
2. Verify database credentials in `settings.py`
3. Check if the database exists
4. Install MySQL client libraries

### Migration Issues

If migrations fail:
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading

Collect static files:
```bash
python manage.py collectstatic
```

## 📝 Notes

- Minimum initial deposit: ₹500
- Account numbers are auto-generated (12 digits)
- Transaction IDs are auto-generated (TXN + 10 digits)
- All amounts are stored with 2 decimal places
- Withdrawals are only allowed if sufficient balance exists

## 🚢 Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Update `SECRET_KEY` with a secure key
3. Configure `ALLOWED_HOSTS`
4. Use a production database
5. Set up a production server (Apache/Nginx with Gunicorn)
6. Configure static files serving
7. Set up SSL/HTTPS

## 👨‍💻 Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📄 License

This project is created for educational purposes.

## 👥 Support

For issues or questions, please contact the development team.

---

**Developed with ❤️ using Django**

