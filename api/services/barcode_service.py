"""
Barcode and QR Code Detection Service
Handles detection, decoding, and parsing of GS1 codes
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode as zbar_decode, ZBarSymbol
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from .image_processor import ImageProcessor


class BarcodeService:
    """Service for barcode and QR code detection and parsing"""

    def __init__(self):
        self.processor = ImageProcessor()
        self.FNC1 = "\x1D"  # GS1 FNC1 separator

    def detect_and_decode(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect and decode all barcodes/QR codes in image

        Args:
            image: Input image

        Returns:
            List of detected codes with metadata
        """
        results = []

        # Try multiple preprocessed versions for better detection
        image_variations = self.processor.preprocess_for_barcode(image)

        for idx, variant in enumerate(image_variations):
            codes = self._decode_barcodes(variant)

            for code in codes:
                # Parse the code data
                parsed = self._parse_code_data(code["data"], code["type"])

                result = {
                    "type": code["type"],
                    "raw_data": code["data"],
                    "parsed": parsed,
                    "location": code.get("location"),
                    "variant_index": idx
                }

                # Avoid duplicates
                if not self._is_duplicate(results, result):
                    results.append(result)

        return results

    def _decode_barcodes(self, image: np.ndarray) -> List[Dict[str, str]]:
        """
        Decode barcodes from preprocessed image

        Args:
            image: Preprocessed image

        Returns:
            List of decoded barcodes
        """
        results = []

        try:
            # Define symbol types to look for
            symbols = self._get_available_symbols()

            decoded_objects = zbar_decode(image, symbols=symbols)

            for obj in decoded_objects:
                results.append({
                    "type": obj.type,
                    "data": obj.data.decode("utf-8", errors="ignore"),
                    "location": {
                        "points": [(p.x, p.y) for p in obj.polygon],
                        "rect": obj.rect
                    }
                })

        except Exception as e:
            print(f"Barcode decoding error: {e}")

        return results

    def _get_available_symbols(self) -> List:
        """Get list of available ZBar symbol types"""
        symbol_names = ["QRCODE", "EAN13", "EAN8", "CODE128", "CODE39", "UPCA", "UPCE", "PDF417", "DATAMATRIX"]
        symbols = []

        for name in symbol_names:
            if hasattr(ZBarSymbol, name):
                symbols.append(getattr(ZBarSymbol, name))

        return symbols

    def _parse_code_data(self, data: str, code_type: str) -> Dict[str, Any]:
        """
        Parse barcode data based on type

        Args:
            data: Raw barcode data
            code_type: Type of barcode

        Returns:
            Parsed data dictionary
        """
        parsed = {
            "gtin": None,
            "expiry": None,
            "batch": None,
            "serial": None,
            "is_gs1": False,
            "digital_link": None
        }

        # Check if it's a GS1 code
        if code_type == "QRCODE" and ("http" in data or "01" in data[:10]):
            # Could be GS1 Digital Link or GS1 AI format
            if "http" in data:
                parsed["digital_link"] = data
                parsed["is_gs1"] = True
                parsed.update(self._parse_digital_link(data))
            else:
                parsed["is_gs1"] = True
                parsed.update(self._parse_gs1_ai(data))

        elif code_type in ["CODE128", "PDF417"]:
            # Could be GS1-128 or GS1 DataBar
            parsed["is_gs1"] = True
            parsed.update(self._parse_gs1_ai(data))

        elif code_type in ["EAN13", "EAN8", "UPCA", "UPCE"]:
            # Standard product barcodes
            parsed["gtin"] = data
            parsed["is_gs1"] = True

        return parsed

    def _parse_gs1_ai(self, raw: str) -> Dict[str, Any]:
        """
        Parse GS1 Application Identifiers from barcode data

        Args:
            raw: Raw barcode string

        Returns:
            Dictionary with extracted GS1 fields
        """
        # Replace FNC1 with pipe for easier parsing
        s = raw.replace(self.FNC1, "|")

        result = {}

        # AI (01) - GTIN (14 digits)
        match = self._extract_ai(s, "01", 14)
        if match:
            result["gtin"] = match

        # AI (17) - Expiry Date (YYMMDD)
        match = self._extract_ai(s, "17", 6)
        if match:
            result["expiry"] = self._parse_gs1_date(match)

        # AI (10) - Batch/Lot Number
        match = self._extract_ai_variable(s, "10")
        if match:
            result["batch"] = match

        # AI (21) - Serial Number
        match = self._extract_ai_variable(s, "21")
        if match:
            result["serial"] = match

        # AI (11) - Production Date
        match = self._extract_ai(s, "11", 6)
        if match:
            result["production_date"] = self._parse_gs1_date(match)

        # AI (15) - Best Before Date
        match = self._extract_ai(s, "15", 6)
        if match:
            result["best_before"] = self._parse_gs1_date(match)

        return result

    def _extract_ai(self, data: str, ai: str, length: int) -> Optional[str]:
        """Extract fixed-length AI value"""
        # Try with parentheses
        pattern = rf"\({ai}\)(\d{{{length}}})"
        match = re.search(pattern, data)
        if match:
            return match.group(1)

        # Try without parentheses
        pattern = rf"{ai}(\d{{{length}}})"
        match = re.search(pattern, data)
        if match:
            return match.group(1)

        return None

    def _extract_ai_variable(self, data: str, ai: str) -> Optional[str]:
        """Extract variable-length AI value"""
        # Try with parentheses (terminated by next AI or separator)
        pattern = rf"\({ai}\)([^\(\|\n\r]+)"
        match = re.search(pattern, data)
        if match:
            return match.group(1).strip()

        # Try without parentheses (terminated by separator)
        pattern = rf"{ai}([^\|\n\r]+)"
        match = re.search(pattern, data)
        if match:
            return match.group(1).strip()

        return None

    def _parse_gs1_date(self, yymmdd: str) -> Optional[date]:
        """
        Parse GS1 date format (YYMMDD)

        Args:
            yymmdd: Date in YYMMDD format

        Returns:
            date object
        """
        try:
            dt = datetime.strptime(yymmdd, "%y%m%d").date()
            return dt
        except Exception:
            return None

    def _parse_digital_link(self, url: str) -> Dict[str, Any]:
        """
        Parse GS1 Digital Link URL

        Args:
            url: GS1 Digital Link URL

        Returns:
            Extracted data
        """
        result = {}

        # Extract GTIN from URL path
        # Format: https://example.com/01/12345678901234/...
        import re

        gtin_match = re.search(r"/01/(\d{14})", url)
        if gtin_match:
            result["gtin"] = gtin_match.group(1)

        # Extract other AIs from URL
        expiry_match = re.search(r"/17/(\d{6})", url)
        if expiry_match:
            result["expiry"] = self._parse_gs1_date(expiry_match.group(1))

        batch_match = re.search(r"/10/([^/\?]+)", url)
        if batch_match:
            result["batch"] = batch_match.group(1)

        serial_match = re.search(r"/21/([^/\?]+)", url)
        if serial_match:
            result["serial"] = serial_match.group(1)

        return result

    def _is_duplicate(self, existing: List[Dict], new: Dict) -> bool:
        """Check if code is already in results"""
        for item in existing:
            if item["raw_data"] == new["raw_data"] and item["type"] == new["type"]:
                return True
        return False

    def validate_gtin(self, gtin: str) -> bool:
        """
        Validate GTIN checksum

        Args:
            gtin: GTIN string

        Returns:
            True if valid
        """
        if not gtin.isdigit():
            return False

        if len(gtin) not in [8, 12, 13, 14]:
            return False

        # GS1 checksum algorithm
        digits = [int(d) for d in gtin[:-1]]
        check_digit = int(gtin[-1])

        total = 0
        multiplier = [3, 1]

        for i, digit in enumerate(reversed(digits)):
            total += digit * multiplier[i % 2]

        calculated = (10 - (total % 10)) % 10

        return calculated == check_digit


import re


def detect_barcodes_multi_image(images: List[np.ndarray]) -> List[Dict[str, Any]]:
    """
    Detect barcodes from multiple images

    Args:
        images: List of images

    Returns:
        Combined barcode detection results
    """
    service = BarcodeService()
    all_results = []

    for idx, image in enumerate(images):
        codes = service.detect_and_decode(image)
        for code in codes:
            code["source_image"] = idx
            all_results.append(code)

    return all_results


if __name__ == "__main__":
    print("Barcode service module loaded successfully")
