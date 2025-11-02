"""
Advanced Tavily AI-Powered Search Service
Uses Tavily API for intelligent web search and drug verification
"""

from typing import Dict, List, Optional, Any
import os
from tavily import TavilyClient


class TavilySearchService:
    """AI-powered search service using Tavily for drug verification"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("Warning: Tavily API key not found. Advanced search disabled.")

    def search_medicine_info(self, product_name: str, manufacturer: str = None) -> Dict[str, Any]:
        """
        Search for comprehensive medicine information using AI

        Args:
            product_name: Name of the medicine
            manufacturer: Optional manufacturer name

        Returns:
            Dictionary with search results and extracted information
        """
        if not self.enabled:
            return {"found": False, "reason": "Tavily API not configured"}

        try:
            # Build search query
            query_parts = [product_name]
            if manufacturer:
                query_parts.append(manufacturer)
            query_parts.extend(["medicine", "pharmaceutical", "India"])

            query = " ".join(query_parts)

            # Perform AI search
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_domains=[
                    "cdsco.gov.in",
                    "gs1india.org",
                    "mohfw.gov.in",
                    "fda.gov",
                    "drugs.com",
                    "medlineplus.gov"
                ]
            )

            # Extract relevant information
            results = {
                "found": len(response.get("results", [])) > 0,
                "query": query,
                "sources": [],
                "summary": response.get("answer", ""),
                "manufacturer_verified": False,
                "regulatory_mentions": []
            }

            for result in response.get("results", []):
                source = {
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content", "")[:500],  # First 500 chars
                    "score": result.get("score", 0)
                }
                results["sources"].append(source)

                # Check for manufacturer verification
                content_lower = result.get("content", "").lower()
                if manufacturer and manufacturer.lower() in content_lower:
                    results["manufacturer_verified"] = True

                # Check for regulatory mentions
                if "cdsco" in content_lower or "fda" in content_lower or "approved" in content_lower:
                    results["regulatory_mentions"].append({
                        "source": result.get("title"),
                        "snippet": result.get("content", "")[:200]
                    })

            return results

        except Exception as e:
            print(f"Tavily search error: {e}")
            return {"found": False, "error": str(e)}

    def verify_barcode_online(self, gtin: str) -> Dict[str, Any]:
        """
        Search for barcode/GTIN information online using AI

        Args:
            gtin: GTIN/barcode number

        Returns:
            Verification results
        """
        if not self.enabled:
            return {"found": False, "reason": "Tavily API not configured"}

        try:
            query = f"GTIN {gtin} pharmaceutical medicine India verification"

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=3,
                include_domains=[
                    "gs1india.org",
                    "gepir.gs1.org",
                    "cdsco.gov.in"
                ]
            )

            results = {
                "found": False,
                "gtin": gtin,
                "product_name": None,
                "manufacturer": None,
                "sources": []
            }

            # Parse results
            for result in response.get("results", []):
                content = result.get("content", "")

                # Try to extract product info from content
                if "product" in content.lower() or "medicine" in content.lower():
                    results["found"] = True
                    results["sources"].append({
                        "title": result.get("title"),
                        "url": result.get("url"),
                        "snippet": content[:300]
                    })

            results["summary"] = response.get("answer", "")

            return results

        except Exception as e:
            print(f"Barcode verification error: {e}")
            return {"found": False, "error": str(e)}

    def check_counterfeit_reports(self, product_name: str, manufacturer: str = None) -> Dict[str, Any]:
        """
        Search for counterfeit alerts and warnings

        Args:
            product_name: Medicine name
            manufacturer: Manufacturer name

        Returns:
            Alert information
        """
        if not self.enabled:
            return {"alerts_found": False, "reason": "Tavily API not configured"}

        try:
            query_parts = [product_name]
            if manufacturer:
                query_parts.append(manufacturer)
            query_parts.extend(["counterfeit", "fake", "alert", "warning", "CDSCO"])

            query = " ".join(query_parts)

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
                include_domains=[
                    "cdsco.gov.in",
                    "mohfw.gov.in",
                    "who.int"
                ]
            )

            alerts = {
                "alerts_found": False,
                "warnings": [],
                "summary": response.get("answer", "")
            }

            # Check for alert keywords
            alert_keywords = ["counterfeit", "fake", "spurious", "warning", "alert", "recalled"]

            for result in response.get("results", []):
                content_lower = result.get("content", "").lower()
                title_lower = result.get("title", "").lower()

                # Check if this is an alert
                if any(keyword in content_lower or keyword in title_lower for keyword in alert_keywords):
                    alerts["alerts_found"] = True
                    alerts["warnings"].append({
                        "title": result.get("title"),
                        "source": result.get("url"),
                        "snippet": result.get("content", "")[:300],
                        "severity": "HIGH"  # Could be determined by AI analysis
                    })

            return alerts

        except Exception as e:
            print(f"Counterfeit check error: {e}")
            return {"alerts_found": False, "error": str(e)}

    def get_medicine_details(self, product_name: str) -> Dict[str, Any]:
        """
        Get comprehensive medicine details using AI

        Args:
            product_name: Medicine name

        Returns:
            Detailed information
        """
        if not self.enabled:
            return {"found": False, "reason": "Tavily API not configured"}

        try:
            query = f"{product_name} medicine composition uses dosage manufacturer India"

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )

            details = {
                "found": len(response.get("results", [])) > 0,
                "product_name": product_name,
                "summary": response.get("answer", ""),
                "composition": None,
                "manufacturer": None,
                "therapeutic_use": None,
                "sources": []
            }

            # Try to extract structured information from AI answer
            answer = response.get("answer", "").lower()

            # Extract manufacturer if mentioned
            if "manufacturer" in answer or "manufactured by" in answer:
                # Simple extraction - could be enhanced with NLP
                words = answer.split()
                if "by" in words:
                    idx = words.index("by")
                    if idx + 1 < len(words):
                        details["manufacturer"] = words[idx + 1].title()

            for result in response.get("results", []):
                details["sources"].append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "relevance_score": result.get("score", 0)
                })

            return details

        except Exception as e:
            print(f"Medicine details error: {e}")
            return {"found": False, "error": str(e)}


# Singleton instance
_tavily_service = None


def get_tavily_service() -> TavilySearchService:
    """Get singleton Tavily service instance"""
    global _tavily_service
    if _tavily_service is None:
        _tavily_service = TavilySearchService()
    return _tavily_service


if __name__ == "__main__":
    # Test
    service = TavilySearchService()
    if service.enabled:
        result = service.search_medicine_info("Dolo 650", "Micro Labs")
        print(f"Search result: {result}")
    else:
        print("Set TAVILY_API_KEY environment variable to test")
