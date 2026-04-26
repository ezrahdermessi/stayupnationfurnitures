@echo off
echo PostgreSQL Database Setup for STAY UP Furniture
echo ================================================

echo.
echo This script will help you set up PostgreSQL database.
echo Please make sure PostgreSQL is installed and running.
echo.

pause

echo.
echo Step 1: Creating database...
psql -U postgres -c "CREATE DATABASE stayup_furniture;"

echo.
echo Step 2: Creating user...
psql -U postgres -c "CREATE USER stayup_user WITH PASSWORD 'furniture123';"

echo.
echo Step 3: Granting privileges...
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE stayup_furniture TO stayup_user;"

echo.
echo Step 4: Testing connection...
psql -U stayup_user -d stayup_furniture -c "SELECT current_database(), current_user;"

echo.
echo Database setup completed!
echo.
echo Next steps:
echo 1. Update your .env file with the correct password
echo 2. Run: python manage.py migrate
echo 3. Run: python manage.py createsuperuser
echo 4. Run: python manage.py runserver
echo.

pause