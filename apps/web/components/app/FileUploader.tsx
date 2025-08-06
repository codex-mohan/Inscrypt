"use client";

import type React from "react";
import {
  getFileIcon,
  formatFileSize,
  getFileTypeLabel,
} from "@/lib/api";
import { FaUpload } from "react-icons/fa";

interface FileUploaderProps {
  id: string;
  selectedFile: File | null;
  handleFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  label: string;
  acceptedFileTypes: string;
  uploadPrompt: string;
  uploadHint: string;
  activeColor: "cyan" | "blue";
}

export function FileUploader({
  id,
  selectedFile,
  handleFileUpload,
  label,
  acceptedFileTypes,
  uploadPrompt,
  uploadHint,
  activeColor,
}: FileUploaderProps) {
  const hoverBorderClass =
    activeColor === "cyan"
      ? "hover:border-cyan-500/50"
      : "hover:border-blue-500/50";
  const textClass =
    activeColor === "cyan" ? "text-cyan-400" : "text-blue-400";

  return (
    <div className="space-y-2">
      <label className="text-gray-200" htmlFor={id}>
        {label}
      </label>
      <div
        className={`border-2 border-dashed border-gray-700 rounded-lg p-8 text-center ${hoverBorderClass} transition-colors`}
      >
        <input
          id={id}
          type="file"
          accept={acceptedFileTypes}
          onChange={handleFileUpload}
          className="hidden"
        />
        <label htmlFor={id} className="cursor-pointer">
          {selectedFile ? (
            <div className="flex items-center justify-center space-x-3">
              {(() => {
                const IconComponent = getFileIcon(selectedFile);
                return <IconComponent className={`${textClass} text-2xl`} />;
              })()}
              <div>
                <p className={`${textClass} font-medium`}>
                  {selectedFile.name}
                </p>
                <p className="text-gray-300 text-sm">
                  {formatFileSize(selectedFile.size)} •{" "}
                  {getFileTypeLabel(selectedFile)}
                </p>
              </div>
            </div>
          ) : (
            <div>
              <FaUpload className="text-gray-400 text-3xl mx-auto mb-3" />
              <p className="text-gray-200">{uploadPrompt}</p>
              <p className="text-gray-300 text-sm mt-1">{uploadHint}</p>
            </div>
          )}
        </label>
      </div>
      {selectedFile && (
        <div
          className={`mt-2 p-2 bg-${activeColor}-500/10 border border-${activeColor}-500/20 rounded text-center`}
        >
          <p className={`${textClass} text-sm`}>
            ✓ {getFileTypeLabel(selectedFile)} file detected - Steganography
            methods available
          </p>
        </div>
      )}
    </div>
  );
}