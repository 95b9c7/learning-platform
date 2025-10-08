# SafeOperator Pro - Railway Deployment Guide

## 🚀 Deployment Overview

This guide will help you deploy SafeOperator Pro to Railway with both frontend (Next.js) and backend (Django) services.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Railway CLI** (optional): `npm install -g @railway/cli`

## 🏗️ Project Structure

```
NewLearningPlatform/
├── frontend/          # Next.js frontend
├── learning_platform/ # Django backend
├── requirements.txt   # Python dependencies
└── README.md
```

## 🔧 Backend Deployment (Django)

### 1. Connect Repository to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `learning_platform` folder as the root directory

### 2. Environment Variables

Set these environment variables in Railway dashboard:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app.railway.app

# Database (Railway will provide PostgreSQL)
DATABASE_URL=postgresql://...

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles/
```

### 3. Backend Configuration

The backend is already configured with:
- ✅ `railway.json` - Railway deployment config
- ✅ `Procfile` - Process definition
- ✅ `requirements.txt` - Python dependencies
- ✅ Gunicorn for production server
- ✅ PostgreSQL support via psycopg2

## 🎨 Frontend Deployment (Next.js)

### 1. Create Second Railway Service

1. In your Railway project, click "New Service"
2. Select "Deploy from GitHub repo"
3. Choose the same repository
4. Select the `frontend` folder as the root directory

### 2. Environment Variables

Set these environment variables for the frontend:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend-app.railway.app/api

# Next.js Configuration
NODE_ENV=production
```

### 3. Frontend Configuration

The frontend is configured with:
- ✅ `railway.json` - Railway deployment config
- ✅ `Procfile` - Process definition
- ✅ Environment variable support for API URL

## 🔄 Deployment Process

### Backend Deployment Steps:

1. **Connect Repository**: Select `learning_platform` folder
2. **Set Environment Variables**: Add the variables listed above
3. **Deploy**: Railway will automatically:
   - Install Python dependencies
   - Run database migrations
   - Collect static files
   - Start Gunicorn server

### Frontend Deployment Steps:

1. **Connect Repository**: Select `frontend` folder
2. **Set Environment Variables**: 
   - `NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api`
3. **Deploy**: Railway will automatically:
   - Install Node.js dependencies
   - Build the Next.js application
   - Start the production server

## 🌐 Custom Domains

After deployment, you can:

1. **Backend**: Set custom domain for API
2. **Frontend**: Set custom domain for the main application
3. **Update CORS**: Add your frontend domain to `ALLOWED_HOSTS`

## 🔐 Security Configuration

### Production Settings:

1. **Generate Secret Key**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Set ALLOWED_HOSTS**:
   ```bash
   ALLOWED_HOSTS=your-app.railway.app,your-custom-domain.com
   ```

3. **Configure CORS**:
   ```bash
   CORS_ALLOWED_ORIGINS=https://your-frontend.railway.app
   ```

## 📊 Monitoring & Logs

Railway provides:
- **Real-time logs** for both services
- **Metrics** and performance monitoring
- **Automatic restarts** on failures
- **Environment variable management**

## 🚨 Troubleshooting

### Common Issues:

1. **Build Failures**: Check logs in Railway dashboard
2. **API Connection Issues**: Verify `NEXT_PUBLIC_API_URL` is correct
3. **CORS Errors**: Update `ALLOWED_HOSTS` and CORS settings
4. **Database Issues**: Check `DATABASE_URL` is properly set

### Debug Commands:

```bash
# Check Railway logs
railway logs

# Check environment variables
railway variables

# Connect to service shell
railway shell
```

## 🎯 Demo Access

Once deployed:

1. **Frontend**: `https://your-frontend.railway.app`
2. **Backend API**: `https://your-backend.railway.app/api`
3. **Demo Login**: `demo@safeoperatorpro.com` / `demo123`

## 📝 Post-Deployment

1. **Test Authentication**: Try logging in with demo account
2. **Verify API**: Check that courses load properly
3. **Test Responsiveness**: Ensure mobile compatibility
4. **Monitor Performance**: Check Railway metrics

## 🔄 Updates

To update your deployment:

1. **Push to GitHub**: Make your changes and push to main branch
2. **Auto-Deploy**: Railway will automatically redeploy
3. **Verify**: Test the updated functionality

---

**Your SafeOperator Pro platform will be live and ready for demos!** 🎉
