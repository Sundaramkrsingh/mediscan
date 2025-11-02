# MediScan - Medicine Verification System

AI-powered medicine verification using real regulatory database checks via Tavily AI.

**🚀 Quick Start: [QUICK_START.md](QUICK_START.md)**

## Features

- Barcode & QR code detection (EAN-13, CODE-128, Data Matrix)
- OCR text extraction (expiry dates, batch numbers)
- GS1 standard validation (checksum & prefix verification)
- **Tavily AI-powered verification** - searches cdsco.gov.in, gs1india.org, FDA.gov
- Multi-factor authenticity detection with counterfeit alerts
- Modern responsive UI with real-time verification details

## Quick Setup

### Backend
```bash
cd api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd ui
npm install
npm run dev
```

Visit: http://localhost:3000

**For detailed setup including Tavily API configuration, see [SETUP.md](SETUP.md)**

## Documentation

**Getting Started:**
- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[SETUP.md](SETUP.md)** - Detailed setup with troubleshooting
- **[VERIFICATION_EXPLAINED.md](VERIFICATION_EXPLAINED.md)** - How verification actually works
- **[TAVILY_SETUP.md](TAVILY_SETUP.md)** - Tavily API configuration guide

**Deployment:**
- **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - Quick deployment overview
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide
- **[DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md)** - Step-by-step checklist

## Deployment

Ready to deploy to production? We've prepared everything you need:

**Backend:** Deploy to [Render](https://render.com) (Free tier available)
**Frontend:** Deploy to [Vercel](https://vercel.com) (Free tier available)

See [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) for complete instructions.

## Tech Stack

**Backend:** FastAPI, OpenCV, Tesseract, Pyzbar, Tavily

**Frontend:** Next.js, React, TypeScript, Tailwind, Framer Motion

**Deployment:** Vercel (Frontend) + Render (Backend)

## Team

Abhishek Gupta, Sundaram Singh (BETN1CS22175), Anurag Raj - ITM University Gwalior
