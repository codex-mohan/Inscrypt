"use client";

import type React from "react";
import { FileUploader } from "./FileUploader";
import { SecretContentInput } from "./SecretContentInput";
import { PasswordInput } from "./PasswordInput";

interface EncryptTabProps {
  selectedFile: File | null;
  handleFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  secretInputType: "text" | "file";
  setSecretInputType: (type: "text" | "file") => void;
  message: string;
  setMessage: (message: string) => void;
  secretFile: File | null;
  setSecretFile: (file: File | null) => void;
  handleSecretFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  handleRemoveSecretFile: () => void;
  password: string;
  setPassword: (password: string) => void;
  showPassword: boolean;
  setShowPassword: (show: boolean) => void;
}

export function EncryptTab({
  selectedFile,
  handleFileUpload,
  secretInputType,
  setSecretInputType,
  message,
  setMessage,
  secretFile,
  setSecretFile,
  handleSecretFileUpload,
  handleRemoveSecretFile,
  password,
  setPassword,
  showPassword,
  setShowPassword,
}: EncryptTabProps) {
  return (
    <div className="space-y-6 mt-6">
      <FileUploader
        id="cover-file"
        selectedFile={selectedFile}
        handleFileUpload={handleFileUpload}
        label="Cover File (Image/Video/Audio)"
        acceptedFileTypes="image/*,video/*,audio/*"
        uploadPrompt="Click to upload or drag and drop"
        uploadHint="PNG, JPG, MP4, MP3 up to 100MB"
        activeColor="cyan"
      />
      <SecretContentInput
        secretInputType={secretInputType}
        setSecretInputType={setSecretInputType}
        message={message}
        setMessage={setMessage}
        secretFile={secretFile}
        setSecretFile={setSecretFile}
        handleSecretFileUpload={handleSecretFileUpload}
        handleRemoveSecretFile={handleRemoveSecretFile}
      />
      <PasswordInput
        id="password"
        label="Encryption Password"
        placeholder="Enter a strong password..."
        password={password}
        setPassword={setPassword}
        showPassword={showPassword}
        setShowPassword={setShowPassword}
        activeColor="cyan"
      />
    </div>
  );
}