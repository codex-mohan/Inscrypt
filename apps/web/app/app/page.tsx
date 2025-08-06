"use client";

import type React from "react";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FaLock, FaUnlock } from "react-icons/fa";
import { AppHeader } from "@/components/app/AppHeader";
import { AlgorithmSettings } from "@/components/app/AlgorithmSettings";
import { SecurityStatus } from "@/components/app/SecurityStatus";
import { SessionStats } from "@/components/app/SessionStats";
import { EncryptTab } from "@/components/app/EncryptTab";
import { DecryptTab } from "@/components/app/DecryptTab";
import { ProcessButton } from "@/components/app/ProcessButton";
import { ResultDisplay } from "@/components/app/ResultDisplay";

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

  const downloadFile = (fileName: string) => {
    const downloadUrl = `http://localhost:8000/api/v1/download/${fileName}`;
    window.open(downloadUrl, "_blank");
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

  const handleTabChange = (value: string) => {
    setActiveTab(value);
    setSelectedFile(null);
    setMessage("");
    setSecretFile(null);
    setPassword("");
    setResult(null);
    setExtractedFile(null);
    setProcessing(false);
    setProgress(0);
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
        } else {
          throw new Error(data.detail);
        }
      } catch (err) {
        setResult({ error: String(err) });
      }
    } else {
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

      <AppHeader />

      <main className="relative z-10 max-w-7xl mx-auto p-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Steganography Workspace
            </h1>
            <p className="text-gray-300 text-lg">
              Securely encrypt and hide messages within your media files using
              advanced steganographic techniques.
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
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
                    onValueChange={handleTabChange}
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

                    <TabsContent value="encrypt">
                      <EncryptTab
                        selectedFile={selectedFile}
                        handleFileUpload={handleFileUpload}
                        secretInputType={secretInputType}
                        setSecretInputType={setSecretInputType}
                        message={message}
                        setMessage={setMessage}
                        secretFile={secretFile}
                        setSecretFile={setSecretFile}
                        handleSecretFileUpload={handleSecretFileUpload}
                        handleRemoveSecretFile={handleRemoveSecretFile}
                        password={password}
                        setPassword={setPassword}
                        showPassword={showPassword}
                        setShowPassword={setShowPassword}
                      />
                    </TabsContent>
                    <TabsContent value="decrypt">
                      <DecryptTab
                        selectedFile={selectedFile}
                        handleFileUpload={handleFileUpload}
                        password={password}
                        setPassword={setPassword}
                        showPassword={showPassword}
                        setShowPassword={setShowPassword}
                        result={result}
                        extractedFile={extractedFile}
                        message={message}
                      />
                    </TabsContent>
                  </Tabs>

                  <ProcessButton
                    processing={processing}
                    progress={progress}
                    activeTab={activeTab}
                    handleProcess={handleProcess}
                    disabled={
                      !selectedFile ||
                      !password ||
                      !steganographyMethod ||
                      (activeTab === "encrypt" &&
                        secretInputType === "text" &&
                        !message) ||
                      (activeTab === "encrypt" &&
                        secretInputType === "file" &&
                        !secretFile)
                    }
                    secretInputType={secretInputType}
                  />

                  <ResultDisplay
                    result={result}
                    activeTab={activeTab}
                    downloadFile={downloadFile}
                  />
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <AlgorithmSettings
                activeTab={activeTab}
                encryptionLayers={encryptionLayers}
                addEncryptionLayer={addEncryptionLayer}
                updateEncryptionLayer={updateEncryptionLayer}
                removeEncryptionLayer={removeEncryptionLayer}
                encryptionAlgorithms={encryptionAlgorithms}
                hashMethod={hashMethod}
                setHashMethod={setHashMethod}
                hashMethods={hashMethods}
                steganographyMethod={steganographyMethod}
                setSteganographyMethod={setSteganographyMethod}
                steganographyTechniques={steganographyTechniques}
                selectedFile={selectedFile}
              />
              <SecurityStatus
                activeTab={activeTab}
                encryptionLayers={encryptionLayers}
                hashMethod={hashMethod}
                hashMethods={hashMethods}
                steganographyMethod={steganographyMethod}
              />
              <SessionStats
                activeTab={activeTab}
                encryptionLayers={encryptionLayers}
              />
            </div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}
