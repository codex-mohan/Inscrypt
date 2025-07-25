"use client"

import { motion, useTransform, type MotionValue } from "framer-motion"
import { FaShieldAlt, FaLock } from "react-icons/fa"

interface ParallaxElementsProps {
  scrollYProgress: MotionValue<number>
}

export function ParallaxElements({ scrollYProgress }: ParallaxElementsProps) {
  // Side parallax effects
  const leftSideX = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], ["-100%", "0%", "0%", "100%"])
  const rightSideX = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], ["100%", "0%", "0%", "-100%"])
  const leftSideX2 = useTransform(scrollYProgress, [0, 0.4, 0.8, 1], ["-150%", "0%", "0%", "150%"])
  const rightSideX2 = useTransform(scrollYProgress, [0, 0.4, 0.8, 1], ["150%", "0%", "0%", "-150%"])

  // Floating elements parallax
  const floatingLeft = useTransform(scrollYProgress, [0, 1], ["-50px", "50px"])
  const floatingRight = useTransform(scrollYProgress, [0, 1], ["50px", "-50px"])
  const rotateLeft = useTransform(scrollYProgress, [0, 1], [0, 360])
  const rotateRight = useTransform(scrollYProgress, [0, 1], [360, 0])

  return (
    <>
      {/* Parallax Side Elements */}
      <div className="fixed inset-0 z-40 pointer-events-none overflow-hidden">
        {/* Left Side Elements */}
        <motion.div className="absolute left-0 top-1/4 w-32 h-32" style={{ x: leftSideX, rotate: rotateLeft }}>
          <div className="w-full h-full bg-gradient-to-r from-cyan-400/20 to-transparent rounded-full blur-xl" />
        </motion.div>

        <motion.div className="absolute left-0 top-1/2 w-24 h-24" style={{ x: leftSideX2 }}>
          <div className="w-full h-full border-2 border-cyan-400/30 rounded-lg rotate-45 backdrop-blur-sm" />
        </motion.div>

        <motion.div className="absolute left-0 top-3/4 w-16 h-16" style={{ x: leftSideX, y: floatingLeft }}>
          <FaShieldAlt className="w-full h-full text-cyan-400/40" />
        </motion.div>

        {/* Right Side Elements */}
        <motion.div className="absolute right-0 top-1/3 w-28 h-28" style={{ x: rightSideX, rotate: rotateRight }}>
          <div className="w-full h-full bg-gradient-to-l from-blue-400/20 to-transparent rounded-full blur-xl" />
        </motion.div>

        <motion.div className="absolute right-0 top-1/2 w-20 h-20" style={{ x: rightSideX2 }}>
          <div className="w-full h-full border-2 border-blue-400/30 rounded-full backdrop-blur-sm" />
        </motion.div>

        <motion.div className="absolute right-0 top-2/3 w-12 h-12" style={{ x: rightSideX, y: floatingRight }}>
          <FaLock className="w-full h-full text-blue-400/40" />
        </motion.div>
      </div>

      {/* Enhanced Light Trails - Much More Visible */}
      <div className="fixed inset-0 z-30 pointer-events-none overflow-hidden">
        {/* Layer 1 - Primary light streaks with higher opacity */}
        <motion.div
          className="absolute left-0 top-1/5 w-96 h-3"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["-100%", "20%"]),
            opacity: useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 0.8, 0.8, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-r from-transparent via-cyan-400/60 to-transparent blur-sm" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-4/5 w-96 h-3"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["100%", "-20%"]),
            opacity: useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 0.8, 0.8, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-l from-transparent via-blue-400/60 to-transparent blur-sm" />
        </motion.div>

        {/* Layer 2 - Secondary light beams with medium opacity */}
        <motion.div
          className="absolute left-0 top-2/5 w-72 h-2"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["-150%", "50%"]),
            opacity: useTransform(scrollYProgress, [0.1, 0.3, 0.7, 0.9], [0, 0.7, 0.7, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-r from-transparent via-cyan-300/70 to-transparent" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-3/5 w-72 h-2"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["150%", "-50%"]),
            opacity: useTransform(scrollYProgress, [0.1, 0.3, 0.7, 0.9], [0, 0.7, 0.7, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-l from-transparent via-blue-300/70 to-transparent" />
        </motion.div>

        {/* Layer 3 - Fast moving bright streaks */}
        <motion.div
          className="absolute left-0 top-1/2 w-48 h-1.5"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["-200%", "100%"]),
            opacity: useTransform(scrollYProgress, [0.05, 0.25, 0.75, 0.95], [0, 0.9, 0.9, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-r from-transparent via-cyan-200/80 to-transparent" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-1/2 w-48 h-1.5"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["200%", "-100%"]),
            opacity: useTransform(scrollYProgress, [0.05, 0.25, 0.75, 0.95], [0, 0.9, 0.9, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-l from-transparent via-blue-200/80 to-transparent" />
        </motion.div>

        {/* Additional Layer 4 - Extra bright accent streaks */}
        <motion.div
          className="absolute left-0 top-1/6 w-80 h-4"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["-120%", "30%"]),
            opacity: useTransform(scrollYProgress, [0.15, 0.35, 0.65, 0.85], [0, 0.6, 0.6, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent blur-md" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-5/6 w-80 h-4"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["120%", "-30%"]),
            opacity: useTransform(scrollYProgress, [0.15, 0.35, 0.65, 0.85], [0, 0.6, 0.6, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-l from-transparent via-blue-500/50 to-transparent blur-md" />
        </motion.div>

        {/* Layer 5 - Ultra-fast thin bright lines */}
        <motion.div
          className="absolute left-0 top-3/8 w-32 h-1"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["-250%", "150%"]),
            opacity: useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-r from-transparent via-cyan-100 to-transparent" />
        </motion.div>

        <motion.div
          className="absolute right-0 top-5/8 w-32 h-1"
          style={{
            x: useTransform(scrollYProgress, [0, 1], ["250%", "-150%"]),
            opacity: useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]),
          }}
        >
          <div className="w-full h-full bg-gradient-to-l from-transparent via-blue-100 to-transparent" />
        </motion.div>
      </div>
    </>
  )
}
