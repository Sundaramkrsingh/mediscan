"""
CDSCO (Central Drugs Standard Control Organization) Web Scraper
Scrapes CDSCO website for drug registration and approval information
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List
import re
import time
from .tavily_search import get_tavily_service


class CDSCOScraper:
    """Scraper for CDSCO India data sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        # CDSCO endpoints
        self.cdsco_base_url = "https://cdsco.gov.in"
        self.approved_drugs_url = f"{self.cdsco_base_url}/opencms/opencms/en/Drugs/"

    def search_drug(self, drug_name: str = None, license_number: str = None) -> Dict[str, Any]:
        """
        Search for drug information in CDSCO database

        Args:
            drug_name: Name of the drug
            license_number: Manufacturing license number

        Returns:
            Dictionary with drug information if found
        """
        result = {
            "found": False,
            "drug_name": drug_name,
            "license_number": license_number,
            "manufacturer": None,
            "approval_status": None,
            "warnings": [],
            "source": "CDSCO"
        }

        if license_number:
            license_result = self._search_by_license(license_number)
            if license_result["found"]:
                result.update(license_result)
                return result

        if drug_name:
            drug_result = self._search_by_name(drug_name)
            if drug_result["found"]:
                result.update(drug_result)
                return result

        # Try Tavily AI search as fallback
        tavily_result = self._search_tavily(drug_name)
        if tavily_result["found"]:
            result.update(tavily_result)
            result["source"] = "Tavily AI Search + CDSCO"
            return result

        return result

    def _search_tavily(self, drug_name: str) -> Dict[str, Any]:
        """Search using Tavily AI for drug information"""
        result = {"found": False}

        try:
            tavily = get_tavily_service()
            if not tavily.enabled:
                return result

            search_result = tavily.get_medicine_details(drug_name)

            if search_result.get("found"):
                result["found"] = True
                result["manufacturer"] = search_result.get("manufacturer")
                result["ai_summary"] = search_result.get("summary")
                result["composition"] = search_result.get("composition")
                result["therapeutic_use"] = search_result.get("therapeutic_use")
                result["sources"] = search_result.get("sources", [])

        except Exception as e:
            print(f"Tavily medicine search error: {e}")

        return result

    def _search_by_license(self, license_number: str) -> Dict[str, Any]:
        """Search by manufacturing license number"""
        result = {"found": False}

        try:
            # CDSCO doesn't have a direct API, so this is a placeholder
            # In practice, you'd need to navigate through their portal
            # or use the DAVA portal if you have access

            # Placeholder implementation
            # Real implementation would require detailed scraping or API access
            pass

        except Exception as e:
            print(f"License search error: {e}")

        return result

    def _search_by_name(self, drug_name: str) -> Dict[str, Any]:
        """Search by drug name"""
        result = {"found": False}

        try:
            # Placeholder for drug name search
            # Would require accessing CDSCO's approved drugs list
            pass

        except Exception as e:
            print(f"Drug name search error: {e}")

        return result

    def check_counterfeit_alerts(self, drug_name: str = None, manufacturer: str = None) -> List[Dict[str, Any]]:
        """
        Check CDSCO's counterfeit drug alerts

        Args:
            drug_name: Name of the drug to check
            manufacturer: Manufacturer name

        Returns:
            List of alerts if any found
        """
        alerts = []

        try:
            # CDSCO publishes alerts about counterfeit drugs
            # This would scrape their alerts page
            alerts_url = f"{self.cdsco_base_url}/opencms/opencms/en/Drugs/Drugs-Alert/"

            response = self.session.get(alerts_url, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for alert content
                alert_sections = soup.find_all('div', class_=['alert-content', 'content'])

                for section in alert_sections:
                    text = section.get_text(strip=True).lower()

                    # Check if drug name or manufacturer mentioned
                    if drug_name and drug_name.lower() in text:
                        alerts.append({
                            "type": "counterfeit_alert",
                            "description": section.get_text(strip=True)[:200],
                            "match": drug_name
                        })
                    elif manufacturer and manufacturer.lower() in text:
                        alerts.append({
                            "type": "manufacturer_alert",
                            "description": section.get_text(strip=True)[:200],
                            "match": manufacturer
                        })

            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"Alert check error: {e}")

        # Also check using Tavily AI
        try:
            tavily = get_tavily_service()
            if tavily.enabled:
                tavily_alerts = tavily.check_counterfeit_reports(drug_name, manufacturer)
                if tavily_alerts.get("alerts_found"):
                    for warning in tavily_alerts.get("warnings", []):
                        alerts.append({
                            "type": "tavily_ai_alert",
                            "description": warning.get("snippet"),
                            "source": warning.get("source"),
                            "severity": warning.get("severity", "MEDIUM"),
                            "match": drug_name or manufacturer
                        })
        except Exception as e:
            print(f"Tavily alert check error: {e}")

        return alerts


class DAVAPortalScraper:
    """
    Scraper for DAVA Portal (Directorate General of Foreign Trade)
    Used for pharmaceutical export verification
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.dava_url = "https://dava.dgft.gov.in"

    def verify_export_barcode(self, gtin: str) -> Dict[str, Any]:
        """
        Verify barcode against DAVA portal for export medicines

        Args:
            gtin: GTIN barcode

        Returns:
            Verification result
        """
        result = {
            "found": False,
            "gtin": gtin,
            "export_approved": False,
            "source": "DAVA Portal"
        }

        try:
            # DAVA portal verification
            # This would require authentication and proper API access
            # Placeholder implementation
            pass

        except Exception as e:
            print(f"DAVA verification error: {e}")

        return result


def verify_drug_regulatory(drug_name: str = None, license_number: str = None, manufacturer: str = None) -> Dict[str, Any]:
    """
    Main function to verify drug against CDSCO regulatory database

    Args:
        drug_name: Name of the drug
        license_number: Manufacturing license
        manufacturer: Manufacturer name

    Returns:
        Regulatory verification result
    """
    scraper = CDSCOScraper()

    # Search drug information
    result = scraper.search_drug(drug_name, license_number)

    # Check for counterfeit alerts
    alerts = scraper.check_counterfeit_alerts(drug_name, manufacturer)
    if alerts:
        result["warnings"] = alerts
        result["risk_level"] = "HIGH" if len(alerts) > 0 else "LOW"

    return result


if __name__ == "__main__":
    # Test CDSCO scraper
    print("Testing CDSCO scraper...")
    result = verify_drug_regulatory(drug_name="Dolo 650", manufacturer="Micro Labs")
    print(f"Result: {result}")
