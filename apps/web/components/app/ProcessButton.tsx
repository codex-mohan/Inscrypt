"use client";

import type React from "react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { FaLock, FaUnlock } from "react-icons/fa";

interface ProcessButtonProps {
  processing: boolean;
  progress: number;
  activeTab: string;
  handleProcess: () => void;
  disabled: boolean;
  secretInputType: "text" | "file";
}

export function ProcessButton({
  processing,
  progress,
  activeTab,
  handleProcess,
  disabled,
  secretInputType,
}: ProcessButtonProps) {
  return (
    <div className="mt-8">
      {processing ? (
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-cyan-400"></div>
            <span className="text-cyan-400">
              {activeTab === "encrypt"
                ? "Encrypting and embedding..."
                : "Extracting and decrypting..."}
            </span>
          </div>
          <Progress value={progress} className="w-full" />
        </div>
      ) : (
        <Button
          onClick={handleProcess}
          disabled={disabled}
          className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50"
        >
          {activeTab === "encrypt" ? (
            <>
              <FaLock className="mr-2" />
              Encrypt & Hide{" "}
              {secretInputType === "file" ? "File" : "Message"}
            </>
          ) : (
            <>
              <FaUnlock className="mr-2" />
              Extract & Decrypt Content
            </>
          )}
        </Button>
      )}
    </div>
  );
}