"use client";

import type React from "react";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import {
  FaShieldAlt,
  FaLock,
  FaUnlock,
  FaUpload,
  FaDownload,
  FaEye,
  FaEyeSlash,
  FaCog,
  FaCheck,
  FaArrowLeft,
  FaFileImage,
  FaFileVideo,
  FaFileAudio,
  FaFileAlt,
  FaTimes,
  FaKeyboard,
  FaLayerGroup,
  FaPlus,
  FaMinus,
  FaBook,
  FaFileCode,
  FaKey,
  FaQuestionCircle,
} from "react-icons/fa";
import Link from "next/link";
import {
  getFileIcon,
  getSecretFileIcon,
  formatFileSize,
  getFileTypeLabel,
  getSteganographyMethods,
} from "@/lib/api";

export default function InscryptApp() {
  const [activeTab, setActiveTab] = useState("encrypt");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [secretFile, setSecretFile] = useState<File | null>(null);
  const [secretInputType, setSecretInputType] = useState<"text" | "file">(
    "text"
  );
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [encryptionLayers, setEncryptionLayers] = useState([
    { algorithm: "AES", id: 1 },
  ]);
  const [hashMethod, setHashMethod] = useState("SHA256");
  const [steganographyMethod, setSteganographyMethod] = useState("");
  const [processing, setProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<any | null>(null);
  const [extractedFile, setExtractedFile] = useState<File | null>(null);
  const [codebookGenerated, setCodebookGenerated] = useState(false);

  // Decrypt mode states
  const [decryptLayers, setDecryptLayers] = useState([
    { algorithm: "AES", id: 1 },
  ]);
  const [decryptHashMethod, setDecryptHashMethod] = useState("SHA256");
  const [codebookFile, setCodebookFile] = useState<File | null>(null);
  const [useCodebook, setUseCodebook] = useState(false);

  const [encryptionAlgorithms, setEncryptionAlgorithms] = useState<any[]>([]);
  const [hashMethods, setHashMethods] = useState<any[]>([]);
  const [steganographyTechniques, setSteganographyTechniques] = useState<any>(
    {}
  );

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/supported")
      .then((r) => r.json())
      .then((d: any) => {
        setEncryptionAlgorithms(
          d.encryption_algorithms.map((v: string) => ({
            value: v,
            label: v,
            description: `${v} algorithm`,
          }))
        );
        setHashMethods(
          d.hash_algorithms.map((v: string) => ({
            value: v,
            label: v,
            description: `${v} hash function`,
          }))
        );
        setSteganographyTechniques(d.steganography_techniques);
      })
      .catch(console.error);
  }, []);

  // Update steganography method when file changes
  useEffect(() => {
    if (selectedFile) {
      const fileType = selectedFile.type.split("/")[0];
      const methods = steganographyTechniques[fileType] || [];
      if (methods.length > 0) {
        setSteganographyMethod(methods[0].name);
      } else {
        setSteganographyMethod("");
      }
    } else {
      setSteganographyMethod("");
    }
  }, [selectedFile, steganographyTechniques]);

  // Generate obfuscated codebook
  const generateCodebook = () => {
    const codebook = {
      version: "1.0",
      timestamp: new Date().toISOString(),
      layers: encryptionLayers.map((layer, index) => ({
        order: index + 1,
        algorithm: btoa(layer.algorithm), // Base64 encode for obfuscation
        id: btoa(layer.id.toString()),
      })),
      hash: btoa(hashMethod),
      steganography: btoa(steganographyMethod),
      checksum: btoa(
        JSON.stringify(encryptionLayers) + hashMethod + steganographyMethod
      ),
    };
    return JSON.stringify(codebook, null, 2);
  };

  const downloadCodebook = (codebook: any) => {
    const codebookContent = JSON.stringify(codebook, null, 2);
    const blob = new Blob([codebookContent], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `inscrypt-codebook-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadFile = (fileName: string) => {
    const downloadUrl = `http://localhost:8000/api/v1/download/${fileName}`;
    window.open(downloadUrl, "_blank");
  };

  const handleCodebookUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setCodebookFile(file);
      // Parse codebook and set decrypt settings
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const codebook = JSON.parse(e.target?.result as string);
          const layers = codebook.layers.map((layer: any) => ({
            algorithm: atob(layer.algorithm),
            id: Number.parseInt(atob(layer.id)),
          }));
          setDecryptLayers(layers);
          setDecryptHashMethod(atob(codebook.hash));
        } catch (error) {
          console.error("Invalid codebook format");
        }
      };
      reader.readAsText(file);
    }
  };

  const addEncryptionLayer = () => {
    if (encryptionLayers.length < 5 && encryptionAlgorithms.length > 0) {
      setEncryptionLayers([
        ...encryptionLayers,
        { algorithm: encryptionAlgorithms[0].value, id: Date.now() },
      ]);
    }
  };

  const removeEncryptionLayer = (id: number) => {
    if (encryptionLayers.length > 1) {
      setEncryptionLayers(encryptionLayers.filter((layer) => layer.id !== id));
    }
  };

  const updateEncryptionLayer = (id: number, algorithm: string) => {
    setEncryptionLayers(
      encryptionLayers.map((layer) =>
        layer.id === id ? { ...layer, algorithm } : layer
      )
    );
  };

  // Decrypt layer management
  const addDecryptLayer = () => {
    if (decryptLayers.length < 5 && encryptionAlgorithms.length > 0) {
      setDecryptLayers([
        ...decryptLayers,
        { algorithm: encryptionAlgorithms[0].value, id: Date.now() },
      ]);
    }
  };

  const removeDecryptLayer = (id: number) => {
    if (decryptLayers.length > 1) {
      setDecryptLayers(decryptLayers.filter((layer) => layer.id !== id));
    }
  };

  const updateDecryptLayer = (id: number, algorithm: string) => {
    setDecryptLayers(
      decryptLayers.map((layer) =>
        layer.id === id ? { ...layer, algorithm } : layer
      )
    );
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSecretFileUpload = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      setSecretFile(file);
      if (file.type.startsWith("text/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setMessage(e.target?.result as string);
        };
        reader.readAsText(file);
      } else {
        setMessage("");
      }
    }
  };

  const handleRemoveSecretFile = () => {
    setSecretFile(null);
    setMessage("");
  };

  const handleProcess = async () => {
    if (!selectedFile || !password || !steganographyMethod) return;

    setProcessing(true);
    setProgress(0);
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("password", password);
    formData.append("stenographic_technique", steganographyMethod);

    if (activeTab === "encrypt") {
      const secretText =
        secretInputType === "file" && secretFile
          ? await secretFile.text()
          : message;
      formData.append("message", secretText);
      formData.append(
        "encryption_algos",
        encryptionLayers.map((l) => l.algorithm).join(",")
      );
      formData.append("hash_function", hashMethod);

      try {
        const res = await fetch("http://localhost:8000/api/v1/embed", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        if (res.ok) {
          setResult(data);
          setCodebookGenerated(true);
        } else {
          throw new Error(data.detail);
        }
      } catch (err) {
        setResult({ error: String(err) });
      }
    } else {
      if (useCodebook && codebookFile) {
        const cb = await codebookFile.text();
        formData.append("codebook", cb);
      } else {
        formData.append(
          "encryption_algos",
          decryptLayers.map((l) => l.algorithm).join(",")
        );
        formData.append("hash_function", decryptHashMethod);
      }

      try {
        const res = await fetch("http://localhost:8000/api/v1/extract", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        if (res.ok) {
          setMessage(data.message);
          setResult({
            message: "Content successfully extracted and decrypted!",
          });
        } else {
          throw new Error(data.detail);
        }
      } catch (err) {
        setResult({ error: String(err) });
      }
    }

    setProcessing(false);
    setProgress(100);
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Background */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/10 via-black to-blue-900/10" />
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `
              linear-gradient(rgba(6,182,212,0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(6,182,212,0.1) 1px, transparent 1px)
            `,
            backgroundSize: "30px 30px",
          }}
        />
      </div>

      {/* Header */}
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

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto p-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Steganography Workspace
            </h1>
            <p className="text-gray-300 text-lg">
              Securely encrypt and hide messages within your media files using
              advanced steganographic techniques.
            </p>
          </div>

          {/* Main Interface */}
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Left Panel - Controls */}
            <div className="lg:col-span-2">
              <Card className="bg-black/40 backdrop-blur-md border-gray-800/50">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2 text-white">
                    <FaLock className="text-cyan-400" />
                    <span>Steganography Operations</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Tabs
                    value={activeTab}
                    onValueChange={setActiveTab}
                    className="w-full"
                  >
                    <TabsList className="grid w-full grid-cols-2 bg-gray-900/50">
                      <TabsTrigger
                        value="encrypt"
                        className="data-[state=active]:bg-cyan-500/20 data-[state=active]:text-cyan-400"
                      >
                        <FaLock className="mr-2" />
                        Encrypt & Hide
                      </TabsTrigger>
                      <TabsTrigger
                        value="decrypt"
                        className="data-[state=active]:bg-blue-500/20 data-[state=active]:text-blue-400"
                      >
                        <FaUnlock className="mr-2" />
                        Extract & Decrypt
                      </TabsTrigger>
                    </TabsList>

                    <TabsContent value="encrypt" className="space-y-6 mt-6">
                      {/* File Upload */}
                      <div className="space-y-2">
                        <Label className="text-gray-200" htmlFor="cover-file">
                          Cover File (Image/Video/Audio)
                        </Label>
                        <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-cyan-500/50 transition-colors">
                          <input
                            id="cover-file"
                            type="file"
                            accept="image/*,video/*,audio/*"
                            onChange={handleFileUpload}
                            className="hidden"
                          />
                          <label
                            htmlFor="cover-file"
                            className="cursor-pointer"
                          >
                            {selectedFile ? (
                              <div className="flex items-center justify-center space-x-3">
                                {(() => {
                                  const IconComponent =
                                    getFileIcon(selectedFile);
                                  return (
                                    <IconComponent className="text-cyan-400 text-2xl" />
                                  );
                                })()}
                                <div>
                                  <p className="text-cyan-400 font-medium">
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
                                <p className="text-gray-200">
                                  Click to upload or drag and drop
                                </p>
                                <p className="text-gray-300 text-sm mt-1">
                                  PNG, JPG, MP4, MP3 up to 100MB
                                </p>
                              </div>
                            )}
                          </label>
                        </div>
                        {selectedFile && (
                          <div className="mt-2 p-2 bg-cyan-500/10 border border-cyan-500/20 rounded text-center">
                            <p className="text-cyan-400 text-sm">
                              ✓ {getFileTypeLabel(selectedFile)} file detected -
                              Steganography methods available
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Secret Content Input Type Selection */}
                      <div className="space-y-4">
                        <Label className="text-gray-200">Secret Content</Label>
                        <div className="flex space-x-4">
                          <Button
                            type="button"
                            variant={
                              secretInputType === "text" ? "default" : "outline"
                            }
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
                            variant={
                              secretInputType === "file" ? "default" : "outline"
                            }
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

                        {/* Text Input */}
                        {secretInputType === "text" && (
                          <div className="space-y-2">
                            <Textarea
                              id="message"
                              placeholder="Enter your secret message here..."
                              value={message}
                              onChange={(e) => setMessage(e.target.value)}
                              className="bg-gray-900/50 border-gray-700 focus:border-cyan-500 min-h-[100px] text-white placeholder:text-gray-400"
                            />
                            <p className="text-gray-300 text-sm">
                              {message.length} characters
                            </p>
                          </div>
                        )}

                        {/* File Input */}
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
                                <label
                                  htmlFor="secret-file"
                                  className="cursor-pointer"
                                >
                                  <FaUpload className="text-gray-400 text-2xl mx-auto mb-2" />
                                  <p className="text-gray-200 mb-1">
                                    Upload secret file
                                  </p>
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
                                      const IconComponent =
                                        getSecretFileIcon(secretFile);
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
                                {/* Show text content preview for text files */}
                                {secretFile.type.startsWith("text/") &&
                                  message && (
                                    <div className="mt-3 p-3 bg-gray-800/50 rounded border border-gray-600">
                                      <p className="text-gray-300 text-sm mb-1">
                                        Preview:
                                      </p>
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

                      {/* Password */}
                      <div className="space-y-2">
                        <Label className="text-gray-200" htmlFor="password">
                          Encryption Password
                        </Label>
                        <div className="relative">
                          <Input
                            id="password"
                            type={showPassword ? "text" : "password"}
                            placeholder="Enter a strong password..."
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="bg-gray-900/50 border-gray-700 focus:border-cyan-500 pr-10 text-white placeholder:text-gray-400"
                          />
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="absolute right-0 top-0 h-full px-3 text-gray-400 hover:text-cyan-400"
                            onClick={() => setShowPassword(!showPassword)}
                          >
                            {showPassword ? <FaEyeSlash /> : <FaEye />}
                          </Button>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="decrypt" className="space-y-6 mt-6">
                      {/* File Upload for Decryption */}
                      <div className="space-y-2">
                        <Label
                          className="text-gray-200"
                          htmlFor="encrypted-file"
                        >
                          Encrypted File
                        </Label>
                        <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-blue-500/50 transition-colors">
                          <input
                            id="encrypted-file"
                            type="file"
                            accept="image/*,video/*,audio/*"
                            onChange={handleFileUpload}
                            className="hidden"
                          />
                          <label
                            htmlFor="encrypted-file"
                            className="cursor-pointer"
                          >
                            {selectedFile ? (
                              <div className="flex items-center justify-center space-x-3">
                                {(() => {
                                  const IconComponent =
                                    getFileIcon(selectedFile);
                                  return (
                                    <IconComponent className="text-blue-400 text-2xl" />
                                  );
                                })()}
                                <div>
                                  <p className="text-blue-400 font-medium">
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
                                <p className="text-gray-200">
                                  Upload file containing hidden message
                                </p>
                                <p className="text-gray-300 text-sm mt-1">
                                  PNG, JPG, MP4, MP3
                                </p>
                              </div>
                            )}
                          </label>
                        </div>
                        {selectedFile && (
                          <div className="mt-2 p-2 bg-blue-500/10 border border-blue-500/20 rounded text-center">
                            <p className="text-blue-400 text-sm">
                              ✓ {getFileTypeLabel(selectedFile)} file detected -
                              Extraction methods available
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Codebook Option */}
                      <div className="space-y-4">
                        <Label className="text-gray-200">
                          Decryption Method
                        </Label>
                        <div className="flex space-x-4">
                          <Button
                            type="button"
                            variant={!useCodebook ? "default" : "outline"}
                            onClick={() => setUseCodebook(false)}
                            className={`flex items-center space-x-2 ${
                              !useCodebook
                                ? "bg-blue-500/20 text-blue-400 border-blue-500/50"
                                : "border-gray-700 text-gray-300 hover:bg-gray-800/50"
                            }`}
                          >
                            <FaKey />
                            <span>Manual Settings</span>
                          </Button>
                          <div className="flex items-center space-x-2">
                            <Button
                              type="button"
                              variant={useCodebook ? "default" : "outline"}
                              onClick={() => setUseCodebook(true)}
                              className={`flex items-center space-x-2 ${
                                useCodebook
                                  ? "bg-blue-500/20 text-blue-400 border-blue-500/50"
                                  : "border-gray-700 text-gray-300 hover:bg-gray-800/50"
                              }`}
                            >
                              <FaBook />
                              <span>Use Codebook</span>
                            </Button>
                            <div className="relative group">
                              <Button
                                type="button"
                                variant="ghost"
                                size="icon"
                                className="w-6 h-6 text-gray-400 hover:text-blue-400 p-0"
                              >
                                <FaQuestionCircle className="w-4 h-4" />
                              </Button>
                              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50 w-64">
                                <div className="text-xs text-gray-200 text-center">
                                  <p className="font-medium text-blue-400 mb-1">
                                    💡 When to use Codebook:
                                  </p>
                                  <p className="mb-1">
                                    • Forgotten encryption layer order
                                  </p>
                                  <p className="mb-1">
                                    • Forgotten hash method used
                                  </p>
                                  <p>• Shared encrypted files with others</p>
                                </div>
                                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Codebook Upload */}
                        {useCodebook && (
                          <div className="space-y-2">
                            {!codebookFile ? (
                              <div className="border-2 border-dashed border-gray-700 rounded-lg p-6 text-center hover:border-blue-500/50 transition-colors">
                                <input
                                  id="codebook-file"
                                  type="file"
                                  accept=".json"
                                  onChange={handleCodebookUpload}
                                  className="hidden"
                                />
                                <label
                                  htmlFor="codebook-file"
                                  className="cursor-pointer"
                                >
                                  <FaFileCode className="text-gray-400 text-2xl mx-auto mb-2" />
                                  <p className="text-gray-200 mb-1">
                                    Upload Codebook
                                  </p>
                                  <p className="text-gray-300 text-sm">
                                    JSON file containing encryption
                                    configuration
                                  </p>
                                </label>
                              </div>
                            ) : (
                              <div className="bg-gray-900/30 border border-gray-700 rounded-lg p-4">
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center space-x-3">
                                    <FaFileCode className="text-blue-400 text-xl" />
                                    <div>
                                      <p className="text-blue-400 font-medium">
                                        {codebookFile.name}
                                      </p>
                                      <p className="text-gray-300 text-sm">
                                        {formatFileSize(codebookFile.size)} •
                                        Codebook loaded
                                      </p>
                                    </div>
                                  </div>
                                  <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => setCodebookFile(null)}
                                    className="text-gray-400 hover:text-red-400"
                                  >
                                    <FaTimes />
                                  </Button>
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>

                      {/* Password for Decryption */}
                      <div className="space-y-2">
                        <Label
                          className="text-gray-200"
                          htmlFor="decrypt-password"
                        >
                          Decryption Password
                        </Label>
                        <div className="relative">
                          <Input
                            id="decrypt-password"
                            type={showPassword ? "text" : "password"}
                            placeholder="Enter the password used for encryption..."
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="bg-gray-900/50 border-gray-700 focus:border-blue-500 pr-10 text-white placeholder:text-gray-400"
                          />
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="absolute right-0 top-0 h-full px-3 text-gray-400 hover:text-blue-400"
                            onClick={() => setShowPassword(!showPassword)}
                          >
                            {showPassword ? <FaEyeSlash /> : <FaEye />}
                          </Button>
                        </div>
                      </div>

                      {/* Extracted Content Display */}
                      {result && activeTab === "decrypt" && (
                        <div className="space-y-2">
                          <Label className="text-gray-200">
                            Extracted Content
                          </Label>
                          {extractedFile ? (
                            <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center space-x-3">
                                  {(() => {
                                    const IconComponent =
                                      getSecretFileIcon(extractedFile);
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
                              {extractedFile.type.startsWith("text/") &&
                                message && (
                                  <div className="p-3 bg-gray-800/50 rounded border border-gray-600">
                                    <p className="text-gray-300 text-sm mb-2">
                                      Content:
                                    </p>
                                    <p className="text-green-400 text-sm max-h-32 overflow-y-auto whitespace-pre-wrap">
                                      {message}
                                    </p>
                                  </div>
                                )}
                            </div>
                          ) : (
                            <div className="bg-gray-900/50 border border-gray-700 rounded-lg p-4">
                              <p className="text-green-400">
                                {message ||
                                  "Your secret message will appear here..."}
                              </p>
                            </div>
                          )}
                        </div>
                      )}
                    </TabsContent>
                  </Tabs>

                  {/* Process Button */}
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
                        disabled={
                          !selectedFile ||
                          !password ||
                          !steganographyMethod ||
                          (activeTab === "encrypt" &&
                            secretInputType === "text" &&
                            !message) ||
                          (activeTab === "encrypt" &&
                            secretInputType === "file" &&
                            !secretFile) ||
                          (activeTab === "decrypt" &&
                            useCodebook &&
                            !codebookFile)
                        }
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

                  {/* Result */}
                  {result && !result.error && activeTab === "encrypt" && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg"
                    >
                      <div className="flex items-center space-x-2 mb-3">
                        <FaCheck className="text-green-400" />
                        <span className="text-green-400 font-medium">
                          Content successfully encrypted and embedded!
                        </span>
                      </div>
                      <div className="flex space-x-3">
                        <Button
                          onClick={() => downloadFile(result.output_path)}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          <FaDownload className="mr-2" />
                          Download Encrypted File
                        </Button>
                        {codebookGenerated && (
                          <Button
                            onClick={() => downloadCodebook(result.codebook)}
                            className="bg-blue-600 hover:bg-blue-700"
                          >
                            <FaBook className="mr-2" />
                            Download Codebook
                          </Button>
                        )}
                      </div>
                    </motion.div>
                  )}
                  {result && result.error && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg"
                    >
                      <div className="flex items-center space-x-2 mb-3">
                        <FaTimes className="text-red-400" />
                        <span className="text-red-400 font-medium">
                          An error occurred: {result.error}
                        </span>
                      </div>
                    </motion.div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Right Panel - Settings & Info */}
            <div className="space-y-6">
              {/* Algorithm Settings - Context Aware */}
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
                          <Label className="text-gray-200">
                            Encryption Layers
                          </Label>
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
                                    <SelectItem
                                      key={algo.value}
                                      value={algo.value}
                                    >
                                      <div>
                                        <div className="font-medium">
                                          {algo.label}
                                        </div>
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
                                  onClick={() =>
                                    removeEncryptionLayer(layer.id)
                                  }
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
                            💡 Multiple layers provide cascading encryption for
                            enhanced security
                          </p>
                        </div>
                      </div>

                      {/* Hash Method */}
                      <div className="space-y-2">
                        <Label className="text-gray-200">Hash Method</Label>
                        <Select
                          value={hashMethod}
                          onValueChange={setHashMethod}
                        >
                          <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent className="bg-gray-900 border-gray-700 text-white">
                            {hashMethods.map((hash) => (
                              <SelectItem key={hash.value} value={hash.value}>
                                <div>
                                  <div className="font-medium">
                                    {hash.label}
                                  </div>
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
                        <Label className="text-gray-200">
                          Steganography Method
                        </Label>
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
                                <SelectItem
                                  key={method.name}
                                  value={method.name}
                                >
                                  <div>
                                    <div className="font-medium">
                                      {method.name}
                                    </div>
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
                    <>
                      {/* Decryption Settings */}
                      {!useCodebook ? (
                        <>
                          {/* Manual Decryption Layers */}
                          <div className="space-y-3">
                            <div className="flex items-center justify-between">
                              <Label className="text-gray-200">
                                Decryption Layers
                              </Label>
                              <div className="flex items-center space-x-2">
                                <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20">
                                  <FaLayerGroup className="mr-1" />
                                  {decryptLayers.length} Layer
                                  {decryptLayers.length !== 1 ? "s" : ""}
                                </Badge>
                                <Button
                                  type="button"
                                  size="sm"
                                  onClick={addDecryptLayer}
                                  disabled={decryptLayers.length >= 5}
                                  className="bg-blue-500/20 text-blue-400 border-blue-500/50 hover:bg-blue-500/30"
                                >
                                  <FaPlus />
                                </Button>
                              </div>
                            </div>

                            <div className="space-y-3 max-h-64 overflow-y-auto">
                              {decryptLayers.map((layer, index) => (
                                <div
                                  key={layer.id}
                                  className="flex items-center space-x-2"
                                >
                                  <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full flex items-center justify-center text-blue-400 text-sm font-bold">
                                    {index + 1}
                                  </div>
                                  <Select
                                    value={layer.algorithm}
                                    onValueChange={(value) =>
                                      updateDecryptLayer(layer.id, value)
                                    }
                                  >
                                    <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white flex-1">
                                      <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent className="bg-gray-900 border-gray-700 text-white">
                                      {encryptionAlgorithms.map((algo) => (
                                        <SelectItem
                                          key={algo.value}
                                          value={algo.value}
                                        >
                                          <div>
                                            <div className="font-medium">
                                              {algo.label}
                                            </div>
                                            <div className="text-sm text-gray-400">
                                              {algo.description}
                                            </div>
                                          </div>
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                  {decryptLayers.length > 1 && (
                                    <Button
                                      type="button"
                                      size="sm"
                                      variant="ghost"
                                      onClick={() =>
                                        removeDecryptLayer(layer.id)
                                      }
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
                                ⚠️ Layer order must match the encryption
                                sequence
                              </p>
                            </div>
                          </div>

                          {/* Hash Method for Decryption */}
                          <div className="space-y-2">
                            <Label className="text-gray-200">Hash Method</Label>
                            <Select
                              value={decryptHashMethod}
                              onValueChange={setDecryptHashMethod}
                            >
                              <SelectTrigger className="bg-gray-900/50 border-gray-700 text-white">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent className="bg-gray-900 border-gray-700 text-white">
                                {hashMethods.map((hash) => (
                                  <SelectItem
                                    key={hash.value}
                                    value={hash.value}
                                  >
                                    <div>
                                      <div className="font-medium">
                                        {hash.label}
                                      </div>
                                      <div className="text-sm text-gray-400">
                                        {hash.description}
                                      </div>
                                    </div>
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </div>
                        </>
                      ) : (
                        <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg text-center">
                          <FaBook className="text-blue-400 text-2xl mx-auto mb-2" />
                          <p className="text-blue-400 font-medium mb-1">
                            Codebook Mode Active
                          </p>
                          <p className="text-gray-300 text-sm">
                            Encryption settings will be loaded from the uploaded
                            codebook
                          </p>
                        </div>
                      )}
                    </>
                  )}
                </CardContent>
              </Card>

              {/* Security Status */}
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
                          {
                            hashMethods.find((h) => h.value === hashMethod)
                              ?.label
                          }
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Steganography</span>
                        <Badge
                          className={`${steganographyMethod ? "bg-green-500/10 text-green-400 border-green-500/20" : "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"}`}
                        >
                          <FaCheck className="mr-1" />
                          {steganographyMethod ? "Ready" : "Pending File"}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Codebook</span>
                        <Badge className="bg-cyan-500/10 text-cyan-400 border-cyan-500/20">
                          <FaBook className="mr-1" />
                          Will Generate
                        </Badge>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Decryption Mode</span>
                        <Badge
                          className={`${useCodebook ? "bg-blue-500/10 text-blue-400 border-blue-500/20" : "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"}`}
                        >
                          {useCodebook ? (
                            <FaBook className="mr-1" />
                          ) : (
                            <FaKey className="mr-1" />
                          )}
                          {useCodebook ? "Codebook" : "Manual"}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Configuration</span>
                        <Badge
                          className={`${(useCodebook && codebookFile) || (!useCodebook && decryptLayers.length > 0) ? "bg-green-500/10 text-green-400 border-green-500/20" : "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"}`}
                        >
                          <FaCheck className="mr-1" />
                          {(useCodebook && codebookFile) ||
                          (!useCodebook && decryptLayers.length > 0)
                            ? "Ready"
                            : "Pending"}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Layers</span>
                        <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20">
                          <FaLayerGroup className="mr-1" />
                          {useCodebook
                            ? codebookFile
                              ? "From Codebook"
                              : "Pending"
                            : `${decryptLayers.length}x`}
                        </Badge>
                      </div>
                    </>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Detection Risk</span>
                    <Badge className="bg-green-500/10 text-green-400 border-green-500/20">
                      <FaCheck className="mr-1" />
                      Minimal
                    </Badge>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Stats */}
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
                        : useCodebook
                          ? "Codebook"
                          : "Manual"}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}
