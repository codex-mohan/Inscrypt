"use client";

import type React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { FaEye, FaEyeSlash } from "react-icons/fa";

interface PasswordInputProps {
  id: string;
  label: string;
  placeholder: string;
  password: string;
  setPassword: (password: string) => void;
  showPassword: boolean;
  setShowPassword: (show: boolean) => void;
  activeColor: "cyan" | "blue";
}

export function PasswordInput({
  id,
  label,
  placeholder,
  password,
  setPassword,
  showPassword,
  setShowPassword,
  activeColor,
}: PasswordInputProps) {
  const focusBorderClass =
    activeColor === "cyan"
      ? "focus:border-cyan-500"
      : "focus:border-blue-500";
  const hoverTextClass =
    activeColor === "cyan" ? "hover:text-cyan-400" : "hover:text-blue-400";

  return (
    <div className="space-y-2">
      <Label className="text-gray-200" htmlFor={id}>
        {label}
      </Label>
      <div className="relative">
        <Input
          id={id}
          type={showPassword ? "text" : "password"}
          placeholder={placeholder}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={`bg-gray-900/50 border-gray-700 ${focusBorderClass} pr-10 text-white placeholder:text-gray-400`}
        />
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className={`absolute right-0 top-0 h-full px-3 text-gray-400 ${hoverTextClass}`}
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? <FaEyeSlash /> : <FaEye />}
        </Button>
      </div>
    </div>
  );
}