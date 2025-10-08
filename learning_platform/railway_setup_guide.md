# Railway PostgreSQL Setup Guide

## Quick Setup Steps

### 1. Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 2. Create PostgreSQL Database
- Click "New Project"
- Select "Database" → "PostgreSQL"
- Railway will create a PostgreSQL instance

### 3. Get Database URL
- Click on your PostgreSQL service
- Go to "Variables" tab
- Copy the `DATABASE_URL` value

### 4. Update Your .env File
Replace the DATABASE_URL in your `.env` file with the Railway URL:

```
DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```

### 5. Test Connection
```bash
python manage.py migrate
```

## Benefits of Railway PostgreSQL
- ✅ No local installation needed
- ✅ Same database for development and production
- ✅ Automatic backups
- ✅ Scalable
- ✅ Free tier available

## Alternative: Local PostgreSQL
If you prefer local development, you can install PostgreSQL locally:
- Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- Install with default settings
- Create database: `modulelearning_db`
- Use local connection string
