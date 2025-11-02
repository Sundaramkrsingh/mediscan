# MediScan Deployment Checklist

Quick checklist to deploy MediScan to production.

## Pre-Deployment ✅

- [ ] Test application locally (frontend + backend)
- [ ] Verify Tavily API key works
- [ ] Review all environment variables
- [ ] Check `.gitignore` includes `.env` files
- [ ] Commit all changes to git

## GitHub Setup 📦

- [ ] Create GitHub repository: `mediscan`
- [ ] Push code to GitHub main branch
- [ ] Verify all files uploaded correctly

## Backend Deployment (Render) 🚀

- [ ] Create Render account
- [ ] Create new Web Service
- [ ] Connect GitHub repository
- [ ] Configure build settings:
  - Root Directory: `api`
  - Build Command: `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables:
  - `PYTHON_VERSION=3.11.0`
  - `TAVILY_API_KEY=[your-key]`
  - `TESSERACT_CMD=/usr/bin/tesseract`
- [ ] Deploy and wait for completion
- [ ] Copy backend URL (e.g., `https://mediscan-api.onrender.com`)
- [ ] Test health endpoint: `https://[your-url]/health`
- [ ] Test API docs: `https://[your-url]/docs`

## Frontend Deployment (Vercel) 🎨

- [ ] Create Vercel account
- [ ] Update `ui/.env.production` with backend URL
- [ ] Commit and push changes
- [ ] Create new project on Vercel
- [ ] Import GitHub repository
- [ ] Configure settings:
  - Framework: Next.js
  - Root Directory: `ui`
  - Build Command: `npm run build`
- [ ] Add environment variable:
  - `NEXT_PUBLIC_API_BASE=[your-render-url]`
- [ ] Deploy and wait for completion
- [ ] Copy frontend URL (e.g., `https://mediscan.vercel.app`)

## Post-Deployment Testing ✨

- [ ] Visit frontend URL
- [ ] Upload test medicine image
- [ ] Click "Scan & Verify Medicine"
- [ ] Verify results display correctly
- [ ] Test on mobile device
- [ ] Test on different browsers
- [ ] Check browser console for errors
- [ ] Verify API calls work correctly

## Production Configuration 🔧

- [ ] Update CORS in `api/main.py` with Vercel URL
- [ ] Enable rate limiting (optional)
- [ ] Set up monitoring/alerts
- [ ] Configure custom domain (optional)
- [ ] Update README with live URLs

## Documentation Updates 📝

- [ ] Add deployment URLs to README.md
- [ ] Update team about live deployment
- [ ] Create user guide if needed
- [ ] Document any issues encountered

## Monitoring & Maintenance 📊

- [ ] Bookmark Vercel dashboard
- [ ] Bookmark Render dashboard
- [ ] Set up error tracking (optional: Sentry)
- [ ] Monitor API usage (Tavily dashboard)
- [ ] Check logs regularly for errors

---

## Quick Commands

### Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Test Backend Locally
```bash
cd api
python main.py
# Visit: http://localhost:8000/health
```

### Test Frontend Locally
```bash
cd ui
npm run dev
# Visit: http://localhost:3000
```

### Update After Deployment
```bash
# Make changes
git add .
git commit -m "Description of changes"
git push

# Both Vercel and Render auto-deploy on push!
```

---

## Deployment URLs

**Update these after deployment:**

- **Frontend:** https://mediscan.vercel.app
- **Backend:** https://mediscan-api.onrender.com
- **API Docs:** https://mediscan-api.onrender.com/docs

---

## Support

If you encounter issues:
1. Check deployment logs on Render/Vercel
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. Test locally to isolate the problem
4. Check environment variables are set correctly
