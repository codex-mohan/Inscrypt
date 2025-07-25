"use client"

import { motion, useScroll, useTransform } from "framer-motion"
import { useRef } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { FaLock, FaImage, FaVideo, FaMusic, FaEye, FaKey, FaShieldAlt } from "react-icons/fa"

const features = [
  {
    icon: FaLock,
    title: "Advanced Encryption",
    description: "Support for AES, DES, ChaCha20, Blowfish, and 15+ encryption algorithms with multi-layer protection",
    gradient: "from-cyan-400 to-blue-600",
  },
  {
    icon: FaImage,
    title: "Image Steganography",
    description: "Hide encrypted messages within PNG, JPEG, and other image formats using LSB and advanced techniques",
    gradient: "from-blue-400 to-purple-600",
  },
  {
    icon: FaVideo,
    title: "Video Embedding",
    description: "Conceal data within video frames and manipulate volume data for undetectable storage",
    gradient: "from-purple-400 to-pink-600",
  },
  {
    icon: FaMusic,
    title: "Audio Steganography",
    description: "Use Fourier transforms to hide messages in audio files while maintaining quality",
    gradient: "from-pink-400 to-red-600",
  },
  {
    icon: FaEye,
    title: "Undetectable",
    description: "Maximum robustness against detection with sophisticated obfuscation techniques",
    gradient: "from-red-400 to-orange-600",
  },
  {
    icon: FaKey,
    title: "Automated Keys",
    description: "Intelligent key generation and media preparation with minimal user input required",
    gradient: "from-orange-400 to-yellow-600",
  },
]

export function FeaturesSection() {
  const featuresRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress: featuresScrollY } = useScroll({
    target: featuresRef,
    offset: ["start end", "end start"],
  })

  const featuresLeftX = useTransform(featuresScrollY, [0, 0.5, 1], ["-100%", "0%", "100%"])
  const featuresRightX = useTransform(featuresScrollY, [0, 0.5, 1], ["100%", "0%", "-100%"])
  const featuresRotate = useTransform(featuresScrollY, [0, 1], [0, 180])
  const featuresScale = useTransform(featuresScrollY, [0, 0.5, 1], [0.8, 1, 0.8])

  return (
    <section ref={featuresRef} id="features" className="relative z-10 py-32 px-6 overflow-hidden">
      {/* Features Parallax Elements */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Left side elements */}
        <motion.div
          className="absolute left-0 top-1/4 w-40 h-40"
          style={{ x: featuresLeftX, rotate: featuresRotate, scale: featuresScale }}
        >
          <div className="w-full h-full bg-gradient-to-r from-cyan-400/10 to-transparent rounded-full blur-2xl" />
        </motion.div>

        <motion.div className="absolute left-0 top-3/4 w-24 h-24" style={{ x: featuresLeftX, rotate: featuresRotate }}>
          <FaShieldAlt className="w-full h-full text-cyan-400/20" />
        </motion.div>

        {/* Right side elements */}
        <motion.div
          className="absolute right-0 top-1/3 w-32 h-32"
          style={{ x: featuresRightX, rotate: featuresRotate, scale: featuresScale }}
        >
          <div className="w-full h-full bg-gradient-to-l from-blue-400/10 to-transparent rounded-full blur-2xl" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-2/3 w-20 h-20"
          style={{ x: featuresRightX, rotate: featuresRotate }}
        >
          <FaLock className="w-full h-full text-blue-400/20" />
        </motion.div>

        {/* Floating geometric shapes */}
        <motion.div
          className="absolute left-1/4 top-1/6 w-14 h-14"
          style={{ x: featuresLeftX, rotate: featuresRotate }}
        >
          <div className="w-full h-full border-2 border-cyan-400/20 rounded-lg backdrop-blur-sm" />
        </motion.div>

        <motion.div
          className="absolute right-1/4 top-5/6 w-14 h-14"
          style={{ x: featuresRightX, rotate: featuresRotate }}
        >
          <div className="w-full h-full border-2 border-blue-400/20 rounded-lg backdrop-blur-sm" />
        </motion.div>

        {/* Additional matching shapes for features */}
        <motion.div
          className="absolute left-1/6 top-1/2 w-10 h-10"
          style={{ x: featuresLeftX, rotate: featuresRotate, scale: featuresScale }}
        >
          <div className="w-full h-full bg-cyan-400/15 rounded-full" />
        </motion.div>

        <motion.div
          className="absolute right-1/6 top-1/2 w-10 h-10"
          style={{ x: featuresRightX, rotate: featuresRotate, scale: featuresScale }}
        >
          <div className="w-full h-full bg-blue-400/15 rounded-full" />
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Comprehensive steganographic capabilities with unmatched security and versatility
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -10, scale: 1.02 }}
            >
              <Card className="bg-black/40 backdrop-blur-md border-gray-800/50 hover:border-cyan-500/50 transition-all duration-300 h-full">
                <CardContent className="p-8">
                  <div
                    className={`w-16 h-16 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6`}
                  >
                    <feature.icon className="text-white text-2xl" />
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-white">{feature.title}</h3>
                  <p className="text-gray-300 leading-relaxed">{feature.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
