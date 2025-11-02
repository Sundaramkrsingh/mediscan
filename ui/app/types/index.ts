// Type definitions for MediScan v2

export interface RiskFactor {
  type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  message: string;
}

export interface VerificationDetails {
  expiry_check: {
    is_expired: boolean;
    expiry_date?: string;
    days_until_expiry?: number;
    status: string;
  };
  gtin_check: {
    verified: boolean;
    gtin?: string;
    company?: string;
    country?: string;
  };
  product_consistency: {
    consistent: boolean;
    issues: string[];
  };
  batch_validity: {
    valid: boolean;
    batch_number?: string;
    issues: string[];
  };
  regulatory_warnings: {
    has_warnings: boolean;
    warnings: string[];
    count: number;
  };
  packaging_issues: {
    has_issues: boolean;
    issues: string[];
  };
}

export interface VerificationResponse {
  status: "AUTHENTIC" | "SUSPICIOUS" | "COUNTERFEIT" | "EXPIRED" | "UNVERIFIED";
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  is_expired: boolean;
  expiry_date: string | null;
  gtin: string | null;
  gtin_verified: boolean;
  product_name: string | null;
  batch_number: string | null;
  manufacturer: string | null;
  country: string | null;
  risk_factors: RiskFactor[];
  recommendations: string[];
  details: VerificationDetails;
  raw_data: {
    barcodes: {
      type?: string;
      data?: string;
      [key: string]: unknown;
    }[];
    ocr_texts: {
      quality_score?: number;
      text?: string;
      [key: string]: unknown;
    }[];
    gs1_verification: {
      found?: boolean;
      country?: string;
      [key: string]: unknown;
    } | null;
    cdsco_verification: {
      found?: boolean;
      warnings?: string[];
      [key: string]: unknown;
    } | null;
  };
}

export interface UploadedImage {
  file: File;
  preview: string;
  type: "branding" | "label" | "barcode" | "general";
}
