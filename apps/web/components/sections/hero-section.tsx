"use client"

import { motion, type MotionValue } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { FaRocket } from "react-icons/fa"
import Link from "next/link"

interface HeroSectionProps {
  y: MotionValue<string>
  opacity: MotionValue<number>
}

export function HeroSection({ y, opacity }: HeroSectionProps) {
  return (
    <section className="relative z-10 min-h-screen flex items-center justify-center px-6 overflow-hidden">
      {/* Grid Background - Increased thickness */}
      <div className="absolute inset-0 opacity-20">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(6,182,212,0.15) 2px, transparent 2px),
              linear-gradient(90deg, rgba(6,182,212,0.15) 2px, transparent 2px)
            `,
            backgroundSize: "50px 50px",
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(6,182,212,0.08) 1px, transparent 1px),
              linear-gradient(90deg, rgba(6,182,212,0.08) 1px, transparent 1px)
            `,
            backgroundSize: "10px 10px",
          }}
        />
      </div>

      {/* Particle System */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={`particle-${i}`}
            className="absolute w-1 h-1 bg-cyan-400 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [-20, -40, -20],
              x: [-10, 10, -10],
              opacity: [0.2, 1, 0.2],
              scale: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 4 + Math.random() * 4,
              repeat: Number.POSITIVE_INFINITY,
              delay: Math.random() * 2,
              ease: "easeInOut",
            }}
          />
        ))}

        {[...Array(15)].map((_, i) => (
          <motion.div
            key={`particle-large-${i}`}
            className="absolute w-2 h-2 bg-blue-400/60 rounded-full blur-sm"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [-30, 30, -30],
              x: [-15, 15, -15],
              opacity: [0.1, 0.6, 0.1],
            }}
            transition={{
              duration: 6 + Math.random() * 3,
              repeat: Number.POSITIVE_INFINITY,
              delay: Math.random() * 3,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>

      <motion.div className="max-w-6xl mx-auto text-center relative z-10" style={{ y, opacity }}>
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1, delay: 0.2 }}
        >
          <Badge className="mb-6 bg-cyan-500/10 text-cyan-400 border-cyan-500/20 px-4 py-2">
            Advanced Steganography Platform
          </Badge>
        </motion.div>

        <motion.h1
          className="text-6xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent"
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
        >
          Hide in Plain Sight
        </motion.h1>

        <motion.p
          className="text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.6 }}
        >
          Encrypt and embed secret messages within images, videos, and audio files using military-grade encryption and
          advanced steganographic techniques.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-6 justify-center items-center"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.8 }}
        >
          <Link href="/app">
            <Button
              size="lg"
              className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 px-8 py-4 text-lg"
            >
              <FaRocket className="mr-2" />
              Get Started
            </Button>
          </Link>
          <Button
            size="lg"
            variant="outline"
            className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 px-8 py-4 text-lg bg-transparent"
          >
            View Demo
          </Button>
        </motion.div>

        {/* Enhanced Floating Elements */}
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full"
              style={{
                left: `${15 + i * 12}%`,
                top: `${25 + (i % 3) * 25}%`,
              }}
              animate={{
                y: [-25, 25, -25],
                opacity: [0.2, 1, 0.2],
                scale: [0.8, 1.2, 0.8],
              }}
              transition={{
                duration: 4 + i * 0.3,
                repeat: Number.POSITIVE_INFINITY,
                delay: i * 0.3,
              }}
            />
          ))}
        </div>
      </motion.div>
    </section>
  )
}
