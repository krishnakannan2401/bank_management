# 🚀 Quick Setup Guide

## Step-by-Step Installation

### 1. Install Python and MySQL

- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Download MySQL from [mysql.com](https://dev.mysql.com/downloads/mysql/)
- Install both and ensure they're added to PATH

### 2. Setup Project

```bash
# Navigate to project directory
cd bank_project

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure MySQL

```sql
-- Open MySQL Command Line or MySQL Workbench
CREATE DATABASE bank_management_db;
```

Update `bankproject/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bank_management_db',
        'USER': 'root',          # Change if different
        'PASSWORD': 'your_password',  # Add your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Initialize Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

Open browser: `http://127.0.0.1:8000/`

## First Steps

1. **Login as Admin:**
   - Use the superuser credentials you created
   - Access admin dashboard at `/admin-dashboard/`

2. **Create Test Customer:**
   - Register a new account from home page
   - Login as admin and approve the account
   - Login as customer to test features

## Common Issues

### Issue: mysqlclient installation fails
**Solution:** 
- Windows: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
- Or use: `pip install pymysql` and add to settings.py:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue: Database connection error
**Solution:**
- Check MySQL is running: `mysql -u root -p`
- Verify database exists
- Check credentials in settings.py

### Issue: Migration errors
**Solution:**
```bash
python manage.py migrate --run-syncdb
```

## Testing the System

1. Register a new customer account
2. Login as admin and approve the customer
3. Login as customer and:
   - View dashboard
   - Make a deposit
   - Make a withdrawal
   - Transfer money (create another account first)
   - View transaction history
   - Update profile

## Admin Features Test

1. Login as admin
2. Go to "Manage Customers" - approve/activate accounts
3. View "All Transactions" - see all transactions
4. Check "Reports" - view statistics

---

**Happy Banking! 🏦**

