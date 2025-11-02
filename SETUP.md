# Setup Guide

## Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **Tesseract OCR** - Download from: https://github.com/UB-Mannheim/tesseract/wiki
4. **Tavily API Key** - Sign up at: https://tavily.com (free tier available)

## Backend Setup

```bash
cd api
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create `api/.env` file:
```
TAVILY_API_KEY=your_tavily_api_key_here
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

Start server:
```bash
python main.py
```

Backend will run on: http://localhost:8000

## Frontend Setup

```bash
cd ui
npm install
npm run dev
```

Frontend will run on: http://localhost:3000

## Verify Setup

1. Open http://localhost:3000
2. Upload a medicine image
3. Click "Scan & Verify Medicine"
4. View results

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

**Tesseract not found:**
- Install Tesseract OCR and update path in `.env`
- Verify: `tesseract --version`

**Date detection issues:**
- Use clear, well-lit images
- Capture label straight-on
- Upload multiple angles for better accuracy

**Tavily errors:**
- Check API key in `.env` file
- Verify free tier quota remaining

**Port conflicts:**
- Backend: Change port in `main.py`
- Frontend: Use `npm run dev -- -p 3001`

**Module import errors:**
- Reinstall: `pip install -r requirements.txt --force-reinstall`
