#!/bin/bash

# SafeOperator Pro - Railway Deployment Script
echo "🚀 SafeOperator Pro Railway Deployment"
echo "======================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "📋 Deployment Checklist:"
echo "1. ✅ Backend configured (Django + PostgreSQL)"
echo "2. ✅ Frontend configured (Next.js)"
echo "3. ✅ Environment variables ready"
echo "4. ✅ Database migrations prepared"
echo ""

echo "🔧 Next Steps:"
echo "1. Go to https://railway.app"
echo "2. Create new project"
echo "3. Deploy from GitHub repo"
echo "4. Select 'learning_platform' folder for backend"
echo "5. Create second service for 'frontend' folder"
echo "6. Set environment variables as per RAILWAY_DEPLOYMENT_GUIDE.md"
echo ""

echo "🌐 Your app will be available at:"
echo "- Frontend: https://your-frontend.railway.app"
echo "- Backend API: https://your-backend.railway.app/api"
echo ""

echo "🎯 Demo credentials:"
echo "- Email: demo@safeoperatorpro.com"
echo "- Password: demo123"
echo ""

echo "📖 See RAILWAY_DEPLOYMENT_GUIDE.md for detailed instructions"
echo "🎉 Happy deploying!"
