# Setting Up Tavily AI for Advanced Verification

MediScan uses **Tavily AI** to perform intelligent web searches across trusted medical databases for comprehensive medicine verification.

## What Tavily Does

Tavily enhances verification by:
- **Cross-referencing** medicine data across CDSCO, GS1, WHO, and FDA websites
- **Finding manufacturer information** from official sources
- **Checking counterfeit alerts** and drug recalls
- **Verifying barcode authenticity** through online databases
- **AI-powered analysis** of medicine authenticity

## Getting Your Free API Key

1. Visit: https://tavily.com
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key

### Free Tier Limits:
- **1,000 searches/month** (sufficient for personal/demo use)
- Advanced search depth
- Multiple source aggregation

## Configuration

### Step 1: Create `.env` file

In the `api/` directory, create or edit `.env`:

```bash
TAVILY_API_KEY=tvly-your-actual-api-key-here
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Step 2: Restart Backend

```bash
cd api
python main.py
```

You should see:
```
Tavily AI service initialized ✓
```

Instead of:
```
Warning: Tavily API key not found. Advanced search disabled.
```

## What Happens Without Tavily

### Current Limitations:

**Without Tavily:**
- ✅ Barcode detection works
- ✅ Basic GS1 prefix validation (890 = India)
- ✅ OCR date extraction works
- ⚠️ No cross-verification with regulatory databases
- ⚠️ No counterfeit alert checking
- ⚠️ Limited manufacturer verification

**With Tavily:**
- ✅ **All basic features**
- ✅ **Real-time regulatory database verification**
- ✅ **Counterfeit alert detection** from CDSCO
- ✅ **Multi-source manufacturer verification**
- ✅ **AI-powered authenticity scoring**

## Verification Flow

### 1. Barcode Detection (No API required)
- OpenCV + Pyzbar detect barcodes locally
- Validates checksum using GS1 algorithm

### 2. GS1 Prefix Verification (No API required)
- Checks country prefix (890 = India, 891 = India, etc.)
- Extracts company prefix
- **Note**: This is basic validation, not full GS1 database lookup

### 3. Tavily AI Search (Requires API key)
```python
# Searches multiple trusted sources:
- cdsco.gov.in (Indian drug regulator)
- gs1india.org (GS1 India database)
- mohfw.gov.in (Ministry of Health)
- gepir.gs1.org (Global GS1 registry)
```

### 4. CDSCO Regulatory Check (Enhanced with Tavily)
- Without Tavily: Basic structure checking
- With Tavily: Real searches against CDSCO database

## Testing Tavily Integration

After setting up your API key, test with:

```bash
cd api
python -c "from services.tavily_search import get_tavily_service; s = get_tavily_service(); print('Enabled:', s.enabled)"
```

Expected output:
```
Enabled: True
```

## Cost Considerations

### Free Tier (Recommended for Development):
- 1,000 API calls/month
- ~33 scans/day
- Perfect for testing and demos

### Paid Plans (For Production):
- Pro: $50/month - 10,000 searches
- Enterprise: Custom pricing

### Alternative: No-API Mode

The system works **without Tavily** but with reduced verification capabilities:
- Barcode scanning: ✓
- Date detection: ✓
- Basic GS1 validation: ✓
- Advanced verification: ✗

## Security Note

**Never commit `.env` file to Git!**

The `.gitignore` already includes `.env`:
```
.env
*.env
```

Always keep your API key private!
