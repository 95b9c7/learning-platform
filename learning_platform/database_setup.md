# Database Setup Instructions

## PostgreSQL Setup

### 1. Create Database
Connect to PostgreSQL and create the database:

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE modulelearning_db;

-- Create user (optional, you can use postgres user)
CREATE USER modulelearning_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE modulelearning_db TO modulelearning_user;
```

### 2. Environment Variables
Copy `env_template.txt` to `.env` and update the database URL:

```bash
cp env_template.txt .env
```

Update the `.env` file with your actual database credentials:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/modulelearning_db
```

### 3. Test Database Connection
Run migrations to test the connection:

```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

## Database Schema
After running migrations, your database will have:
- Django's default tables (auth, sessions, etc.)
- Core app tables (to be created in next steps)
