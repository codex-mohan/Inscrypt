"use client"

import { motion } from "framer-motion"

const algorithms = [
  "AES",
  "DES",
  "DES3",
  "ChaCha20",
  "Blowfish",
  "ARC2",
  "ARC4",
  "Salsa20",
  "CAST",
  "PKCS1_OAEP",
  "PKCS1_v1_5",
  "XOR",
]

const hashMethods = [
  "SHA256",
  "SHA512",
  "SHA3_256",
  "Keccak",
  "Blake",
  "Whirlpool",
  "SHAKE256",
  "TupleHash",
  "KangarooTwelve",
]

export function TechnologySection() {
  return (
    <section id="technology" className="relative z-10 py-32 px-6 bg-gradient-to-r from-cyan-900/10 to-blue-900/10">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Advanced Technology Stack
          </h2>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-16">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h3 className="text-3xl font-bold mb-8 text-cyan-400">Encryption Algorithms</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {algorithms.map((algo, index) => (
                <motion.div
                  key={algo}
                  className="bg-black/40 backdrop-blur-md border border-gray-800/50 rounded-lg p-4 text-center hover:border-cyan-500/50 transition-colors"
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.05 }}
                >
                  <span className="text-white font-mono">{algo}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h3 className="text-3xl font-bold mb-8 text-blue-400">Hash Methods</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {hashMethods.map((hash, index) => (
                <motion.div
                  key={hash}
                  className="bg-black/40 backdrop-blur-md border border-gray-800/50 rounded-lg p-4 text-center hover:border-blue-500/50 transition-colors"
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.05 }}
                >
                  <span className="text-white font-mono">{hash}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
