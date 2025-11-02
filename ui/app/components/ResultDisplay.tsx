"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ShieldCheck,
  ShieldAlert,
  ShieldX,
  AlertTriangle,
  HelpCircle,
  Calendar,
  Package,
  Building2,
  Globe,
  Barcode,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  CheckCircle2,
  XCircle,
  Info,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import { VerificationResponse } from "../types";

interface ResultDisplayProps {
  result: VerificationResponse;
}

export default function ResultDisplay({ result }: ResultDisplayProps) {
  const [showDetails, setShowDetails] = useState(false);

  const getStatusConfig = (status: string) => {
    switch (status) {
      case "AUTHENTIC":
        return {
          gradient: "from-green-500 to-emerald-600",
          bg: "bg-green-50",
          border: "border-green-500",
          text: "text-green-900",
          icon: ShieldCheck,
          label: "Medicine Authentic",
          message: "This medicine appears to be genuine and safe to use.",
        };
      case "EXPIRED":
        return {
          gradient: "from-red-500 to-rose-600",
          bg: "bg-red-50",
          border: "border-red-500",
          text: "text-red-900",
          icon: Calendar,
          label: "Medicine Expired",
          message: "This medicine has passed its expiry date. Do not use.",
        };
      case "COUNTERFEIT":
        return {
          gradient: "from-red-600 to-pink-700",
          bg: "bg-red-50",
          border: "border-red-600",
          text: "text-red-900",
          icon: ShieldX,
          label: "Counterfeit Detected",
          message: "Warning! This medicine may be counterfeit. Do not use.",
        };
      case "SUSPICIOUS":
        return {
          gradient: "from-orange-500 to-amber-600",
          bg: "bg-orange-50",
          border: "border-orange-500",
          text: "text-orange-900",
          icon: ShieldAlert,
          label: "Suspicious Medicine",
          message: "Some verification checks failed. Consult a pharmacist.",
        };
      default:
        return {
          gradient: "from-gray-500 to-slate-600",
          bg: "bg-gray-50",
          border: "border-gray-500",
          text: "text-gray-900",
          icon: HelpCircle,
          label: "Unverified",
          message: "Unable to fully verify this medicine.",
        };
    }
  };

  const getRiskConfig = (risk: string) => {
    switch (risk) {
      case "LOW":
        return { color: "text-green-600", bg: "bg-green-100", value: 25 };
      case "MEDIUM":
        return { color: "text-yellow-600", bg: "bg-yellow-100", value: 50 };
      case "HIGH":
        return { color: "text-orange-600", bg: "bg-orange-100", value: 75 };
      case "CRITICAL":
        return { color: "text-red-600", bg: "bg-red-100", value: 100 };
      default:
        return { color: "text-gray-600", bg: "bg-gray-100", value: 0 };
    }
  };

  const statusConfig = getStatusConfig(result.status);
  const riskConfig = getRiskConfig(result.risk_level);
  const StatusIcon = statusConfig.icon;

  // Prepare verification scores data
  const verificationScores = [
    {
      name: "Expiry",
      score: result.details?.expiry_check?.found ? 100 : 0,
    },
    {
      name: "GTIN",
      score: result.gtin_verified ? 100 : 0,
    },
    {
      name: "Barcode",
      score: result.raw_data?.barcodes?.length > 0 ? 100 : 50,
    },
    {
      name: "OCR",
      score: result.raw_data?.ocr_texts?.[0]?.quality_score || 0,
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="space-y-6"
    >
      {/* Main Status Card with Animation */}
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className={`relative rounded-3xl p-8 border-4 ${statusConfig.border} ${statusConfig.bg} overflow-hidden shadow-2xl`}
      >
        {/* Animated background gradient */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${statusConfig.gradient} opacity-5`}
        />

        {/* Floating particles effect */}
        <motion.div
          className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <div className="relative z-10">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="flex items-start gap-6">
              {/* Animated Icon */}
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{
                  type: "spring",
                  stiffness: 200,
                  damping: 15,
                  delay: 0.3,
                }}
                className={`w-20 h-20 bg-gradient-to-br ${statusConfig.gradient} rounded-2xl flex items-center justify-center shadow-lg`}
              >
                <StatusIcon className="w-12 h-12 text-white" />
              </motion.div>

              <div>
                <motion.h2
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                  className={`text-4xl font-bold ${statusConfig.text} mb-2`}
                >
                  {statusConfig.label}
                </motion.h2>
                <motion.p
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 }}
                  className={`text-lg ${statusConfig.text} opacity-80`}
                >
                  {statusConfig.message}
                </motion.p>
              </div>
            </div>

            {/* Risk Level Badge */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", delay: 0.6 }}
              className={`${riskConfig.bg} ${riskConfig.color} px-6 py-4 rounded-2xl shadow-lg`}
            >
              <p className="text-sm font-medium opacity-80">Risk Level</p>
              <p className="text-3xl font-bold mt-1">{result.risk_level}</p>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Quick Summary Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        {/* Expiry Status */}
        <div className={`glass rounded-xl p-4 border-2 ${result.is_expired ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'}`}>
          <div className="flex items-center gap-2 mb-2">
            <Calendar className={`w-5 h-5 ${result.is_expired ? 'text-red-600' : 'text-green-600'}`} />
            <span className="text-xs font-medium text-gray-700">Expiry</span>
          </div>
          <p className={`text-lg font-bold ${result.is_expired ? 'text-red-900' : 'text-green-900'}`}>
            {result.is_expired ? 'Expired' : 'Valid'}
          </p>
        </div>

        {/* Barcode Status */}
        <div className={`glass rounded-xl p-4 border-2 ${result.gtin ? 'border-blue-300 bg-blue-50' : 'border-gray-300 bg-gray-50'}`}>
          <div className="flex items-center gap-2 mb-2">
            <Barcode className={`w-5 h-5 ${result.gtin ? 'text-blue-600' : 'text-gray-600'}`} />
            <span className="text-xs font-medium text-gray-700">Barcode</span>
          </div>
          <p className={`text-lg font-bold ${result.gtin ? 'text-blue-900' : 'text-gray-900'}`}>
            {result.gtin ? 'Found' : 'Not Found'}
          </p>
        </div>

        {/* Verification Status */}
        <div className={`glass rounded-xl p-4 border-2 ${result.gtin_verified ? 'border-green-300 bg-green-50' : 'border-orange-300 bg-orange-50'}`}>
          <div className="flex items-center gap-2 mb-2">
            <ShieldCheck className={`w-5 h-5 ${result.gtin_verified ? 'text-green-600' : 'text-orange-600'}`} />
            <span className="text-xs font-medium text-gray-700">Verified</span>
          </div>
          <p className={`text-lg font-bold ${result.gtin_verified ? 'text-green-900' : 'text-orange-900'}`}>
            {result.gtin_verified ? 'Yes' : 'Partial'}
          </p>
        </div>

        {/* Manufacturer */}
        <div className="glass rounded-xl p-4 border-2 border-purple-300 bg-purple-50">
          <div className="flex items-center gap-2 mb-2">
            <Building2 className="w-5 h-5 text-purple-600" />
            <span className="text-xs font-medium text-gray-700">Origin</span>
          </div>
          <p className="text-lg font-bold text-purple-900 truncate">
            {result.country || 'Unknown'}
          </p>
        </div>
      </motion.div>

      {/* Safety Score & Analytics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid md:grid-cols-3 gap-6"
      >
        {/* Overall Safety Score */}
        <div className="glass rounded-2xl p-6 shadow-xl border border-white">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            Safety Score
          </h3>
          <div className="flex flex-col items-center justify-center">
            <div className="relative w-32 h-32">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="#e5e7eb"
                  strokeWidth="12"
                  fill="none"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke={riskConfig.value < 30 ? "#10b981" : riskConfig.value < 60 ? "#f59e0b" : "#ef4444"}
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${(100 - riskConfig.value) * 3.51} 351`}
                  className="transition-all duration-1000"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold text-gray-900">{100 - riskConfig.value}</span>
                <span className="text-xs text-gray-600">out of 100</span>
              </div>
            </div>
            <div className="mt-4 text-center">
              <p className={`text-lg font-bold ${riskConfig.color}`}>
                {result.risk_level === "LOW" ? "Very Safe" :
                 result.risk_level === "MEDIUM" ? "Mostly Safe" :
                 result.risk_level === "HIGH" ? "Caution Advised" : "High Risk"}
              </p>
            </div>
          </div>
        </div>

        {/* Verification Status */}
        <div className="glass rounded-2xl p-6 shadow-xl border border-white md:col-span-2">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-600" />
            Verification Status
          </h3>
          <div className="space-y-3">
            {verificationScores.map((item, idx) => (
              <div key={idx} className="flex items-center gap-3">
                <div className="flex-1">
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">{item.name}</span>
                    <span className="text-sm font-bold text-gray-900">{item.score}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${item.score}%` }}
                      transition={{ duration: 1, delay: 0.3 + idx * 0.1 }}
                      className={`h-full ${
                        item.score === 100 ? 'bg-green-500' :
                        item.score >= 70 ? 'bg-blue-500' :
                        item.score >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                    />
                  </div>
                </div>
                {item.score === 100 && (
                  <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0" />
                )}
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Medicine Information Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="glass rounded-2xl shadow-xl border border-white p-6"
      >
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Package className="w-6 h-6 text-blue-600" />
          Medicine Information
        </h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {result.product_name && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              className="p-4 bg-blue-50/50 rounded-xl border border-blue-200"
            >
              <p className="text-sm text-blue-600 font-medium mb-1 flex items-center gap-2">
                <Package className="w-4 h-4" />
                Product Name
              </p>
              <p className="text-lg font-bold text-gray-900">
                {result.product_name}
              </p>
            </motion.div>
          )}
          {result.manufacturer && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.55 }}
              className="p-4 bg-purple-50/50 rounded-xl border border-purple-200"
            >
              <p className="text-sm text-purple-600 font-medium mb-1 flex items-center gap-2">
                <Building2 className="w-4 h-4" />
                Manufacturer
              </p>
              <p className="text-lg font-bold text-gray-900">
                {result.manufacturer}
              </p>
            </motion.div>
          )}
          {result.expiry_date && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 }}
              className={`p-4 rounded-xl border ${
                result.is_expired
                  ? "bg-red-50/50 border-red-200"
                  : "bg-green-50/50 border-green-200"
              }`}
            >
              <p
                className={`text-sm font-medium mb-1 flex items-center gap-2 ${
                  result.is_expired ? "text-red-600" : "text-green-600"
                }`}
              >
                <Calendar className="w-4 h-4" />
                Expiry Date
              </p>
              <p
                className={`text-lg font-bold ${
                  result.is_expired ? "text-red-900" : "text-gray-900"
                }`}
              >
                {new Date(result.expiry_date).toLocaleDateString("en-IN", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
                {result.is_expired && (
                  <span className="ml-2 text-sm font-normal">(EXPIRED)</span>
                )}
              </p>
            </motion.div>
          )}
          {result.batch_number && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.65 }}
              className="p-4 bg-indigo-50/50 rounded-xl border border-indigo-200"
            >
              <p className="text-sm text-indigo-600 font-medium mb-1 flex items-center gap-2">
                <Package className="w-4 h-4" />
                Batch Number
              </p>
              <p className="text-lg font-bold text-gray-900 font-mono">
                {result.batch_number}
              </p>
            </motion.div>
          )}
          {result.gtin && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.7 }}
              className="p-4 bg-teal-50/50 rounded-xl border border-teal-200"
            >
              <p className="text-sm text-teal-600 font-medium mb-1 flex items-center gap-2">
                <Barcode className="w-4 h-4" />
                GTIN/Barcode
              </p>
              <p className="text-lg font-bold text-gray-900 font-mono flex items-center gap-2">
                {result.gtin}
                {result.gtin_verified && (
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                )}
              </p>
            </motion.div>
          )}
          {result.country && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.75 }}
              className="p-4 bg-amber-50/50 rounded-xl border border-amber-200"
            >
              <p className="text-sm text-amber-600 font-medium mb-1 flex items-center gap-2">
                <Globe className="w-4 h-4" />
                Country
              </p>
              <p className="text-lg font-bold text-gray-900">{result.country}</p>
            </motion.div>
          )}
        </div>
      </motion.div>

      {/* How We Checked */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.45 }}
        className="glass rounded-2xl shadow-xl border border-white p-6"
      >
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-purple-600" />
          How We Verified Your Medicine
        </h3>
        <div className="space-y-4">
          {/* Step 1: Scanned Package */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="flex items-start gap-4 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border border-blue-200"
          >
            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${result.gtin ? 'bg-green-500' : 'bg-gray-400'}`}>
              {result.gtin ? (
                <CheckCircle2 className="w-6 h-6 text-white" />
              ) : (
                <XCircle className="w-6 h-6 text-white" />
              )}
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 text-lg mb-1">📦 Scanned Package Barcode</h4>
              <p className="text-gray-700 text-sm mb-2">
                {result.gtin
                  ? `Found unique product code on your medicine package`
                  : "Could not find a barcode on the packaging - try taking a clearer photo"}
              </p>
              {result.gtin && (
                <div className="mt-2 p-2 bg-white rounded border border-blue-200">
                  <p className="text-xs text-gray-600">Product Code: <span className="font-mono font-bold text-gray-900">{result.gtin}</span></p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Step 2: Checked Authenticity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.55 }}
            className="flex items-start gap-4 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200"
          >
            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${result.gtin_verified ? 'bg-green-500' : 'bg-gray-400'}`}>
              {result.gtin_verified ? (
                <CheckCircle2 className="w-6 h-6 text-white" />
              ) : (
                <XCircle className="w-6 h-6 text-white" />
              )}
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 text-lg mb-1">🔍 Checked Product Code Authenticity</h4>
              <p className="text-gray-700 text-sm mb-2">
                {result.gtin_verified
                  ? "Product code is valid and follows international standards"
                  : "Product code structure appears invalid - this could be a counterfeit"}
              </p>
              {result.raw_data?.gs1_verification?.found && result.raw_data.gs1_verification.country && (
                <div className="mt-2 p-2 bg-white rounded border border-green-200">
                  <p className="text-xs text-gray-600">
                    Manufacturing Country: <span className="font-bold text-gray-900">{result.raw_data.gs1_verification.country}</span>
                  </p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Step 3: Verified with Authorities */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="flex items-start gap-4 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-200"
          >
            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${result.raw_data?.cdsco_verification?.found ? 'bg-green-500' : 'bg-blue-500'}`}>
              {result.raw_data?.cdsco_verification?.found ? (
                <CheckCircle2 className="w-6 h-6 text-white" />
              ) : (
                <Sparkles className="w-6 h-6 text-white" />
              )}
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 text-lg mb-1">🏛️ Cross-Checked with Health Authorities</h4>
              <p className="text-gray-700 text-sm mb-2">
                Verified your medicine against government health databases and official registries
              </p>
              {result.raw_data?.cdsco_verification?.warnings && result.raw_data.cdsco_verification.warnings.length > 0 && (
                <div className="mt-2 p-3 bg-red-50 rounded-lg border border-red-300">
                  <p className="font-bold text-red-700 text-sm flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" />
                    Safety Alerts Found
                  </p>
                  {result.raw_data.cdsco_verification.warnings.map((warning: string, idx: number) => (
                    <p key={idx} className="text-red-600 text-xs mt-1">• {warning}</p>
                  ))}
                </div>
              )}
              {!result.raw_data?.cdsco_verification?.warnings && (
                <div className="mt-2 p-2 bg-white rounded border border-purple-200">
                  <p className="text-xs text-green-700 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    No safety alerts or recalls found for this medicine
                  </p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Step 4: Read Package Label */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.65 }}
            className="flex items-start gap-4 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl border border-amber-200"
          >
            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${result.expiry_date ? 'bg-green-500' : 'bg-orange-400'}`}>
              {result.expiry_date ? (
                <CheckCircle2 className="w-6 h-6 text-white" />
              ) : (
                <Calendar className="w-6 h-6 text-white" />
              )}
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 text-lg mb-1">📅 Read Package Label & Expiry Date</h4>
              <p className="text-gray-700 text-sm mb-2">
                {result.expiry_date
                  ? "Found and verified the expiry date printed on your medicine"
                  : "Couldn't read expiry date clearly - please take a sharper photo of the label"}
              </p>
              <div className="mt-2 space-y-2">
                {result.expiry_date && (
                  <div className="p-3 bg-white rounded-lg border border-amber-300">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-semibold text-gray-700">Expiry Date:</span>
                      <span className="text-lg font-bold text-gray-900">
                        {new Date(result.expiry_date).toLocaleDateString("en-IN", {
                          day: "numeric",
                          month: "short",
                          year: "numeric"
                        })}
                      </span>
                    </div>
                    {result.is_expired ? (
                      <div className="p-2 bg-red-50 rounded border border-red-200">
                        <p className="text-xs text-red-700 font-semibold">⚠️ This medicine has expired - do not use</p>
                      </div>
                    ) : (
                      <div className="p-2 bg-green-50 rounded border border-green-200">
                        <p className="text-xs text-green-700 font-semibold">✓ Medicine is still within validity period</p>
                      </div>
                    )}
                  </div>
                )}
                {result.batch_number && (
                  <div className="p-2 bg-white rounded border border-amber-200">
                    <p className="text-xs text-gray-600">
                      Batch Number: <span className="font-mono font-bold text-gray-900">{result.batch_number}</span>
                    </p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>

          {/* Step 5: AI Smart Verification */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7 }}
            className="flex items-start gap-4 p-4 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl border border-indigo-200"
          >
            <div className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 bg-indigo-500">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 text-lg mb-1">🤖 AI-Powered Smart Verification</h4>
              <p className="text-gray-700 text-sm mb-2">
                Our AI searched multiple official health & drug regulatory websites to confirm authenticity
              </p>
              <div className="mt-2 space-y-2">
                <div className="p-3 bg-white rounded-lg border border-indigo-300">
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                      <span className="text-gray-700">Drug Regulatory Authority</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                      <span className="text-gray-700">International Databases</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                      <span className="text-gray-700">Ministry of Health</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />
                      <span className="text-gray-700">Safety Alerts Database</span>
                    </div>
                  </div>
                </div>
                <div className="p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-300">
                  <p className="text-sm font-semibold text-green-800 flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Comprehensive verification complete
                  </p>
                  <p className="text-xs text-green-700 mt-1">
                    All available information has been cross-checked across official sources
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Risk Factors */}
      <AnimatePresence>
        {result.risk_factors && result.risk_factors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ delay: 0.5 }}
            className="glass rounded-2xl shadow-xl border border-red-200 p-6"
          >
            <h3 className="text-2xl font-bold text-red-900 mb-6 flex items-center gap-2">
              <AlertCircle className="w-6 h-6" />
              Risk Factors Detected
            </h3>
            <div className="space-y-3">
              {result.risk_factors.map((factor, index) => {
                const severityConfig = {
                  CRITICAL: {
                    bg: "bg-red-50",
                    border: "border-red-500",
                    icon: XCircle,
                    badge: "bg-red-200 text-red-900",
                  },
                  HIGH: {
                    bg: "bg-orange-50",
                    border: "border-orange-500",
                    icon: AlertTriangle,
                    badge: "bg-orange-200 text-orange-900",
                  },
                  MEDIUM: {
                    bg: "bg-yellow-50",
                    border: "border-yellow-500",
                    icon: AlertCircle,
                    badge: "bg-yellow-200 text-yellow-900",
                  },
                  LOW: {
                    bg: "bg-blue-50",
                    border: "border-blue-500",
                    icon: Info,
                    badge: "bg-blue-200 text-blue-900",
                  },
                };

                const config =
                  severityConfig[factor.severity as keyof typeof severityConfig] ||
                  severityConfig.LOW;
                const FactorIcon = config.icon;

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    className={`p-5 rounded-xl border-l-4 ${config.bg} ${config.border} shadow-md`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3 flex-1">
                        <FactorIcon className="w-5 h-5 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="font-bold text-gray-900 text-lg">
                            {factor.type.replace(/_/g, " ")}
                          </p>
                          <p className="text-sm text-gray-700 mt-1">
                            {factor.message}
                          </p>
                        </div>
                      </div>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold ${config.badge} whitespace-nowrap`}
                      >
                        {factor.severity}
                      </span>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* What Should You Do? */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="glass rounded-2xl border-2 border-blue-300 p-6 shadow-xl bg-gradient-to-br from-blue-50 to-cyan-50"
      >
        <h3 className="text-2xl font-bold text-blue-900 mb-2 flex items-center gap-2">
          <Info className="w-7 h-7" />
          What Should You Do?
        </h3>
        <p className="text-sm text-blue-700 mb-6">Based on our verification, here are our recommendations</p>
        <div className="space-y-3">
          {result.recommendations.map((rec, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 + index * 0.1 }}
              className="flex items-start gap-4 p-4 bg-white rounded-xl border-2 border-blue-200 hover:border-blue-300 transition-colors shadow-sm"
            >
              <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-sm">{index + 1}</span>
              </div>
              <p className="text-gray-800 font-medium flex-1">{rec}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Technical Details (Collapsible) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="glass rounded-2xl shadow-xl border border-gray-300"
      >
        <motion.button
          onClick={() => setShowDetails(!showDetails)}
          whileHover={{ backgroundColor: "rgba(0, 0, 0, 0.02)" }}
          whileTap={{ scale: 0.98 }}
          className="w-full p-6 flex items-center justify-between transition-colors rounded-t-2xl"
        >
          <div>
            <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
              <Info className="w-5 h-5 text-gray-600" />
              Advanced Technical Details
            </h3>
            <p className="text-xs text-gray-600 mt-1">For developers and technical users</p>
          </div>
          <motion.div
            animate={{ rotate: showDetails ? 180 : 0 }}
            transition={{ duration: 0.3 }}
          >
            <ChevronDown className="w-6 h-6 text-gray-600" />
          </motion.div>
        </motion.button>

        <AnimatePresence>
          {showDetails && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="p-6 pt-0 space-y-4 border-t">
                {/* Expiry Check */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200"
                >
                  <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-blue-600" />
                    Expiry Check
                  </h4>
                  <pre className="text-xs text-gray-700 overflow-auto bg-white p-3 rounded-lg border">
                    {JSON.stringify(result.details.expiry_check, null, 2)}
                  </pre>
                </motion.div>

                {/* GTIN Check */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200"
                >
                  <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <Barcode className="w-5 h-5 text-green-600" />
                    GTIN Verification
                  </h4>
                  <pre className="text-xs text-gray-700 overflow-auto bg-white p-3 rounded-lg border">
                    {JSON.stringify(result.details.gtin_check, null, 2)}
                  </pre>
                </motion.div>

                {/* Barcodes Detected */}
                {result.raw_data.barcodes && result.raw_data.barcodes.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="p-4 bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl border border-teal-200"
                  >
                    <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                      <Barcode className="w-5 h-5 text-teal-600" />
                      Barcodes Detected ({result.raw_data.barcodes.length})
                    </h4>
                    <div className="space-y-2">
                      {result.raw_data.barcodes.map((barcode, idx) => (
                        <div
                          key={idx}
                          className="p-3 bg-white rounded-lg border text-sm"
                        >
                          <p className="font-mono text-gray-800 font-semibold">
                            Type: <span className="text-teal-600">{barcode.type}</span>
                          </p>
                          <p className="font-mono text-gray-600 mt-1">
                            Data: {barcode.data}
                          </p>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}

                {/* OCR Quality */}
                {result.raw_data.ocr_texts && result.raw_data.ocr_texts.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-200"
                  >
                    <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-purple-600" />
                      OCR Quality Scores
                    </h4>
                    <div className="space-y-2">
                      {result.raw_data.ocr_texts.map((ocr, idx) => (
                        <div
                          key={idx}
                          className="flex justify-between items-center p-3 bg-white rounded-lg border"
                        >
                          <span className="text-sm font-medium text-gray-700">
                            Image {idx + 1}
                          </span>
                          <div className="flex items-center gap-3">
                            <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{
                                  width: `${ocr.quality_score}%`,
                                }}
                                transition={{ duration: 1, delay: 0.5 + idx * 0.1 }}
                                className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                              />
                            </div>
                            <span className="text-sm font-bold text-gray-900 w-12 text-right">
                              {ocr.quality_score.toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}