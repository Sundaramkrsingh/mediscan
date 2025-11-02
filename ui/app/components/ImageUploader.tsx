"use client";

import React, { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Camera, Upload, X, Image as ImageIcon, CheckCircle2 } from "lucide-react";
import { UploadedImage } from "../types";

interface ImageUploaderProps {
  images: UploadedImage[];
  onImagesChange: (images: UploadedImage[]) => void;
}

export default function ImageUploader({ images, onImagesChange }: ImageUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Detect if mobile
  const isMobile = typeof window !== "undefined" && /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  const handleFileSelect = (files: FileList | null) => {
    if (!files || files.length === 0) return;

    const newImages: UploadedImage[] = [];

    Array.from(files).forEach((file) => {
      if (file.type.startsWith("image/")) {
        const preview = URL.createObjectURL(file);
        newImages.push({
          file,
          preview,
          type: "general",
        });
      }
    });

    onImagesChange([...images, ...newImages]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleRemoveImage = (index: number) => {
    const newImages = images.filter((_, i) => i !== index);
    onImagesChange(newImages);
  };

  const handleCameraClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area with stunning animations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300
          ${isDragging
            ? "border-blue-500 bg-blue-50/50 scale-[1.02] shadow-xl"
            : "border-gray-300 bg-white/80 backdrop-blur-sm"}
          ${!isMobile ? "hover:border-blue-400 hover:bg-gray-50/50 hover:shadow-lg" : ""}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          capture={isMobile ? "environment" : undefined}
          onChange={(e) => handleFileSelect(e.target.files)}
          className="hidden"
        />

        {/* Animated background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-transparent to-green-50/50 rounded-2xl opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

        <div className="relative space-y-6">
          {/* Animated Icon */}
          <motion.div
            className="flex justify-center"
            animate={{
              scale: isDragging ? 1.1 : 1,
              rotate: isDragging ? 5 : 0
            }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }}
          >
            <div className="relative">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-green-500 rounded-2xl flex items-center justify-center shadow-lg">
                {isMobile ? (
                  <Camera className="w-10 h-10 text-white" />
                ) : (
                  <Upload className="w-10 h-10 text-white" />
                )}
              </div>
              {/* Pulse ring animation */}
              <motion.div
                className="absolute inset-0 bg-blue-400 rounded-2xl"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 0, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              />
            </div>
          </motion.div>

          {/* Text Content */}
          <div>
            <motion.p
              className="text-xl font-bold text-gray-800 mb-2"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              {isMobile ? "Capture Medicine Photos" : "Upload Medicine Images"}
            </motion.p>
            <motion.p
              className="text-sm text-gray-600 max-w-md mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              {isMobile
                ? "Take clear photos of the medicine label, barcode, and packaging"
                : "Drag and drop images here, or click below to browse"}
            </motion.p>
          </div>

          {/* Upload Button */}
          <motion.button
            onClick={handleCameraClick}
            whileHover={{ scale: 1.05, boxShadow: "0 10px 30px rgba(59, 130, 246, 0.3)" }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl font-semibold transition-all shadow-lg flex items-center gap-2 mx-auto"
          >
            {isMobile ? (
              <>
                <Camera className="w-5 h-5" />
                Open Camera / Gallery
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                Browse Files
              </>
            )}
          </motion.button>

          {/* Helper Text */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="flex flex-wrap items-center justify-center gap-4 text-xs text-gray-500"
          >
            <span className="flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3 text-green-500" />
              JPG, PNG, WEBP
            </span>
            <span className="flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3 text-green-500" />
              Multiple images
            </span>
            <span className="flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3 text-green-500" />
              Max 10MB each
            </span>
          </motion.div>
        </div>
      </motion.div>

      {/* Image Preview Grid with Stagger Animation */}
      <AnimatePresence>
        {images.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center justify-between mb-4"
            >
              <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                <ImageIcon className="w-5 h-5 text-blue-600" />
                Uploaded Images ({images.length})
              </h3>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onImagesChange([])}
                className="text-sm text-red-600 hover:text-red-700 font-medium flex items-center gap-1"
              >
                <X className="w-4 h-4" />
                Clear All
              </motion.button>
            </motion.div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <AnimatePresence mode="popLayout">
                {images.map((img, index) => (
                  <motion.div
                    key={index}
                    layout
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    transition={{
                      duration: 0.3,
                      delay: index * 0.05,
                      layout: { type: "spring", stiffness: 300, damping: 30 }
                    }}
                    className="relative group"
                  >
                    {/* Image Container */}
                    <div className="relative aspect-square rounded-xl overflow-hidden border-2 border-gray-200 hover:border-blue-400 transition-all shadow-md hover:shadow-xl">
                      <img
                        src={img.preview}
                        alt={`Medicine ${index + 1}`}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                      />

                      {/* Overlay on Hover */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                      {/* Remove Button */}
                      <motion.button
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: 0, scale: 0 }}
                        whileHover={{ scale: 1.1 }}
                        onClick={() => handleRemoveImage(index)}
                        className="absolute top-2 right-2 w-8 h-8 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all shadow-lg"
                        title="Remove image"
                      >
                        <X className="w-4 h-4" />
                      </motion.button>

                      {/* Image Label */}
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent p-3 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                        <p className="text-white text-xs font-semibold">
                          Image {index + 1}
                        </p>
                        <p className="text-white/70 text-[10px]">
                          {(img.file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>

                      {/* Success Checkmark */}
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.05 + 0.2, type: "spring" }}
                        className="absolute top-2 left-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center shadow-lg"
                      >
                        <CheckCircle2 className="w-4 h-4 text-white" />
                      </motion.div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Helpful Tips */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-4 p-4 bg-blue-50/50 rounded-xl border border-blue-200"
            >
              <p className="text-sm text-blue-800 font-medium mb-2">Tips for better results:</p>
              <ul className="text-xs text-blue-700 space-y-1 ml-4">
                <li>• Include clear photos of the barcode and expiry date</li>
                <li>• Ensure good lighting and focus</li>
                <li>• Upload photos of different angles of the packaging</li>
                <li>• Include manufacturer details and batch number if visible</li>
              </ul>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}