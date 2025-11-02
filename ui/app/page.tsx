"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Shield, Scan, CheckCircle, AlertTriangle, XCircle, Sparkles, Camera, Brain, FileCheck } from "lucide-react";
import { VerificationResponse, UploadedImage } from "./types";
import ImageUploader from "./components/ImageUploader";
import ResultDisplay from "./components/ResultDisplay";
import LoadingScreen from "./components/LoadingScreen";

export default function Home() {
  const [images, setImages] = useState<UploadedImage[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImagesSelected = (newImages: UploadedImage[]) => {
    setImages(newImages);
    setResult(null);
    setError(null);
  };

  const handleScan = async () => {
    if (images.length === 0) {
      setError("Please upload at least one image");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      images.forEach((img) => {
        formData.append("images", img.file);
      });

      const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
      const response = await fetch(`${apiBase}/verify`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Verification failed: ${response.statusText}`);
      }

      const data: VerificationResponse = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Scan error:", err);
      setError(err instanceof Error ? err.message : "Failed to verify medicine");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImages([]);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <div className="fixed inset-0 overflow-hidden pointer-events-none opacity-30">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      <motion.header
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative bg-white/80 backdrop-blur-lg shadow-sm border-b border-gray-200/50 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              className="flex items-center gap-3"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-green-500 rounded-xl flex items-center justify-center shadow-lg">
                  <Shield className="w-7 h-7 text-white" />
                </div>
                <motion.div
                  className="absolute -top-1 -right-1"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                >
                  <Sparkles className="w-4 h-4 text-yellow-500" />
                </motion.div>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">MediScan</h1>
                <p className="text-xs text-gray-500">AI-Powered Verification</p>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.header>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AnimatePresence mode="wait">
          {loading ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <LoadingScreen />
            </motion.div>
          ) : result ? (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="space-y-6"
            >
              <ResultDisplay result={result} />
              <div className="flex justify-center">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleReset}
                  className="px-8 py-3 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white rounded-xl font-semibold shadow-lg transition-all"
                >
                  Scan Another Medicine
                </motion.button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-8"
            >
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-center py-12"
              >
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                  className="inline-block mb-6"
                >
                  <div className="relative">
                    <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-green-500 rounded-2xl flex items-center justify-center shadow-2xl glow">
                      <Scan className="w-10 h-10 text-white" />
                    </div>
                  </div>
                </motion.div>

                <motion.h2
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-5xl md:text-6xl font-bold text-gray-900 mb-6"
                >
                  Verify Your{" "}
                  <span className="gradient-text">Medicine</span>
                </motion.h2>

                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                  className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed"
                >
                  Upload images of your medicine packaging. Our advanced AI system
                  analyzes barcodes, labels, and cross-verifies against regulatory
                  databases to ensure authenticity and check expiry dates.
                </motion.p>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="grid grid-cols-3 gap-8 max-w-2xl mx-auto mt-12"
                >
                  {[
                    { icon: CheckCircle, label: "95% Accuracy", color: "text-green-500" },
                    { icon: Shield, label: "AI-Powered", color: "text-blue-500" },
                    { icon: Sparkles, label: "Instant Results", color: "text-purple-500" },
                  ].map((stat, index) => (
                    <motion.div
                      key={index}
                      whileHover={{ scale: 1.1, y: -5 }}
                      className="flex flex-col items-center"
                    >
                      <stat.icon className={`w-8 h-8 ${stat.color} mb-2`} />
                      <p className="text-sm font-semibold text-gray-700">{stat.label}</p>
                    </motion.div>
                  ))}
                </motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="glass rounded-2xl p-8 border border-white shadow-xl"
              >
                <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-yellow-500" />
                  How to Scan
                </h3>
                <div className="grid md:grid-cols-3 gap-6">
                  {[
                    {
                      step: "1",
                      title: "Capture Images",
                      desc: "Take clear photos of medicine pack, barcode, and label",
                      icon: Camera,
                    },
                    {
                      step: "2",
                      title: "AI Analysis",
                      desc: "Our system scans barcodes and verifies against databases",
                      icon: Brain,
                    },
                    {
                      step: "3",
                      title: "Get Results",
                      desc: "Receive instant verification with detailed recommendations",
                      icon: FileCheck,
                    },
                  ].map((item, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.7 + index * 0.1 }}
                      whileHover={{ y: -8, transition: { duration: 0.2 } }}
                      className="relative bg-white rounded-xl p-6 shadow-lg border border-gray-100"
                    >
                      <div className="absolute -top-4 -left-4 w-10 h-10 bg-gradient-to-br from-blue-500 to-green-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                        {item.step}
                      </div>
                      <item.icon className="w-12 h-12 text-blue-600 mb-4" />
                      <h4 className="text-lg font-bold text-gray-900 mb-2">{item.title}</h4>
                      <p className="text-sm text-gray-600">{item.desc}</p>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 }}
              >
                <ImageUploader images={images} onImagesChange={handleImagesSelected} />
              </motion.div>

              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="bg-red-50 border-2 border-red-200 rounded-xl p-6 flex items-start gap-4"
                  >
                    <XCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-red-900">Error</p>
                      <p className="text-red-700">{error}</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {images.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 20 }}
                    className="flex justify-center"
                  >
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleScan}
                      disabled={loading}
                      className="group relative px-12 py-5 bg-gradient-to-r from-blue-600 via-blue-500 to-green-600 text-white rounded-2xl font-bold text-lg shadow-2xl hover:shadow-3xl transition-all disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
                    >
                      <span className="relative z-10 flex items-center gap-3">
                        <Scan className="w-6 h-6" />
                        {loading ? "Analyzing..." : "Scan & Verify Medicine"}
                        <Sparkles className="w-5 h-5" />
                      </span>
                      <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    </motion.button>
                  </motion.div>
                )}
              </AnimatePresence>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.1 }}
                className="bg-gradient-to-r from-blue-50 to-green-50 border-2 border-blue-200 rounded-xl p-6"
              >
                <div className="flex items-start gap-4">
                  <AlertTriangle className="w-6 h-6 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-blue-900 mb-2">Medical Disclaimer</p>
                    <p className="text-sm text-blue-800">
                      This tool is for informational purposes only and does not constitute medical advice.
                      Always consult with licensed healthcare professionals and pharmacists.
                    </p>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
        className="relative mt-20 py-12 border-t border-gray-200 bg-white/50 backdrop-blur-sm"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-600 mb-2">
            MediScan - Powered by AI, OpenCV, and Tavily
          </p>
          <p className="text-sm text-gray-500">
            Built to make healthcare safer | ITM University Gwalior
          </p>
        </div>
      </motion.footer>

      <style jsx>{`
        @keyframes blob {
          0%, 100% { transform: translate(0, 0) scale(1); }
          25% { transform: translate(20px, -50px) scale(1.1); }
          50% { transform: translate(-20px, 20px) scale(0.9); }
          75% { transform: translate(50px, 50px) scale(1.05); }
        }

        .animate-blob {
          animation: blob 7s infinite;
        }

        .animation-delay-2000 {
          animation-delay: 2s;
        }

        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
}