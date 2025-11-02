# Vercel Deployment Instructions

## Quick Fix for the Build Error

The error happened because Vercel needs to be configured to use the `ui` folder as the root directory.

---

## ✅ Correct Vercel Configuration

### When Creating New Project in Vercel:

1. **Go to Vercel Dashboard:** https://vercel.com/new

2. **Import Repository:**
   - Click "Import Project"
   - Select: `Sundaramkrsingh/mediscan`

3. **Configure Project Settings:**

   **Framework Preset:** Next.js (auto-detected)

   **Root Directory:**
   ```
   ui
   ```
   ⚠️ **IMPORTANT:** Click "Edit" next to Root Directory and select `ui`

   **Build Command:** (leave default)
   ```
   npm run build
   ```

   **Output Directory:** (leave default)
   ```
   .next
   ```

   **Install Command:** (leave default)
   ```
   npm install
   ```

4. **Environment Variables:**

   Click "Add Environment Variable" and add:

   | Key | Value |
   |-----|-------|
   | `NEXT_PUBLIC_API_BASE` | `https://your-render-backend-url.onrender.com` |

   ⚠️ Replace with your actual Render backend URL!

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Done! 🎉

---

## If You Already Created the Project

### Option 1: Delete and Recreate (Easiest)

1. Go to your Vercel project settings
2. Click "Delete Project"
3. Follow the steps above to create it correctly

### Option 2: Update Settings

1. Go to Project Settings in Vercel
2. Navigate to "General" tab
3. Under "Build & Development Settings":
   - **Root Directory:** Change to `ui`
   - **Framework Preset:** Next.js
   - Save changes
4. Go to "Deployments" tab
5. Click "Redeploy" on the latest deployment

---

## Environment Variables

Make sure you add this in Vercel dashboard under "Environment Variables":

```
NEXT_PUBLIC_API_BASE=https://your-render-url.onrender.com
```

**Where to add:**
1. Go to your project in Vercel
2. Click "Settings"
3. Click "Environment Variables"
4. Add the variable
5. Click "Save"
6. Redeploy your project

---

## Verify Deployment

After deployment, check:

1. ✅ Frontend loads at: `https://your-project.vercel.app`
2. ✅ No console errors (F12 → Console)
3. ✅ Can upload images
4. ✅ API calls work (check Network tab)

---

## Common Issues

### Issue: "Build Command exited with 1"

**Solution:** Make sure Root Directory is set to `ui` in project settings

### Issue: "Cannot find module 'next'"

**Solution:**
- Root Directory should be `ui`
- Install Command should be `npm install`

### Issue: "API calls fail / CORS error"

**Solution:**
1. Check `NEXT_PUBLIC_API_BASE` is set correctly in Vercel
2. Update CORS in backend `api/main.py` with your Vercel URL
3. Redeploy backend on Render

---

## File Structure Vercel Sees

When Root Directory is set to `ui`, Vercel sees:

```
ui/                    (← This becomes root for Vercel)
├── app/
│   ├── components/
│   ├── layout.tsx
│   └── page.tsx
├── package.json       (← Vercel reads this)
├── next.config.ts
└── ...
```

This is correct! ✅

---

## Quick Commands

**Trigger Redeploy:**
```bash
# Make any small change
git commit --allow-empty -m "Trigger Vercel redeploy"
git push
```

**Check Environment Variables:**
- Go to: https://vercel.com/[your-username]/mediscan/settings/environment-variables

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/docs/deployment
- Our Guide: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

---

**Updated:** November 2, 2025
**Status:** Configuration fixed - ready to deploy!
