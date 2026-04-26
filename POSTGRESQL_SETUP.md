# PostgreSQL Database Setup for STAY UP Furniture

This script will help you set up PostgreSQL for the STAY UP Furniture Django project.

## Prerequisites
- PostgreSQL installed and running
- Admin access to create databases and users

## Manual Setup Instructions

### Option 1: Using pgAdmin (GUI)
1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Enter database name: `stayup_furniture`
4. Click "Save"
5. Go to "Login/Group Roles" → "Create" → "Login/Group Role"
6. Enter username: `postgres` (or your preferred username)
7. Set a strong password
8. Go to "Privileges" tab and grant necessary permissions
9. Save the user

### Option 2: Using SQL Shell (psql)
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE stayup_furniture;

-- Create user (replace 'your_password' with actual password)
CREATE USER stayup_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE stayup_furniture TO stayup_user;

-- Exit
\q
```

### Option 3: Using Windows Command Line
```cmd
-- Open psql as postgres user
psql -U postgres

-- Then run the SQL commands above
```

## Update Environment Variables

After creating the database, update your `.env` file:

```env
# Database Configuration
DB_NAME=stayup_furniture
DB_USER=stayup_user  # or postgres if using default
DB_PASSWORD=your_actual_password_here
DB_HOST=localhost
DB_PORT=5432
```

## Test Connection

1. Make sure PostgreSQL service is running
2. Run Django migrations:
   ```bash
   python manage.py migrate
   ```

3. If successful, create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Test the server:
   ```bash
   python manage.py runserver
   ```

## Common Issues & Solutions

### Issue: "OperationalError: could not connect to server"
- Check if PostgreSQL service is running
- Verify host and port settings
- Check firewall settings

### Issue: "FATAL: password authentication failed for user"
- Verify username and password in .env file
- Make sure user exists and has correct permissions

### Issue: "FATAL: database does not exist"
- Database name doesn't match between .env and actual database
- Case sensitivity matters in PostgreSQL

## For Production

1. Use a stronger password
2. Create a dedicated database user (not postgres)
3. Set up proper connection limits
4. Configure SSL connections
5. Set up regular backups

## Database Backup Commands

```bash
# Backup database
pg_dump -U stayup_user -h localhost stayup_furniture > backup.sql

# Restore database
psql -U stayup_user -h localhost stayup_furniture < backup.sql
```

## Alternative: Use Docker PostgreSQL

If you prefer using Docker:

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: stayup_furniture
      POSTGRES_USER: stayup_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Then run:
```bash
docker-compose up -d
```