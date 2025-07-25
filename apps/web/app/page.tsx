"use client"

import { motion, useScroll, useTransform } from "framer-motion"
import { useRef } from "react"
import { Header } from "@/components/sections/header"
import { HeroSection } from "@/components/sections/hero-section"
import { FeaturesSection } from "@/components/sections/features-section"
import { TechnologySection } from "@/components/sections/technology-section"
import { MultilayerSection } from "@/components/sections/multilayer-section"
import { CTASection } from "@/components/sections/cta-section"
import { Footer } from "@/components/sections/footer"
import { ParallaxElements } from "@/components/parallax/parallax-elements"
import { UseCasesSection } from "@/components/sections/use-cases-section"

export default function InscryptLanding() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  })

  // Hero parallax effects
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"])
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])

  return (
    <div ref={containerRef} className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/20 via-black to-blue-900/20" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(6,182,212,0.1),transparent_50%)]" />
        <motion.div
          className="absolute inset-0 opacity-30"
          animate={{
            background: [
              "radial-gradient(circle at 20% 80%, rgba(6,182,212,0.1) 0%, transparent 50%)",
              "radial-gradient(circle at 80% 20%, rgba(6,182,212,0.1) 0%, transparent 50%)",
              "radial-gradient(circle at 40% 40%, rgba(6,182,212,0.1) 0%, transparent 50%)",
            ],
          }}
          transition={{ duration: 8, repeat: Number.POSITIVE_INFINITY, repeatType: "reverse" }}
        />
      </div>

      {/* Parallax Elements */}
      <ParallaxElements scrollYProgress={scrollYProgress} />

      {/* Page Sections */}
      <Header />
      <HeroSection y={y} opacity={opacity} />
      <FeaturesSection />
      <TechnologySection />
      <UseCasesSection />
      <MultilayerSection />
      <CTASection />
      <Footer />
    </div>
  )
}
