# MediScan Deployment Guide

Complete guide for deploying MediScan to production using Vercel (Frontend) and Render (Backend).

---

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Render Account** - Sign up at [render.com](https://render.com)
4. **Tavily API Key** - Get from [tavily.com](https://tavily.com)

---

## Part 1: Push Code to GitHub

### Step 1: Initialize Git Repository

```bash
cd c:\Users\sunda\Projects-Sundaram\Dev\mediscan

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - MediScan ready for deployment"
```

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository named `mediscan`
2. **DO NOT** initialize with README (we already have one)
3. Copy the repository URL (e.g., `https://github.com/yourusername/mediscan.git`)

### Step 3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/yourusername/mediscan.git

# Push code
git branch -M main
git push -u origin main
```

---

## Part 2: Deploy Backend to Render

### Step 1: Create Web Service on Render

1. Go to [render.com/dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your `mediscan` repository

### Step 2: Configure Web Service

**Basic Settings:**
- **Name:** `mediscan-api`
- **Region:** Singapore (or closest to you)
- **Branch:** `main`
- **Root Directory:** `api`
- **Runtime:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt && playwright install chromium && playwright install-deps
  ```
- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (or paid plan for better performance)

### Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `TAVILY_API_KEY` | `your-tavily-api-key-here` |
| `TESSERACT_CMD` | `/usr/bin/tesseract` |

**Important:** Replace `your-tavily-api-key-here` with your actual Tavily API key!

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (takes 5-10 minutes first time)
3. Once deployed, copy your backend URL (e.g., `https://mediscan-api.onrender.com`)

### Step 5: Test Backend

Visit: `https://mediscan-api.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "service": "MediScan API"
}
```

**Note:** Free tier services sleep after 15 minutes of inactivity. First request after sleeping takes ~30 seconds to wake up.

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Update Frontend Configuration

Before deploying, update the API URL:

1. Edit `ui/.env.production`:
```env
NEXT_PUBLIC_API_BASE=https://mediscan-api.onrender.com
```

2. Commit and push this change:
```bash
git add ui/.env.production
git commit -m "Update production API URL"
git push
```

### Step 2: Deploy to Vercel

**Option A: Using Vercel Dashboard (Recommended)**

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your `mediscan` repository from GitHub
4. Configure project:
   - **Framework Preset:** Next.js
   - **Root Directory:** `ui`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.next`
   - **Install Command:** `npm install`

5. Add Environment Variables:
   - Key: `NEXT_PUBLIC_API_BASE`
   - Value: `https://mediscan-api.onrender.com` (your Render backend URL)

6. Click **"Deploy"**
7. Wait 2-3 minutes for deployment
8. Copy your frontend URL (e.g., `https://mediscan.vercel.app`)

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to frontend
cd ui

# Deploy
vercel --prod

# Follow prompts:
# - Set up and deploy: Y
# - Which scope: (your account)
# - Link to existing project: N
# - Project name: mediscan
# - Directory: ./
# - Override settings: N
```

### Step 3: Configure CORS on Backend

Update backend to allow your Vercel domain:

1. SSH into Render or update `api/main.py` locally:

```python
# In api/main.py, update CORS origins:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mediscan.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Commit and push:
```bash
git add api/main.py
git commit -m "Update CORS for production"
git push
```

Render will automatically redeploy with the new changes.

---

## Part 4: Verify Deployment

### Test Full Flow

1. Visit your Vercel URL: `https://mediscan.vercel.app`
2. Upload a medicine image
3. Click "Scan & Verify Medicine"
4. Verify results appear correctly

### Common Issues & Solutions

**Issue 1: CORS Error**
- **Solution:** Make sure you added Vercel URL to CORS origins in `api/main.py`

**Issue 2: Backend returns 404**
- **Solution:** Check that `NEXT_PUBLIC_API_BASE` environment variable is set correctly in Vercel

**Issue 3: Tesseract not found**
- **Solution:** Verify `TESSERACT_CMD=/usr/bin/tesseract` in Render environment variables

**Issue 4: First request times out (Render free tier)**
- **Solution:** This is normal. Free tier sleeps after 15 min inactivity. Wait 30s for wake-up.

**Issue 5: Playwright fails**
- **Solution:** Ensure build command includes `playwright install chromium && playwright install-deps`

---

## Part 5: Custom Domain (Optional)

### For Vercel (Frontend)

1. In Vercel dashboard, go to your project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain (e.g., `mediscan.yourdomain.com`)
4. Follow DNS configuration instructions

### For Render (Backend)

1. In Render dashboard, go to your web service
2. Click **"Settings"** → **"Custom Domains"**
3. Add your API subdomain (e.g., `api.mediscan.yourdomain.com`)
4. Update DNS records as instructed

---

## Monitoring & Maintenance

### Vercel Analytics
- Automatically enabled for all deployments
- View at: Vercel Dashboard → Your Project → Analytics

### Render Logs
- View logs at: Render Dashboard → Your Service → Logs
- Monitor for errors and performance issues

### Update Deployment

**Frontend Updates:**
```bash
# Make changes in ui/
git add .
git commit -m "Update frontend"
git push
# Vercel auto-deploys on push
```

**Backend Updates:**
```bash
# Make changes in api/
git add .
git commit -m "Update backend"
git push
# Render auto-deploys on push
```

---

## Cost Summary

**Free Tier:**
- **Vercel:** 100GB bandwidth, unlimited deployments
- **Render:** 750 hours/month (sleeps after 15 min inactivity)
- **Tavily:** 1,000 searches/month

**Total Monthly Cost:** $0 (with limitations)

**Recommended Paid Tier for Production:**
- **Vercel Pro:** $20/month (better performance, analytics)
- **Render Starter:** $7/month (no sleeping, 0.5GB RAM)
- **Tavily Pro:** $100/month (10,000 searches)

**Total Production Cost:** ~$127/month

---

## Security Checklist

- ✅ `.env` files added to `.gitignore`
- ✅ API keys stored in environment variables (not in code)
- ✅ CORS configured with specific origins
- ✅ HTTPS enabled (automatic on Vercel and Render)
- ✅ Rate limiting recommended for production
- ✅ Input validation on all endpoints

---

## Deployment URLs

After deployment, update these in your documentation:

**Frontend (Vercel):**
```
Production: https://mediscan.vercel.app
Preview: https://mediscan-git-[branch].vercel.app
```

**Backend (Render):**
```
Production: https://mediscan-api.onrender.com
API Docs: https://mediscan-api.onrender.com/docs
Health Check: https://mediscan-api.onrender.com/health
```

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Test complete verification flow
4. 📱 Share URL with team and users
5. 📊 Monitor usage and performance
6. 🔄 Set up CI/CD pipeline (optional)
7. 📈 Consider upgrading to paid tier for production use

---

**Congratulations! Your MediScan application is now live!** 🎉

For issues or questions, check:
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Project README: [README.md](README.md)
