"use client";

import type React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { FaCheck, FaDownload, FaTimes } from "react-icons/fa";

interface ResultDisplayProps {
  result: any | null;
  activeTab: string;
  downloadFile: (fileName: string) => void;
}

export function ResultDisplay({
  result,
  activeTab,
  downloadFile,
}: ResultDisplayProps) {
  if (!result) return null;

  if (result.error) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg"
      >
        <div className="flex items-center space-x-2 mb-3">
          <FaTimes className="text-red-400" />
          <span className="text-red-400 font-medium">
            An error occurred: {result.error}
          </span>
        </div>
      </motion.div>
    );
  }

  if (activeTab === "encrypt" && result.output_path) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg"
      >
        <div className="flex items-center space-x-2 mb-3">
          <FaCheck className="text-green-400" />
          <span className="text-green-400 font-medium">
            Content successfully encrypted and embedded!
          </span>
        </div>
        <div className="flex space-x-3">
          <Button
            onClick={() => downloadFile(result.output_path)}
            className="bg-green-600 hover:bg-green-700"
          >
            <FaDownload className="mr-2" />
            Download Encrypted File
          </Button>
        </div>
      </motion.div>
    );
  }

  return null;
}