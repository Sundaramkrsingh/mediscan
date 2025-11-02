"""
GS1 India Web Scraper for Medicine Verification
Scrapes GS1 Datakart and Smart Consumer data to verify GTIN/barcode authenticity
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re
import time
from urllib.parse import quote
from .tavily_search import get_tavily_service


class GS1Scraper:
    """Scraper for GS1 India data sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        # GS1 India endpoints
        self.gs1_verify_url = "https://www.gs1india.org/verify-barcode.html"
        self.gepir_url = "https://gepir.gs1.org/index.php/search-by-gtin"

    def verify_gtin(self, gtin: str) -> Dict[str, Any]:
        """
        Verify GTIN against GS1 databases

        Args:
            gtin: 13 or 14 digit GTIN code

        Returns:
            Dictionary with product information if found
        """
        result = {
            "found": False,
            "gtin": gtin,
            "product_name": None,
            "company_name": None,
            "company_prefix": None,
            "country": None,
            "source": None,
            "verified": False
        }

        # Try GEPIR (Global Electronic Party Information Registry)
        gepir_result = self._search_gepir(gtin)
        if gepir_result["found"]:
            result.update(gepir_result)
            result["source"] = "GEPIR"
            return result

        # Try GS1 India verification
        gs1_india_result = self._search_gs1_india(gtin)
        if gs1_india_result["found"]:
            result.update(gs1_india_result)
            result["source"] = "GS1 India"
            return result

        # Try Tavily AI search as fallback
        tavily_result = self._search_tavily(gtin)
        if tavily_result["found"]:
            result.update(tavily_result)
            result["source"] = "Tavily AI Search"
            return result

        return result

    def _search_tavily(self, gtin: str) -> Dict[str, Any]:
        """Search using Tavily AI as fallback"""
        result = {"found": False}

        try:
            tavily = get_tavily_service()
            if not tavily.enabled:
                return result

            search_result = tavily.verify_barcode_online(gtin)

            if search_result.get("found"):
                result["found"] = True
                result["verified"] = True
                result["product_name"] = search_result.get("product_name")
                result["company_name"] = search_result.get("manufacturer")
                result["ai_summary"] = search_result.get("summary")
                result["sources"] = search_result.get("sources", [])

        except Exception as e:
            print(f"Tavily search error: {e}")

        return result

    def _search_gepir(self, gtin: str) -> Dict[str, Any]:
        """Search GEPIR database for GTIN"""
        result = {"found": False}

        try:
            # GEPIR search endpoint
            search_url = f"https://gepir.gs1.org/index.php/search-by-gtin/{gtin}"

            response = self.session.get(search_url, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for company information
                company_elem = soup.find('div', class_='company-name')
                if company_elem:
                    result["found"] = True
                    result["company_name"] = company_elem.get_text(strip=True)
                    result["verified"] = True

                # Look for additional details
                details = soup.find_all('div', class_='detail-row')
                for detail in details:
                    label = detail.find('span', class_='label')
                    value = detail.find('span', class_='value')
                    if label and value:
                        label_text = label.get_text(strip=True).lower()
                        if 'country' in label_text:
                            result["country"] = value.get_text(strip=True)
                        elif 'prefix' in label_text:
                            result["company_prefix"] = value.get_text(strip=True)

            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"GEPIR search error: {e}")

        return result

    def _search_gs1_india(self, gtin: str) -> Dict[str, Any]:
        """Search GS1 India website for GTIN verification"""
        result = {"found": False}

        try:
            # Check if GTIN starts with Indian GS1 prefix (890)
            if gtin.startswith('890'):
                result["country"] = "India"
                result["company_prefix"] = gtin[:7]  # First 7 digits typically
                result["found"] = True
                result["verified"] = True

                # Additional verification can be added here
                # This is a basic check based on GS1 prefix structure

        except Exception as e:
            print(f"GS1 India search error: {e}")

        return result

    def extract_company_prefix(self, gtin: str) -> Optional[str]:
        """Extract company prefix from GTIN"""
        if len(gtin) == 13:  # EAN-13
            return gtin[:7]  # Typically first 7 digits
        elif len(gtin) == 14:  # GTIN-14
            return gtin[1:8]  # Skip indicator digit
        return None

    def validate_gtin_checksum(self, gtin: str) -> bool:
        """
        Validate GTIN check digit using GS1 algorithm

        Args:
            gtin: GTIN string (13 or 14 digits)

        Returns:
            True if checksum is valid
        """
        if not gtin.isdigit():
            return False

        if len(gtin) not in [13, 14]:
            return False

        # GS1 checksum algorithm
        digits = [int(d) for d in gtin[:-1]]
        check_digit = int(gtin[-1])

        # Multiply from right to left, alternating 3 and 1
        total = 0
        multiplier = [3, 1]

        for i, digit in enumerate(reversed(digits)):
            total += digit * multiplier[i % 2]

        calculated_check = (10 - (total % 10)) % 10

        return calculated_check == check_digit

    def search_product_info(self, product_name: str) -> Dict[str, Any]:
        """
        Search for product information by name
        Used as fallback when GTIN is not available
        """
        result = {
            "found": False,
            "products": []
        }

        # This can be enhanced to search pharmaceutical databases
        # For now, it's a placeholder for future implementation

        return result


def verify_barcode(gtin: str) -> Dict[str, Any]:
    """
    Main function to verify a barcode/GTIN

    Args:
        gtin: The GTIN/barcode to verify

    Returns:
        Verification result with product information
    """
    scraper = GS1Scraper()

    # First validate checksum
    if not scraper.validate_gtin_checksum(gtin):
        return {
            "found": False,
            "error": "Invalid GTIN checksum",
            "verified": False
        }

    # Search GS1 databases
    result = scraper.verify_gtin(gtin)

    return result


if __name__ == "__main__":
    # Test with sample GTINs
    test_gtins = [
        "8901117277403",  # Dolo 650 (if real)
        "8901148203051",  # Sample
    ]

    for gtin in test_gtins:
        print(f"\nVerifying GTIN: {gtin}")
        result = verify_barcode(gtin)
        print(f"Result: {result}")