"""
MediScan Services Package
Contains all core services for medicine verification
"""

from .barcode_service import BarcodeService, detect_barcodes_multi_image
from .ocr_service import OCRService, extract_text_multi_image
from .gs1_scraper import GS1Scraper, verify_barcode
from .cdsco_scraper import CDSCOScraper, verify_drug_regulatory
from .authenticity_checker import AuthenticityChecker, verify_authenticity
from .image_processor import ImageProcessor, preprocess_image

__all__ = [
    "BarcodeService",
    "detect_barcodes_multi_image",
    "OCRService",
    "extract_text_multi_image",
    "GS1Scraper",
    "verify_barcode",
    "CDSCOScraper",
    "verify_drug_regulatory",
    "AuthenticityChecker",
    "verify_authenticity",
    "ImageProcessor",
    "preprocess_image",
]
