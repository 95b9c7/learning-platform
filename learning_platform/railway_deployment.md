# Railway Deployment Guide

## Railway Setup Steps

### 1. Connect Repository
- Go to [Railway.app](https://railway.app)
- Connect your GitHub repository
- Railway will automatically detect your Django project

### 2. Add PostgreSQL Database
- In Railway dashboard, click "New Service"
- Select "Database" → "PostgreSQL"
- Railway will automatically set `DATABASE_URL` environment variable

### 3. Environment Variables
Railway will automatically set these:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Railway assigns this automatically

You'll need to set these manually in Railway dashboard:
```
SECRET_KEY=your_production_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.railway.app
STRIPE_PUBLISHABLE_KEY=your_stripe_key
STRIPE_SECRET_KEY=your_stripe_secret
```

### 4. Automatic Deployment
- Railway will automatically deploy when you push to your main branch
- Runs migrations automatically via Procfile
- Collects static files automatically

## Development vs Production

### Local Development (.env file):
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/modulelearning_db
SECRET_KEY=django-insecure-z2wy^=$l5ojj_sz+3xioj-t-=8g98p#14qes$+v-03ku7bh$d^
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Railway Production (Environment Variables):
```
DATABASE_URL=postgresql://railway_user:password@railway_host:5432/railway_db
SECRET_KEY=your_secure_production_key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
```

## Benefits of Railway
- ✅ Automatic PostgreSQL setup
- ✅ Automatic HTTPS/SSL
- ✅ Zero-config deployment
- ✅ Built-in monitoring
- ✅ Automatic scaling
- ✅ GitHub integration
