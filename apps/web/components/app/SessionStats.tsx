"use client";

import type React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SessionStatsProps {
  activeTab: string;
  encryptionLayers: { algorithm: string; id: number }[];
}

export function SessionStats({
  activeTab,
  encryptionLayers,
}: SessionStatsProps) {
  return (
    <Card className="bg-black/40 backdrop-blur-md border-gray-800/50">
      <CardHeader>
        <CardTitle className="text-white">Session Stats</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-300">Files Processed</span>
          <span className="text-cyan-400 font-mono">0</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-300">Content Hidden</span>
          <span className="text-cyan-400 font-mono">0</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-300">Security Level</span>
          <span className="text-green-400 font-mono">
            {activeTab === "encrypt"
              ? encryptionLayers.length > 1
                ? "Maximum"
                : "High"
              : "Ready"}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}