"use client";

import type React from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  FaBook,
  FaCog,
  FaLayerGroup,
  FaPlus,
  FaMinus,
} from "react-icons/fa";

interface AlgorithmSettingsProps {
  activeTab: string;
  encryptionLayers: { algorithm: string; id: number }[];
  addEncryptionLayer: () => void;
  updateEncryptionLayer: (id: number, algorithm: string) => void;
  removeEncryptionLayer: (id: number) => void;
  encryptionAlgorithms: {
    value: string;
    label: string;
    description: string;
  }[];
  hashMethod: string;
  setHashMethod: (value: string) => void;
  hashMethods: { value: string; label: string; description: string }[];
  steganographyMethod: string;
  setSteganographyMethod: (value: string) => void;
  steganographyTechniques: any;
  selectedFile: File | null;
}

export function AlgorithmSettings({
  activeTab,
  encryptionLayers,
  addEncryptionLayer,
  updateEncryptionLayer,
  removeEncryptionLayer,
  encryptionAlgorithms,
  hashMethod,
  setHashMethod,
  hashMethods,
  steganographyMethod,
  setSteganographyMethod,
  steganographyTechniques,
  selectedFile,
}: AlgorithmSettingsProps) {
  return (
    <Card className="bg-black/40 backdrop-blur-md border-gray-800/50">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2 text-white">
          <FaCog className="text-cyan-400" />
          <span>
            {activeTab === "encrypt"
              ? "Encryption Settings"
              : "Decryption Settings"}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {activeTab === "encrypt" ? (
          <>
            {/* Encryption Layers */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label className="text-gray-200">Encryption Layers</Label>
                <div className="flex items-center space-x-2">
                  <Badge className="bg-cyan-500/10 text-cyan-400 border-cyan-500/20">
                    <FaLayerGroup className="mr-1" />
                    {encryptionLayers.length} Layer
                    {encryptionLayers.length !== 1 ? "s" : ""}
                  </Badge>
                  <Button
                    type="button"
                    size="sm"
                    onClick={addEncryptionLayer}
                    disabled={encryptionLayers.length >= 5}
                    className="bg-cyan-500/20 text-cyan-400 border-cyan-500/50 hover:bg-cyan-500/30"
                  >
                    <FaPlus />
                  </Button>
                </div>
              </div>

              <div className="space-y-3 max-h-64 overflow-y-auto">
                {encryptionLayers.map((layer, index) => (
                  <div
                    key={layer.id}
                    className="flex items-center space-x-2"
                  >
                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full flex items-center justify-center text-cyan-400 text-sm font-bold">
                      {index + 1}
                    </div>
                    <Select
                      value={layer.algorithm}
                      onValueChange={(value) =>
                        updateEncryptionLayer(layer.id, value)
                      }
                    >
                      <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white flex-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-900 border-gray-700 text-white">
                        {encryptionAlgorithms.map((algo) => (
                          <SelectItem key={algo.value} value={algo.value}>
                            <div>
                              <div className="font-medium">{algo.label}</div>
                              <div className="text-sm text-gray-400">
                                {algo.description}
                              </div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {encryptionLayers.length > 1 && (
                      <Button
                        type="button"
                        size="sm"
                        variant="ghost"
                        onClick={() => removeEncryptionLayer(layer.id)}
                        className="text-gray-400 hover:text-red-400 flex-shrink-0"
                      >
                        <FaMinus />
                      </Button>
                    )}
                  </div>
                ))}
              </div>

              <div className="text-xs text-gray-400 bg-gray-900/30 p-2 rounded">
                <p>
                  💡 Multiple layers provide cascading encryption for enhanced
                  security
                </p>
              </div>
            </div>

            {/* Hash Method */}
            <div className="space-y-2">
              <Label className="text-gray-200">Hash Method</Label>
              <Select value={hashMethod} onValueChange={setHashMethod}>
                <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-gray-900 border-gray-700 text-white">
                  {hashMethods.map((hash) => (
                    <SelectItem key={hash.value} value={hash.value}>
                      <div>
                        <div className="font-medium">{hash.label}</div>
                        <div className="text-sm text-gray-400">
                          {hash.description}
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Steganography Method */}
            <div className="space-y-2">
              <Label className="text-gray-200">Steganography Method</Label>
              {!selectedFile ? (
                <div className="p-3 bg-gray-900/30 border border-gray-700 rounded text-center">
                  <p className="text-gray-400 text-sm">
                    Upload a cover file to see available methods
                  </p>
                </div>
              ) : (
                <Select
                  value={steganographyMethod}
                  onValueChange={setSteganographyMethod}
                >
                  <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white">
                    <SelectValue placeholder="Select method..." />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-900 border-gray-700 text-white">
                    {(
                      steganographyTechniques[
                        selectedFile.type.split("/")[0]
                      ] || []
                    ).map((method: any) => (
                      <SelectItem key={method.name} value={method.name}>
                        <div>
                          <div className="font-medium">{method.name}</div>
                          <div className="text-sm text-gray-400">
                            {method.description}
                          </div>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            </div>
          </>
        ) : (
          <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg text-center">
            <FaBook className="text-blue-400 text-2xl mx-auto mb-2" />
            <p className="text-blue-400 font-medium mb-1">Ready to Decrypt</p>
            <p className="text-gray-300 text-sm">
              Provide the encrypted file and password to extract the hidden
              content.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}