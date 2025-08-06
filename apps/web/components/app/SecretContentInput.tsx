"use client";

import type React from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  getSecretFileIcon,
  formatFileSize,
} from "@/lib/api";
import { FaKeyboard, FaUpload, FaTimes } from "react-icons/fa";

interface SecretContentInputProps {
  secretInputType: "text" | "file";
  setSecretInputType: (type: "text" | "file") => void;
  message: string;
  setMessage: (message: string) => void;
  secretFile: File | null;
  setSecretFile: (file: File | null) => void;
  handleSecretFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  handleRemoveSecretFile: () => void;
}

export function SecretContentInput({
  secretInputType,
  setSecretInputType,
  message,
  setMessage,
  secretFile,
  setSecretFile,
  handleSecretFileUpload,
  handleRemoveSecretFile,
}: SecretContentInputProps) {
  return (
    <div className="space-y-4">
      <label className="text-gray-200">Secret Content</label>
      <div className="flex space-x-4">
        <Button
          type="button"
          variant={secretInputType === "text" ? "default" : "outline"}
          onClick={() => {
            setSecretInputType("text");
            setSecretFile(null);
          }}
          className={`flex items-center space-x-2 ${
            secretInputType === "text"
              ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/50"
              : "border-gray-700 text-gray-300 hover:bg-gray-800/50"
          }`}
        >
          <FaKeyboard />
          <span>Type Message</span>
        </Button>
        <Button
          type="button"
          variant={secretInputType === "file" ? "default" : "outline"}
          onClick={() => {
            setSecretInputType("file");
            setMessage("");
          }}
          className={`flex items-center space-x-2 ${
            secretInputType === "file"
              ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/50"
              : "border-gray-700 text-gray-300 hover:bg-gray-800/50"
          }`}
        >
          <FaUpload />
          <span>Upload File</span>
        </Button>
      </div>

      {secretInputType === "text" && (
        <div className="space-y-2">
          <Textarea
            id="message"
            placeholder="Enter your secret message here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="bg-gray-900/50 border-gray-700 focus:border-cyan-500 min-h-[100px] text-white placeholder:text-gray-400"
          />
          <p className="text-gray-300 text-sm">{message.length} characters</p>
        </div>
      )}

      {secretInputType === "file" && (
        <div className="space-y-2">
          {!secretFile ? (
            <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-cyan-500/50 transition-colors">
              <input
                id="secret-file"
                type="file"
                accept="text/*,image/*,audio/*"
                onChange={handleSecretFileUpload}
                className="hidden"
              />
              <label htmlFor="secret-file" className="cursor-pointer">
                <FaUpload className="text-gray-400 text-2xl mx-auto mb-2" />
                <p className="text-gray-200 mb-1">Upload secret file</p>
                <p className="text-gray-300 text-sm">
                  Text files, Images, Audio up to 50MB
                </p>
              </label>
            </div>
          ) : (
            <div className="bg-gray-900/30 border border-gray-700 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {(() => {
                    const IconComponent = getSecretFileIcon(secretFile);
                    return (
                      <IconComponent className="text-cyan-400 text-xl" />
                    );
                  })()}
                  <div>
                    <p className="text-cyan-400 font-medium">
                      {secretFile.name}
                    </p>
                    <p className="text-gray-300 text-sm">
                      {formatFileSize(secretFile.size)} •{" "}
                      {secretFile.type || "Unknown type"}
                    </p>
                  </div>
                </div>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  onClick={handleRemoveSecretFile}
                  className="text-gray-400 hover:text-red-400"
                >
                  <FaTimes />
                </Button>
              </div>
              {secretFile.type.startsWith("text/") && message && (
                <div className="mt-3 p-3 bg-gray-800/50 rounded border border-gray-600">
                  <p className="text-gray-300 text-sm mb-1">Preview:</p>
                  <p className="text-gray-200 text-sm max-h-20 overflow-y-auto">
                    {message.length > 200
                      ? `${message.substring(0, 200)}...`
                      : message}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}