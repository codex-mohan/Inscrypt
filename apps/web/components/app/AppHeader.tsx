"use client";

import type React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FaArrowLeft, FaCog, FaShieldAlt } from "react-icons/fa";

export function AppHeader() {
  return (
    <header className="relative z-10 p-6 backdrop-blur-md bg-black/20 border-b border-cyan-500/20">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link href="/">
            <Button
              variant="ghost"
              size="icon"
              className="text-cyan-400 hover:bg-cyan-400/10"
            >
              <FaArrowLeft />
            </Button>
          </Link>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
              <FaShieldAlt className="text-white text-xl" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Inscrypt
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse" />
            Secure Connection
          </Badge>
          <Button
            variant="ghost"
            size="icon"
            className="text-cyan-400 hover:bg-cyan-400/10"
          >
            <FaCog />
          </Button>
        </div>
      </div>
    </header>
  );
}