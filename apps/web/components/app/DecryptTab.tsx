"use client";

import type React from "react";
import { FileUploader } from "./FileUploader";
import { PasswordInput } from "./PasswordInput";
import { Button } from "@/components/ui/button";
import { getSecretFileIcon, formatFileSize } from "@/lib/api";
import { FaDownload } from "react-icons/fa";

interface DecryptTabProps {
  selectedFile: File | null;
  handleFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  password: string;
  setPassword: (password: string) => void;
  showPassword: boolean;
  setShowPassword: (show: boolean) => void;
  result: any | null;
  extractedFile: File | null;
  message: string;
}

export function DecryptTab({
  selectedFile,
  handleFileUpload,
  password,
  setPassword,
  showPassword,
  setShowPassword,
  result,
  extractedFile,
  message,
}: DecryptTabProps) {
  return (
    <div className="space-y-6 mt-6">
      <FileUploader
        id="encrypted-file"
        selectedFile={selectedFile}
        handleFileUpload={handleFileUpload}
        label="Encrypted File"
        acceptedFileTypes="image/*,video/*,audio/*"
        uploadPrompt="Upload file containing hidden message"
        uploadHint="PNG, JPG, MP4, MP3"
        activeColor="blue"
      />
      <PasswordInput
        id="decrypt-password"
        label="Decryption Password"
        placeholder="Enter the password used for encryption..."
        password={password}
        setPassword={setPassword}
        showPassword={showPassword}
        setShowPassword={setShowPassword}
        activeColor="blue"
      />

      {/* Extracted Content Display */}
      {result && (
        <div className="space-y-2">
          <label className="text-gray-200">Extracted Content</label>
          {extractedFile ? (
            <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  {(() => {
                    const IconComponent = getSecretFileIcon(extractedFile);
                    return (
                      <IconComponent className="text-green-400 text-xl" />
                    );
                  })()}
                  <div>
                    <p className="text-green-400 font-medium">
                      {extractedFile.name}
                    </p>
                    <p className="text-gray-300 text-sm">
                      {formatFileSize(extractedFile.size)} •{" "}
                      {extractedFile.type || "Unknown type"}
                    </p>
                  </div>
                </div>
                <Button className="bg-green-600 hover:bg-green-700">
                  <FaDownload className="mr-2" />
                  Download
                </Button>
              </div>
              {extractedFile.type.startsWith("text/") && message && (
                <div className="p-3 bg-gray-800/50 rounded border border-gray-600">
                  <p className="text-gray-300 text-sm mb-2">Content:</p>
                  <p className="text-green-400 text-sm max-h-32 overflow-y-auto whitespace-pre-wrap">
                    {message}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
              <p className="text-green-400">
                {message || "Your secret message will appear here..."}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}