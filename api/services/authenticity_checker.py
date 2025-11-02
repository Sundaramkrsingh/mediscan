"""
Medicine Authenticity Checker
Analyzes multiple data points to detect counterfeit medicines
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
from enum import Enum


class AuthenticityStatus(Enum):
    """Status levels for medicine authenticity"""
    AUTHENTIC = "AUTHENTIC"
    SUSPICIOUS = "SUSPICIOUS"
    COUNTERFEIT = "COUNTERFEIT"
    EXPIRED = "EXPIRED"
    UNVERIFIED = "UNVERIFIED"


class RiskLevel(Enum):
    """Risk levels for detected issues"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AuthenticityChecker:
    """
    Checks medicine authenticity by cross-referencing multiple data sources
    and detecting inconsistencies
    """

    def __init__(self):
        self.risk_factors = []

    def verify_medicine(
        self,
        gtin: Optional[str],
        expiry_date: Optional[date],
        batch_number: Optional[str],
        product_name: Optional[str],
        gs1_data: Optional[Dict],
        cdsco_data: Optional[Dict],
        ocr_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Comprehensive authenticity verification

        Args:
            gtin: GTIN/barcode from package
            expiry_date: Expiry date (from OCR or barcode)
            batch_number: Batch number
            product_name: Product name from OCR
            gs1_data: Data from GS1 verification
            cdsco_data: Data from CDSCO verification
            ocr_data: All OCR extracted data

        Returns:
            Verification result with status and risk factors
        """
        self.risk_factors = []

        # 1. Check expiry status
        expiry_status = self._check_expiry(expiry_date)

        # 2. Verify GTIN authenticity
        gtin_status = self._verify_gtin(gtin, gs1_data)

        # 3. Cross-verify product information
        product_consistency = self._verify_product_consistency(
            gtin, product_name, gs1_data, cdsco_data
        )

        # 4. Check batch and manufacturing dates
        batch_validity = self._verify_batch_dates(
            batch_number, expiry_date, ocr_data
        )

        # 5. Check regulatory warnings
        regulatory_issues = self._check_regulatory_warnings(
            product_name, gtin, cdsco_data
        )

        # 6. Detect packaging inconsistencies
        packaging_issues = self._detect_packaging_issues(ocr_data, gs1_data)

        # Calculate overall risk level
        risk_level = self._calculate_risk_level()

        # Determine final status
        status = self._determine_status(
            expiry_status, gtin_status, product_consistency,
            batch_validity, regulatory_issues
        )

        return {
            "status": status.value,
            "risk_level": risk_level.value,
            "is_expired": expiry_status["is_expired"],
            "expiry_date": expiry_date.isoformat() if expiry_date else None,
            "gtin_verified": gtin_status["verified"],
            "risk_factors": self.risk_factors,
            "recommendations": self._generate_recommendations(status, risk_level),
            "details": {
                "expiry_check": expiry_status,
                "gtin_check": gtin_status,
                "product_consistency": product_consistency,
                "batch_validity": batch_validity,
                "regulatory_warnings": regulatory_issues,
                "packaging_issues": packaging_issues
            }
        }

    def _check_expiry(self, expiry_date: Optional[date]) -> Dict[str, Any]:
        """Check if medicine is expired"""
        if not expiry_date:
            return {
                "is_expired": False,
                "status": "unknown",
                "note": "No expiry date found"
            }

        today = date.today()
        days_until_expiry = (expiry_date - today).days

        is_expired = expiry_date < today

        if is_expired:
            self.risk_factors.append({
                "type": "EXPIRED",
                "severity": "CRITICAL",
                "message": f"Medicine expired on {expiry_date.isoformat()}"
            })

        elif days_until_expiry < 30:
            self.risk_factors.append({
                "type": "NEAR_EXPIRY",
                "severity": "MEDIUM",
                "message": f"Medicine expires in {days_until_expiry} days"
            })

        return {
            "is_expired": is_expired,
            "expiry_date": expiry_date.isoformat(),
            "days_until_expiry": days_until_expiry if not is_expired else None,
            "status": "expired" if is_expired else "valid"
        }

    def _verify_gtin(self, gtin: Optional[str], gs1_data: Optional[Dict]) -> Dict[str, Any]:
        """Verify GTIN against GS1 database"""
        if not gtin:
            return {"verified": False, "reason": "No GTIN found"}

        if not gs1_data or not gs1_data.get("found"):
            self.risk_factors.append({
                "type": "GTIN_NOT_VERIFIED",
                "severity": "HIGH",
                "message": "GTIN not found in GS1 database"
            })
            return {
                "verified": False,
                "reason": "GTIN not found in database",
                "gtin": gtin
            }

        # GTIN found in database
        return {
            "verified": True,
            "gtin": gtin,
            "company": gs1_data.get("company_name"),
            "country": gs1_data.get("country")
        }

    def _verify_product_consistency(
        self,
        gtin: Optional[str],
        product_name: Optional[str],
        gs1_data: Optional[Dict],
        cdsco_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Check consistency between different data sources"""
        issues = []

        # Check if product name matches across sources
        if product_name and gs1_data and gs1_data.get("product_name"):
            if not self._fuzzy_match(product_name, gs1_data["product_name"]):
                issues.append("Product name mismatch between package and GS1 database")
                self.risk_factors.append({
                    "type": "NAME_MISMATCH",
                    "severity": "HIGH",
                    "message": "Product name doesn't match registered name"
                })

        # Check manufacturer consistency
        if gs1_data and cdsco_data:
            gs1_company = (gs1_data.get("company_name") or "").lower()
            cdsco_company = (cdsco_data.get("manufacturer") or "").lower()

            if gs1_company and cdsco_company and gs1_company != cdsco_company:
                if not self._fuzzy_match(gs1_company, cdsco_company):
                    issues.append("Manufacturer mismatch between GS1 and CDSCO")
                    self.risk_factors.append({
                        "type": "MANUFACTURER_MISMATCH",
                        "severity": "CRITICAL",
                        "message": "Different manufacturers in databases"
                    })

        return {
            "consistent": len(issues) == 0,
            "issues": issues
        }

    def _verify_batch_dates(
        self,
        batch_number: Optional[str],
        expiry_date: Optional[date],
        ocr_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Verify batch number and date consistency"""
        issues = []

        if not batch_number:
            return {"valid": True, "note": "No batch number found"}

        # Check manufacturing date vs expiry date
        if ocr_data and ocr_data.get("manufacturing_date"):
            mfg_date = ocr_data["manufacturing_date"]["date"]

            if expiry_date and mfg_date:
                # Typically medicines have 2-5 year shelf life
                shelf_life_days = (expiry_date - mfg_date).days

                if shelf_life_days < 0:
                    issues.append("Expiry date before manufacturing date")
                    self.risk_factors.append({
                        "type": "INVALID_DATES",
                        "severity": "CRITICAL",
                        "message": "Expiry date is before manufacturing date"
                    })
                elif shelf_life_days > 3650:  # More than 10 years
                    issues.append("Unusually long shelf life")
                    self.risk_factors.append({
                        "type": "SUSPICIOUS_SHELF_LIFE",
                        "severity": "MEDIUM",
                        "message": f"Shelf life of {shelf_life_days // 365} years is unusual"
                    })

        return {
            "valid": len(issues) == 0,
            "batch_number": batch_number,
            "issues": issues
        }

    def _check_regulatory_warnings(
        self,
        product_name: Optional[str],
        gtin: Optional[str],
        cdsco_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Check for regulatory warnings or counterfeit alerts"""
        warnings = []

        if cdsco_data and cdsco_data.get("warnings"):
            warnings.extend(cdsco_data["warnings"])

            for warning in cdsco_data["warnings"]:
                self.risk_factors.append({
                    "type": "REGULATORY_WARNING",
                    "severity": "CRITICAL",
                    "message": f"CDSCO Alert: {warning.get('type', 'Warning found')}"
                })

        return {
            "has_warnings": len(warnings) > 0,
            "warnings": warnings,
            "count": len(warnings)
        }

    def _detect_packaging_issues(
        self,
        ocr_data: Optional[Dict],
        gs1_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Detect potential packaging inconsistencies"""
        issues = []

        # Check for poor quality OCR (might indicate fake/poor quality packaging)
        if ocr_data and ocr_data.get("all_texts"):
            avg_quality = sum(t["quality"]["quality_score"] for t in ocr_data["all_texts"]) / len(ocr_data["all_texts"])

            if avg_quality < 30:
                issues.append("Poor packaging quality detected")
                self.risk_factors.append({
                    "type": "POOR_PACKAGING_QUALITY",
                    "severity": "MEDIUM",
                    "message": "Packaging quality is below standard"
                })

        # Check for missing required information
        required_fields = ["expiry_date", "batch_number"]
        missing = []

        if ocr_data:
            if not ocr_data.get("expiry_date"):
                missing.append("expiry date")
            if not ocr_data.get("batch_number"):
                missing.append("batch number")

        if missing:
            issues.append(f"Missing required information: {', '.join(missing)}")
            self.risk_factors.append({
                "type": "MISSING_INFO",
                "severity": "HIGH",
                "message": f"Missing: {', '.join(missing)}"
            })

        return {
            "has_issues": len(issues) > 0,
            "issues": issues
        }

    def _calculate_risk_level(self) -> RiskLevel:
        """Calculate overall risk level based on risk factors"""
        if not self.risk_factors:
            return RiskLevel.LOW

        critical_count = sum(1 for rf in self.risk_factors if rf["severity"] == "CRITICAL")
        high_count = sum(1 for rf in self.risk_factors if rf["severity"] == "HIGH")

        if critical_count > 0:
            return RiskLevel.CRITICAL
        elif high_count >= 2:
            return RiskLevel.CRITICAL
        elif high_count == 1:
            return RiskLevel.HIGH
        elif len(self.risk_factors) >= 3:
            return RiskLevel.HIGH
        elif len(self.risk_factors) >= 1:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _determine_status(
        self,
        expiry_status: Dict,
        gtin_status: Dict,
        product_consistency: Dict,
        batch_validity: Dict,
        regulatory_issues: Dict
    ) -> AuthenticityStatus:
        """Determine overall authenticity status"""

        # Expired takes precedence
        if expiry_status["is_expired"]:
            return AuthenticityStatus.EXPIRED

        # Critical regulatory warnings
        if regulatory_issues["has_warnings"]:
            return AuthenticityStatus.COUNTERFEIT

        # GTIN not verified + other issues
        if not gtin_status["verified"]:
            if not product_consistency["consistent"] or not batch_validity["valid"]:
                return AuthenticityStatus.COUNTERFEIT
            else:
                return AuthenticityStatus.SUSPICIOUS

        # Product inconsistencies
        if not product_consistency["consistent"]:
            return AuthenticityStatus.SUSPICIOUS

        # Batch issues
        if not batch_validity["valid"]:
            return AuthenticityStatus.SUSPICIOUS

        # GTIN verified and no major issues
        if gtin_status["verified"]:
            return AuthenticityStatus.AUTHENTIC

        return AuthenticityStatus.UNVERIFIED

    def _generate_recommendations(self, status: AuthenticityStatus, risk_level: RiskLevel) -> List[str]:
        """Generate user recommendations based on verification"""
        recommendations = []

        if status == AuthenticityStatus.EXPIRED:
            recommendations.append("⚠️ DO NOT USE - Medicine has expired")
            recommendations.append("Dispose of safely at a pharmacy or waste facility")

        elif status == AuthenticityStatus.COUNTERFEIT:
            recommendations.append("🚫 DO NOT USE - Suspected counterfeit medicine")
            recommendations.append("Report to local pharmacy authorities")
            recommendations.append("Contact the manufacturer directly to verify")

        elif status == AuthenticityStatus.SUSPICIOUS:
            recommendations.append("⚠️ CAUTION - Unable to fully verify authenticity")
            recommendations.append("Consult with a licensed pharmacist")
            recommendations.append("Check with the retailer or manufacturer")

        elif status == AuthenticityStatus.AUTHENTIC and risk_level == RiskLevel.LOW:
            recommendations.append("✓ Medicine appears authentic")
            recommendations.append("Always follow prescribed dosage")

        elif status == AuthenticityStatus.UNVERIFIED:
            recommendations.append("❓ Could not verify - Limited data available")
            recommendations.append("Purchase from licensed pharmacies only")

        recommendations.append("\n⚕️ Disclaimer: This tool is for informational purposes only. Always consult healthcare professionals.")

        return recommendations

    def _fuzzy_match(self, str1: str, str2: str, threshold: float = 0.7) -> bool:
        """Simple fuzzy string matching"""
        # Basic implementation - can be enhanced with libraries like fuzzywuzzy
        str1_clean = str1.lower().strip()
        str2_clean = str2.lower().strip()

        if str1_clean == str2_clean:
            return True

        # Check if one is substring of other
        if str1_clean in str2_clean or str2_clean in str1_clean:
            return True

        # Calculate simple similarity (common words)
        words1 = set(str1_clean.split())
        words2 = set(str2_clean.split())

        if not words1 or not words2:
            return False

        common = len(words1 & words2)
        total = len(words1 | words2)

        similarity = common / total if total > 0 else 0

        return similarity >= threshold


def verify_authenticity(
    gtin: Optional[str],
    expiry_date: Optional[date],
    batch_number: Optional[str],
    product_name: Optional[str],
    gs1_data: Optional[Dict],
    cdsco_data: Optional[Dict],
    ocr_data: Optional[Dict]
) -> Dict[str, Any]:
    """
    Main function to verify medicine authenticity

    Returns comprehensive verification results
    """
    checker = AuthenticityChecker()
    return checker.verify_medicine(
        gtin, expiry_date, batch_number, product_name,
        gs1_data, cdsco_data, ocr_data
    )


if __name__ == "__main__":
    print("Authenticity checker module loaded successfully")
