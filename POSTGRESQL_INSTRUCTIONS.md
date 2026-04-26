# PostgreSQL Setup Instructions for STAY UP Furniture

## ✅ What I've Already Done

1. **Updated Django Settings** - Changed from SQLite to PostgreSQL
2. **Installed Required Packages** - psycopg2-binary and python-decouple
3. **Created Environment Configuration** - .env file with database settings
4. **Created Setup Scripts** - Both manual and automated options

## 🚀 Next Steps for You

### Option 1: Quick Setup (Recommended)

1. **Install PostgreSQL** if not already installed:
   - Download from: https://www.postgresql.org/download/windows/
   - During installation, set password for postgres user (remember it!)

2. **Run the Setup Script**:
   ```cmd
   setup_postgresql.bat
   ```

3. **Test Django Connection**:
   ```cmd
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

### Option 2: Manual Setup

1. **Open pgAdmin** (installed with PostgreSQL)

2. **Create Database**:
   - Right-click "Databases" → "Create" → "Database"
   - Name: `stayup_furniture`
   - Click "Save"

3. **Create User**:
   - Go to "Login/Group Roles" → "Create" → "Login/Group Role"
   - Name: `stayup_user`
   - Password: `furniture123` (or your choice)
   - Go to "Privileges" tab → "Can login? = Yes"
   - Save

4. **Grant Privileges**:
   - Right-click "stayup_furniture" database
   - Select "Properties"
   - Go to "Security" tab
   - Add "stayup_user" with all privileges

5. **Update .env file** if you used different credentials:
   ```env
   DB_NAME=stayup_furniture
   DB_USER=stayup_user
   DB_PASSWORD=your_actual_password
   ```

6. **Run Migrations**:
   ```cmd
   python manage.py migrate
   ```

## 🎯 After Database Setup

Once PostgreSQL is set up, you'll have:

✅ **Production-ready database** instead of SQLite
✅ **Better performance** for handling furniture catalog
✅ **Scalability** for growth and multiple users
✅ **Advanced features** like transactions and constraints

## 📋 Verification Commands

```cmd
# Test database connection
python manage.py dbshell

# Check tables were created
python manage.py shell
>>> from store.models import Product, Category
>>> Category.objects.all()

# Run server
python manage.py runserver
```

## 🔧 Troubleshooting

### "FATAL: password authentication failed"
- Check .env file password matches actual PostgreSQL password
- Try using 'postgres' as username if setup script didn't work

### "OperationalError: could not connect to server"
- Make sure PostgreSQL service is running
- Check that port 5432 is not blocked by firewall
- Verify DB_HOST is 'localhost'

### "FATAL: database does not exist"
- Database name in .env must match exactly (case sensitive)
- Run the setup script again or create manually in pgAdmin

## 🚀 Benefits of PostgreSQL vs SQLite

| Feature | PostgreSQL | SQLite |
|---------|-------------|---------|
| **Performance** | ✅ Excellent for production | ⚠️ Limited for web apps |
| **Concurrency** | ✅ Multiple users | ❌ Single writer |
| **Scalability** | ✅ Grows with business | ❌ Limited size |
| **Features** | ✅ Full SQL support | ⚠️ Basic SQL |
| **Backup/Restore** | ✅ Robust tools | ⚠️ File copy only |
| **Production Ready** | ✅ Industry standard | ❌ Development only |

Your STAY UP Furniture website is now ready to handle serious e-commerce traffic! 🛋️💨