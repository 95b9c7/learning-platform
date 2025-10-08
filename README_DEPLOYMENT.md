# 🚀 SafeOperator Pro - Quick Deployment Guide

## One-Click Railway Deployment

### 🎯 Quick Start

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Deploy Backend First:**
   - Choose `learning_platform` folder as root
   - Railway will auto-detect Python/Django
   - Add PostgreSQL database service
6. **Deploy Frontend:**
   - Create new service in same project
   - Choose `frontend` folder as root
   - Railway will auto-detect Node.js/Next.js

### 🔧 Environment Variables

#### Backend (Django):
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DATABASE_URL=postgresql://... (auto-provided by Railway)
CORS_ALLOW_ALL_ORIGINS=True
```

#### Frontend (Next.js):
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api
NODE_ENV=production
```

### 🎉 Demo Access

Once deployed:
- **Frontend**: `https://your-frontend.railway.app`
- **Demo Login**: `demo@safeoperatorpro.com` / `demo123`

### 📖 Full Guide

See `RAILWAY_DEPLOYMENT_GUIDE.md` for detailed instructions.

---

**Ready to demo SafeOperator Pro!** 🛡️
