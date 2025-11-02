"""
Enhanced OCR Service for Medicine Label Text Extraction
Supports multi-image analysis and advanced text extraction
"""

import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime, date
from dateutil.parser import parse as dateparse
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Optional, Tuple, Any
from .image_processor import ImageProcessor


class OCRService:
    """Advanced OCR service for medicine packaging"""

    def __init__(self, tesseract_cmd: Optional[str] = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        self.processor = ImageProcessor()

        # Date patterns for expiry detection
        self.date_patterns = [
            r"\b(0?[1-9]|1[0-2])[\/\-\.\|Il:,](\d{2})\b",  # MM/YY (OCR might read / as |, I, l, :, or ,)
            r"\b(0?[1-9]|1[0-2])[\/\-\.\|Il:,](\d{4})\b",  # MM/YYYY
            r"\b(0?[1-9]|[12]\d|3[01])[\/\-\.\|Il:,](0?[1-9]|1[0-2])[\/\-\.\|Il:,](\d{2,4})\b",  # DD/MM/YY
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC|JUH|JUt)[a-z\.\-]*[\s\-\.]*(\d{2,4})",  # Month YYYY (loose)
            r"(\d{2,4})[\s\-\.](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|SEPT|OCT|NOV|DEC)[a-z]*",  # YYYY Month
            r"\b(\d{2})[\s]*[\/\-\.\|Il:,][\s]*(\d{2})\b",  # MM/YY with spaces and OCR errors
            r"(\d{1,2})[\s]+(\d{2,4})\b",  # Loose pattern: "08 22" or "7 2024"
            r"[A-Z]{3,4}[\.\-\s]*(\d{2})",  # Very loose: "JUH 25" or "MAR.24"
        ]

        # Month name variations (including OCR errors)
        self.month_map = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
            'JUL': 7, 'AUG': 8, 'SEP': 9, 'SEPT': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12,
            'JUH': 6, 'JUt': 7, 'JUI': 7, 'JULY': 7, 'JUNE': 6, 'JUME': 6,  # Common OCR errors
            'JAH': 1, 'FE8': 2, 'FE3': 2, 'MAY': 5, 'MA¥': 5,
        }

        # Keywords that typically appear near expiry dates
        self.expiry_keywords = r"(EXP|EXPIRY|EXPIRES?|USE\s+BY|BEST\s+BEFORE|VALID\s+UNTIL|EXPDT|EXP\s*DATE|EXPIRY\s*DATE)"
        self.mfg_keywords = r"(MFG|MFD|MANUFACTURED|PRODUCTION|MFG\s*DATE|MANUF|MFD\s*DATE)"
        self.batch_keywords = r"(BATCH|LOT|B\.?NO|L\.?NO|BATCH\s*NO|LOT\s*NO)"

    def extract_text_from_image(self, image: np.ndarray, preprocess: bool = True) -> str:
        """
        Extract text from image using OCR with multiple strategies

        Args:
            image: Input image
            preprocess: Whether to preprocess image

        Returns:
            Extracted text
        """
        all_text = []

        # Strategy 1: Try different rotations (0, 90, 180, 270)
        for angle in [0, 90, 180, 270]:
            if angle == 0:
                rotated = image
            else:
                rotated = self._rotate_image(image, angle)

            if preprocess:
                processed = self.processor.preprocess_for_ocr(rotated)
            else:
                processed = rotated

            configs = [
                "--oem 3 --psm 6 -l eng",  # Uniform block of text
                "--oem 3 --psm 11 -l eng",  # Sparse text
            ]

            for config in configs:
                try:
                    text = pytesseract.image_to_string(processed, config=config)
                    if text.strip():
                        # Check if this orientation has readable text (contains common words)
                        word_count = len([w for w in text.split() if len(w) > 2])
                        if word_count > 5:  # Reasonable amount of text
                            all_text.append(text)
                except Exception as e:
                    print(f"[OCR] Error with {config} at {angle}°: {e}")

        # Strategy 2: Enhanced preprocessing for date detection
        try:
            date_enhanced = self.processor.enhance_for_expiry_date(image)
            text = pytesseract.image_to_string(date_enhanced, config="--oem 3 --psm 6 -l eng")
            if text.strip():
                all_text.append(text)
        except Exception as e:
            print(f"[OCR] Error with date enhancement: {e}")

        # Combine all text results
        combined = "\n".join(all_text)
        return combined if combined else ""

    def _rotate_image(self, image: np.ndarray, angle: int) -> np.ndarray:
        """Rotate image by specified angle (90, 180, 270)"""
        if angle == 0:
            return image
        elif angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image

    def extract_from_multiple_images(self, images: List[np.ndarray]) -> Dict[str, Any]:
        """
        Extract and combine text from multiple images

        Args:
            images: List of images

        Returns:
            Combined extraction results
        """
        all_texts = []
        expiry_candidates = []
        mfg_candidates = []
        batch_candidates = []

        for idx, image in enumerate(images):
            # Assess image quality
            quality = self.processor.assess_image_quality(image)

            # Extract text
            text = self.extract_text_from_image(image)
            all_texts.append({
                "image_index": idx,
                "text": text,
                "quality": quality
            })


            # Extract specific information
            expiry = self.extract_expiry_date(text)
            if expiry:
                expiry_candidates.append({
                    "date": expiry["date"],
                    "confidence": expiry["confidence"],
                    "source_text": expiry["snippet"],
                    "image_index": idx
                })

            mfg = self.extract_manufacturing_date(text)
            if mfg:
                mfg_candidates.append({
                    "date": mfg["date"],
                    "source_text": mfg["snippet"],
                    "image_index": idx
                })

            batch = self.extract_batch_number(text)
            if batch:
                batch_candidates.append({
                    "batch": batch,
                    "image_index": idx
                })

        # Choose best candidates
        best_expiry = self._select_best_expiry(expiry_candidates)
        best_mfg = self._select_best_mfg(mfg_candidates)
        best_batch = self._select_best_batch(batch_candidates)

        return {
            "all_texts": all_texts,
            "expiry_date": best_expiry,
            "manufacturing_date": best_mfg,
            "batch_number": best_batch,
            "product_name": self._extract_product_name(all_texts),
        }

    def extract_expiry_date(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract expiry date from OCR text

        Args:
            text: OCR extracted text

        Returns:
            Dictionary with expiry date information
        """
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        # First pass: Look for dates near expiry keywords
        for line in lines:
            if re.search(self.expiry_keywords, line, re.IGNORECASE):
                # Try to extract the entire rest of the line after the keyword
                keyword_match = re.search(self.expiry_keywords, line, re.IGNORECASE)
                if keyword_match:
                    rest_of_line = line[keyword_match.end():].strip()

                    # Try all patterns on the rest of the line
                    for pattern in self.date_patterns:
                        match = re.search(pattern, rest_of_line, re.IGNORECASE)
                        if match:
                            parsed_date = self._normalize_date(match.group(0))
                            if parsed_date:
                                return {
                                    "date": parsed_date,
                                    "snippet": line,
                                    "confidence": "high"
                                }

        # Second pass: Look near expiry keywords (date might be on next line)
        for i, line in enumerate(lines):
            if re.search(self.expiry_keywords, line, re.IGNORECASE):
                # Check current line and next 2 lines
                check_lines = lines[i:min(i+3, len(lines))]
                for check_line in check_lines:
                    for pattern in self.date_patterns:
                        match = re.search(pattern, check_line, re.IGNORECASE)
                        if match:
                            parsed_date = self._normalize_date(match.group(0))
                            if parsed_date:
                                return {
                                    "date": parsed_date,
                                    "snippet": check_line,
                                    "confidence": "medium"
                                }

        # Third pass: Look for any dates (prefer future dates, but accept past if reasonable)
        all_dates = []
        for line in lines:
            # Try exact patterns first
            for pattern in self.date_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    parsed_date = self._normalize_date(match.group(0))
                    if parsed_date:
                        # Accept dates from 2020 onwards (reasonable for medicine)
                        if parsed_date.year >= 2020:
                            all_dates.append({
                                "date": parsed_date,
                                "snippet": line,
                                "is_future": parsed_date > date.today()
                            })

            # Also try fuzzy extraction: look for any 2-digit year preceded by text
            fuzzy_match = re.search(r'([A-Z]{2,4})[^\d]{0,3}(\d{2})(?:\D|$)', line, re.IGNORECASE)
            if fuzzy_match and not all_dates:  # Only if no dates found yet
                potential_month = fuzzy_match.group(1).upper()
                potential_year = fuzzy_match.group(2)

                # Check if the text looks like a month
                for month_key in self.month_map.keys():
                    if month_key[:3] in potential_month[:3] or potential_month[:3] in month_key[:3]:
                        month_num = self.month_map[month_key]
                        year = 2000 + int(potential_year) if int(potential_year) < 50 else 1900 + int(potential_year)
                        try:
                            dt = date(year, month_num, 1) + relativedelta(months=1) - relativedelta(days=1)
                            if dt.year >= 2020:
                                all_dates.append({
                                    "date": dt,
                                    "snippet": line,
                                    "is_future": dt > date.today()
                                })
                                break
                        except:
                            pass

        # Prefer future dates, but accept recent past dates if no future date found
        if all_dates:
            future_dates = [d for d in all_dates if d["is_future"]]
            if future_dates:
                result = future_dates[0]
            else:
                # Use most recent date
                result = max(all_dates, key=lambda x: x["date"])

            return {
                "date": result["date"],
                "snippet": result["snippet"],
                "confidence": "low" if not result["is_future"] else "medium"
            }

        return None

    def extract_manufacturing_date(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract manufacturing date from text"""
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        for line in lines:
            if re.search(self.mfg_keywords, line, re.IGNORECASE):
                for pattern in self.date_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        parsed_date = self._normalize_date(match.group(0))
                        if parsed_date and parsed_date <= date.today():
                            return {
                                "date": parsed_date,
                                "snippet": line
                            }

        return None

    def extract_batch_number(self, text: str) -> Optional[str]:
        """Extract batch/lot number from text"""
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        for line in lines:
            if re.search(self.batch_keywords, line, re.IGNORECASE):
                # Extract alphanumeric code after keyword
                match = re.search(
                    r"(?:BATCH|LOT|B\.?NO|L\.?NO)[\s:]+([A-Z0-9]+)",
                    line,
                    re.IGNORECASE
                )
                if match:
                    return match.group(1)

        return None

    def _normalize_date(self, date_string: str) -> Optional[date]:
        """
        Normalize various date formats to date object

        Args:
            date_string: Date string in various formats

        Returns:
            date object or None
        """
        original_string = date_string
        # Clean up OCR errors: replace common misreads with /
        date_string = date_string.strip()
        date_string = re.sub(r'[|Il:,]', '/', date_string)  # Replace OCR errors with /

        # Try to extract month name with fuzzy matching
        for month_str, month_num in self.month_map.items():
            if month_str.upper() in date_string.upper():
                # Extract year from the string
                year_match = re.search(r'(\d{2,4})', date_string)
                if year_match:
                    year_str = year_match.group(1)
                    year = int(year_str)
                    if year < 100:
                        year = 2000 + year if year < 50 else 1900 + year

                    # Create date as last day of that month
                    try:
                        dt = date(year, month_num, 1) + relativedelta(months=1) - relativedelta(days=1)
                        return dt
                    except Exception:
                        pass

        date_string = date_string.replace(" ", "")

        # Try explicit formats first
        formats = [
            "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
            "%d/%m/%y", "%d-%m-%y", "%d.%m.%y",
            "%m/%Y", "%m-%Y", "%m.%Y",
            "%m/%y", "%m-%y", "%m.%y",
            "%Y-%m-%d", "%Y/%m/%d",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_string, fmt).date()

                # If only month/year, return last day of month
                if fmt in ("%m/%Y", "%m-%Y", "%m.%Y", "%m/%y", "%m-%y", "%m.%y"):
                    first_next = date(dt.year, dt.month, 1) + relativedelta(months=1)
                    dt = first_next - relativedelta(days=1)

                # Handle 2-digit years
                if dt.year < 100:
                    if dt.year < 50:
                        dt = dt.replace(year=dt.year + 2000)
                    else:
                        dt = dt.replace(year=dt.year + 1900)

                return dt
            except ValueError:
                continue

        # Try month name formats
        month_formats = ["%b%Y", "%B%Y", "%Y%b", "%Y%B"]
        for fmt in month_formats:
            try:
                dt = datetime.strptime(date_string, fmt).date()
                first_next = date(dt.year, dt.month, 1) + relativedelta(months=1)
                dt = first_next - relativedelta(days=1)
                return dt
            except ValueError:
                continue

        # Try dateutil as fallback
        try:
            original = date_string
            date_string_with_space = re.sub(r"(\d{2})", r"\1 ", date_string, count=1).strip()
            dt = dateparse(date_string_with_space, dayfirst=True, default=datetime.today()).date()

            # If no day specified, use end of month
            if not re.search(r"\b([12]\d|3[01])\b", original):
                first_next = date(dt.year, dt.month, 1) + relativedelta(months=1)
                dt = first_next - relativedelta(days=1)

            return dt
        except Exception:
            return None

    def _select_best_expiry(self, candidates: List[Dict]) -> Optional[Dict]:
        """Select the most reliable expiry date from candidates"""
        if not candidates:
            return None

        # Sort by confidence and recency
        high_conf = [c for c in candidates if c.get("confidence") == "high"]
        if high_conf:
            return high_conf[0]

        return candidates[0] if candidates else None

    def _select_best_mfg(self, candidates: List[Dict]) -> Optional[Dict]:
        """Select best manufacturing date"""
        if not candidates:
            return None

        # Select earliest manufacturing date
        return min(candidates, key=lambda x: x["date"])

    def _select_best_batch(self, candidates: List[str]) -> Optional[str]:
        """Select most common batch number"""
        if not candidates:
            return None

        # Return most frequent
        from collections import Counter
        counter = Counter(c["batch"] for c in candidates)
        return counter.most_common(1)[0][0] if counter else None

    def _extract_product_name(self, text_results: List[Dict]) -> Optional[str]:
        """
        Extract product/medicine name from OCR text
        Usually the largest/most prominent text at the top
        """
        if not text_results:
            return None

        # Get highest quality text
        best_text = max(text_results, key=lambda x: x["quality"]["quality_score"])
        lines = [ln.strip() for ln in best_text["text"].splitlines() if ln.strip()]

        # Product name is typically in first few lines and in CAPS
        for line in lines[:5]:
            # Look for capitalized words
            if len(line) > 3 and line.isupper():
                # Remove common prefixes/suffixes
                name = re.sub(r'\b(TAB|TABLET|CAP|CAPSULE|SYR|SYRUP|INJ|INJECTION)\b', '', line, flags=re.IGNORECASE)
                return name.strip()

        return None


def extract_text_multi_image(images: List[np.ndarray], tesseract_cmd: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for multi-image OCR extraction

    Args:
        images: List of images
        tesseract_cmd: Path to tesseract executable

    Returns:
        Extraction results
    """
    service = OCRService(tesseract_cmd)
    return service.extract_from_multiple_images(images)


if __name__ == "__main__":
    print("OCR service module loaded successfully")
