"""
MediScan API v2 - Medicine Expiry and Authenticity Detection
Enhanced version with web scraping, multi-image support, and authenticity checking
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import numpy as np
import cv2
import os
from datetime import date

# Import our custom services
from services.barcode_service import BarcodeService, detect_barcodes_multi_image
from services.ocr_service import OCRService, extract_text_multi_image
from services.gs1_scraper import GS1Scraper, verify_barcode
from services.cdsco_scraper import CDSCOScraper, verify_drug_regulatory
from services.authenticity_checker import AuthenticityChecker, verify_authenticity
from services.image_processor import ImageProcessor

# Configure Tesseract path
pytesseract_cmd = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Initialize FastAPI app
app = FastAPI(
    title="MediScan API v2",
    description="Medicine Expiry and Authenticity Detection System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class VerificationResponse(BaseModel):
    """Response model for verification endpoint"""
    status: str
    risk_level: str
    is_expired: bool
    expiry_date: Optional[str]
    gtin: Optional[str]
    gtin_verified: bool
    product_name: Optional[str]
    batch_number: Optional[str]
    manufacturer: Optional[str]
    country: Optional[str]
    risk_factors: List[dict]
    recommendations: List[str]
    details: dict
    raw_data: dict


# Helper functions
def file_to_cv2_image(data: bytes) -> Optional[np.ndarray]:
    """Convert uploaded file bytes to OpenCV image"""
    try:
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Image conversion error: {e}")
        return None


# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "tesseract_configured": os.path.exists(pytesseract_cmd) if pytesseract_cmd else False
    }


@app.post("/verify", response_model=VerificationResponse)
async def verify_medicine(images: List[UploadFile] = File(...)):
    """
    Main verification endpoint - analyzes medicine packaging images

    Accepts multiple images and returns comprehensive authenticity analysis
    """
    if not images or len(images) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required")

    try:
        # Step 1: Convert uploaded files to OpenCV images
        cv_images = []
        for uploaded_file in images:
            data = await uploaded_file.read()
            img = file_to_cv2_image(data)
            if img is not None:
                cv_images.append(img)

        if not cv_images:
            raise HTTPException(status_code=400, detail="No valid images provided")

        # Step 2: Detect and decode barcodes/QR codes from all images
        print("Step 2: Detecting barcodes...")
        barcode_service = BarcodeService()
        all_barcodes = []
        gtin = None
        barcode_expiry = None
        batch_from_barcode = None

        for img in cv_images:
            codes = barcode_service.detect_and_decode(img)
            all_barcodes.extend(codes)

            # Extract GTIN and other info
            for code in codes:
                if code["parsed"].get("gtin") and not gtin:
                    gtin = code["parsed"]["gtin"]
                if code["parsed"].get("expiry") and not barcode_expiry:
                    barcode_expiry = code["parsed"]["expiry"]
                if code["parsed"].get("batch") and not batch_from_barcode:
                    batch_from_barcode = code["parsed"]["batch"]

        print(f"Found {len(all_barcodes)} barcodes, GTIN: {gtin}")

        # Step 3: Perform OCR on all images
        print("Step 3: Performing OCR...")
        ocr_service = OCRService(tesseract_cmd=pytesseract_cmd)
        ocr_results = ocr_service.extract_from_multiple_images(cv_images)

        # Extract key information from OCR
        ocr_expiry = ocr_results.get("expiry_date", {}).get("date") if ocr_results.get("expiry_date") else None
        ocr_batch = ocr_results.get("batch_number")
        product_name = ocr_results.get("product_name")

        print(f"OCR - Product: {product_name}, Expiry: {ocr_expiry}, Batch: {ocr_batch}")

        # Step 4: Determine final expiry date (prefer barcode, fallback to OCR)
        final_expiry = barcode_expiry or ocr_expiry
        final_batch = batch_from_barcode or ocr_batch

        # Step 5: Verify GTIN against GS1 database
        print("Step 5: Verifying GTIN with GS1...")
        gs1_data = None
        if gtin:
            gs1_scraper = GS1Scraper()
            gs1_data = gs1_scraper.verify_gtin(gtin)
            print(f"GS1 verification: {gs1_data}")

        # Step 6: Check regulatory database (CDSCO)
        print("Step 6: Checking CDSCO...")
        cdsco_data = None
        if product_name or gtin:
            cdsco_scraper = CDSCOScraper()
            manufacturer = gs1_data.get("company_name") if gs1_data else None
            cdsco_data = cdsco_scraper.search_drug(
                drug_name=product_name,
                license_number=None  # Would need to extract from packaging
            )

            # Check for counterfeit alerts
            if product_name or manufacturer:
                alerts = cdsco_scraper.check_counterfeit_alerts(product_name, manufacturer)
                if alerts:
                    if not cdsco_data:
                        cdsco_data = {}
                    cdsco_data["warnings"] = alerts

            print(f"CDSCO verification: {cdsco_data}")

        # Step 7: Perform comprehensive authenticity check
        print("Step 7: Performing authenticity check...")
        authenticity_result = verify_authenticity(
            gtin=gtin,
            expiry_date=final_expiry,
            batch_number=final_batch,
            product_name=product_name,
            gs1_data=gs1_data,
            cdsco_data=cdsco_data,
            ocr_data=ocr_results
        )

        print(f"Authenticity result: {authenticity_result['status']}, Risk: {authenticity_result['risk_level']}")

        # Step 8: Build response
        manufacturer = None
        country = None

        if gs1_data and gs1_data.get("found"):
            manufacturer = gs1_data.get("company_name")
            country = gs1_data.get("country")

        response = VerificationResponse(
            status=authenticity_result["status"],
            risk_level=authenticity_result["risk_level"],
            is_expired=authenticity_result["is_expired"],
            expiry_date=authenticity_result["expiry_date"],
            gtin=gtin,
            gtin_verified=authenticity_result["gtin_verified"],
            product_name=product_name,
            batch_number=final_batch,
            manufacturer=manufacturer,
            country=country,
            risk_factors=authenticity_result["risk_factors"],
            recommendations=authenticity_result["recommendations"],
            details=authenticity_result["details"],
            raw_data={
                "barcodes": [
                    {
                        "type": bc["type"],
                        "data": bc["raw_data"],
                        "parsed": bc["parsed"]
                    }
                    for bc in all_barcodes
                ],
                "ocr_texts": [
                    {
                        "text_preview": t["text"][:200] + "..." if len(t["text"]) > 200 else t["text"],
                        "quality_score": t["quality"]["quality_score"]
                    }
                    for t in ocr_results.get("all_texts", [])
                ],
                "gs1_verification": gs1_data,
                "cdsco_verification": cdsco_data
            }
        )

        return response

    except Exception as e:
        print(f"Verification error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.post("/verify-barcode")
async def verify_barcode_only(gtin: str):
    """
    Verify a GTIN/barcode without uploading images

    Useful for manual barcode entry
    """
    try:
        gs1_scraper = GS1Scraper()
        result = gs1_scraper.verify_gtin(gtin)

        is_valid = gs1_scraper.validate_gtin_checksum(gtin)

        return {
            "gtin": gtin,
            "checksum_valid": is_valid,
            "verification": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "MediScan API v2",
        "version": "2.0.0",
        "description": "Medicine Expiry and Authenticity Detection System",
        "endpoints": {
            "/health": "Health check",
            "/verify": "Verify medicine from images (POST)",
            "/verify-barcode": "Verify GTIN/barcode only (POST)",
            "/docs": "API documentation (Swagger UI)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
