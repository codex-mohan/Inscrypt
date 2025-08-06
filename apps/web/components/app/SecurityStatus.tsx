"use client";

import type React from "react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FaCheck, FaLayerGroup, FaShieldAlt } from "react-icons/fa";

interface SecurityStatusProps {
  activeTab: string;
  encryptionLayers: { algorithm: string; id: number }[];
  hashMethod: string;
  hashMethods: { value: string; label: string }[];
  steganographyMethod: string;
}

export function SecurityStatus({
  activeTab,
  encryptionLayers,
  hashMethod,
  hashMethods,
  steganographyMethod,
}: SecurityStatusProps) {
  return (
    <Card className="bg-black/40 backdrop-blur-md border-gray-800/50">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2 text-white">
          <FaShieldAlt className="text-green-400" />
          <span>Security Status</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {activeTab === "encrypt" ? (
          <>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Encryption Layers</span>
              <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
                <FaLayerGroup className="mr-1" />
                {encryptionLayers.length}x Active
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Hash Function</span>
              <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
                <FaCheck className="mr-1" />
                {hashMethods.find((h) => h.value === hashMethod)?.label}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300">Steganography</span>
              <Badge
                className={`${
                  steganographyMethod
                    ? "bg-green-500/10 text-green-400 border-green-500/20"
                    : "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                }`}
              >
                <FaCheck className="mr-1" />
                {steganographyMethod ? "Ready" : "Pending File"}
              </Badge>
            </div>
          </>
        ) : null}
        <div className="flex items-center justify-between">
          <span className="text-gray-300">Detection Risk</span>
          <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
            <FaCheck className="mr-1" />
            Minimal
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}