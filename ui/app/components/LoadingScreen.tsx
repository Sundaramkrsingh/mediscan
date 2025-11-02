"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Loader2,
  Scan,
  FileText,
  Database,
  Shield,
  CheckCircle2,
  Clock,
  Sparkles,
} from "lucide-react";

const verificationSteps = [
  {
    id: 1,
    icon: Scan,
    label: "Detecting barcodes and QR codes",
    duration: 2000,
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    id: 2,
    icon: FileText,
    label: "Extracting text from labels",
    duration: 3000,
    color: "text-purple-600",
    bg: "bg-purple-50",
  },
  {
    id: 3,
    icon: Database,
    label: "Verifying against GS1 database",
    duration: 2500,
    color: "text-green-600",
    bg: "bg-green-50",
  },
  {
    id: 4,
    icon: Shield,
    label: "Checking regulatory compliance",
    duration: 2000,
    color: "text-orange-600",
    bg: "bg-orange-50",
  },
  {
    id: 5,
    icon: Sparkles,
    label: "AI-powered authenticity analysis",
    duration: 3000,
    color: "text-pink-600",
    bg: "bg-pink-50",
  },
];

export default function LoadingScreen() {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  useEffect(() => {
    // Simulate step progression
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        const next = prev + 1;
        if (next < verificationSteps.length) {
          setCompletedSteps((completed) => [...completed, prev]);
          return next;
        }
        return prev;
      });
    }, 3000);

    // Smooth progress bar animation
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 95) return 95;
        return prev + 1;
      });
    }, 150);

    return () => {
      clearInterval(stepInterval);
      clearInterval(progressInterval);
    };
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center py-16 px-4"
    >
      {/* Main Spinner with Glow Effect */}
      <div className="relative mb-12">
        {/* Outer rotating ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear",
          }}
          className="w-32 h-32 border-8 border-transparent border-t-blue-500 border-r-green-500 border-b-purple-500 border-l-pink-500 rounded-full"
        />

        {/* Inner rotating ring (opposite direction) */}
        <motion.div
          animate={{ rotate: -360 }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute inset-2 border-6 border-transparent border-t-pink-400 border-l-blue-400 rounded-full"
        />

        {/* Center icon with pulse */}
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.8, 1, 0.8],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute inset-0 flex items-center justify-center"
        >
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl">
            <Loader2 className="w-10 h-10 text-white" />
          </div>
        </motion.div>

        {/* Glow effect */}
        <motion.div
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute inset-0 bg-blue-400 rounded-full blur-2xl -z-10"
        />
      </div>

      {/* Title with Gradient */}
      <motion.h3
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-3xl font-bold mb-2 gradient-text text-center"
      >
        Analyzing Medicine
      </motion.h3>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-gray-600 mb-8 flex items-center gap-2"
      >
        <Clock className="w-4 h-4" />
        Please wait while we verify your medicine
      </motion.p>

      {/* Progress Bar */}
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: "100%" }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md mb-8"
      >
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Progress: {progress}%
          </span>
          <span className="text-xs text-gray-500">
            Step {currentStep + 1} of {verificationSteps.length}
          </span>
        </div>
        <div className="h-3 bg-gray-200 rounded-full overflow-hidden shadow-inner">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
            className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full shadow-lg"
          />
        </div>
      </motion.div>

      {/* Verification Steps */}
      <div className="w-full max-w-md space-y-3">
        {verificationSteps.map((step, index) => {
          const StepIcon = step.icon;
          const isCompleted = completedSteps.includes(index);
          const isCurrent = currentStep === index;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`
                flex items-center gap-4 p-4 rounded-xl border-2 transition-all
                ${isCurrent
                  ? `${step.bg} border-current scale-105 shadow-lg`
                  : isCompleted
                  ? "bg-green-50 border-green-200"
                  : "bg-gray-50 border-gray-200 opacity-60"
                }
              `}
            >
              {/* Icon */}
              <div
                className={`
                  w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 transition-all
                  ${isCurrent
                    ? `bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg`
                    : isCompleted
                    ? "bg-green-500"
                    : "bg-gray-300"
                  }
                `}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-6 h-6 text-white" />
                ) : (
                  <StepIcon
                    className={`w-6 h-6 ${isCurrent ? "text-white" : "text-gray-500"}`}
                  />
                )}
              </div>

              {/* Label */}
              <div className="flex-1">
                <p
                  className={`font-semibold ${
                    isCurrent
                      ? step.color
                      : isCompleted
                      ? "text-green-700"
                      : "text-gray-500"
                  }`}
                >
                  {step.label}
                </p>
                {isCurrent && (
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ duration: step.duration / 1000 }}
                    className="h-1 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mt-2"
                  />
                )}
              </div>

              {/* Status Indicator */}
              <div>
                <AnimatePresence mode="wait">
                  {isCurrent && (
                    <motion.div
                      key="loading"
                      initial={{ opacity: 0, rotate: 0 }}
                      animate={{ opacity: 1, rotate: 360 }}
                      exit={{ opacity: 0 }}
                      transition={{ rotate: { duration: 1, repeat: Infinity, ease: "linear" } }}
                    >
                      <Loader2 className={`w-5 h-5 ${step.color}`} />
                    </motion.div>
                  )}
                  {isCompleted && (
                    <motion.div
                      key="completed"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      exit={{ scale: 0 }}
                    >
                      <CheckCircle2 className="w-5 h-5 text-green-600" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Floating particles animation */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        {[...Array(8)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-blue-400 rounded-full opacity-20"
            animate={{
              x: [
                Math.random() * window.innerWidth,
                Math.random() * window.innerWidth,
              ],
              y: [
                Math.random() * window.innerHeight,
                Math.random() * window.innerHeight,
              ],
              scale: [1, 1.5, 1],
              opacity: [0.2, 0.5, 0.2],
            }}
            transition={{
              duration: 5 + Math.random() * 5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>

      {/* Time Estimate */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-8 text-sm text-gray-500 text-center flex items-center gap-2"
      >
        <Clock className="w-4 h-4" />
        Estimated time: 10-30 seconds
      </motion.p>

      {/* Fun fact animation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
        className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200 max-w-md"
      >
        <p className="text-sm text-blue-800">
          <strong className="font-semibold">Did you know?</strong> Counterfeit
          medicines account for up to 10% of global pharmaceutical sales. Always
          verify your medicines!
        </p>
      </motion.div>
    </motion.div>
  );
}