"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { FaRocket, FaEye } from "react-icons/fa"
import Link from "next/link"

export function CTASection() {
  return (
    <section className="relative z-10 py-32 px-6 bg-gradient-to-r from-cyan-900/20 to-blue-900/20">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-bold mb-8 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Ready to Secure Your Data?
          </h2>
          <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
            Join the next generation of digital privacy with Inscrypt's advanced steganographic platform.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link href="/app">
              <Button
                size="lg"
                className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 px-12 py-4 text-lg"
              >
                <FaRocket className="mr-2" />
                Launch App
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 px-12 py-4 text-lg bg-transparent"
            >
              <FaEye className="mr-2" />
              View Demo
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
