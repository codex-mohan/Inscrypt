"use client"

import { motion } from "framer-motion"
import { FaLayerGroup } from "react-icons/fa"

const multiLayerExamples = [
  { name: "AES", color: "from-cyan-400 to-cyan-600" },
  { name: "Blowfish", color: "from-blue-400 to-blue-600" },
  { name: "ChaCha20", color: "from-purple-400 to-purple-600" },
  { name: "DES3", color: "from-pink-400 to-pink-600" },
  { name: "Salsa20", color: "from-red-400 to-red-600" },
  { name: "CAST", color: "from-orange-400 to-orange-600" },
]

export function MultilayerSection() {
  return (
    <section className="relative z-10 py-32 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Multi-Layer Protection
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-12">
            Stack multiple encryption layers for ultimate security. Mix and match algorithms for maximum protection.
          </p>
        </motion.div>

        {/* Main Example */}
        <div className="flex justify-center mb-16">
          <motion.div
            className="relative"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1 }}
            viewport={{ once: true }}
          >
            <div className="flex items-center space-x-8">
              {multiLayerExamples.slice(0, 3).map((layer, index) => (
                <motion.div
                  key={layer.name}
                  className="relative"
                  initial={{ opacity: 0, x: -50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  viewport={{ once: true }}
                >
                  <div
                    className={`w-32 h-32 bg-gradient-to-r ${layer.color}/20 backdrop-blur-md border border-cyan-500/30 rounded-2xl flex items-center justify-center`}
                  >
                    <FaLayerGroup className="text-cyan-400 text-3xl" />
                  </div>
                  <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2">
                    <span className="text-cyan-400 font-bold">{layer.name}</span>
                  </div>
                  {index < 2 && (
                    <div className="absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <div className="w-8 h-0.5 bg-gradient-to-r from-cyan-400 to-blue-400"></div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Additional Examples Grid */}
        <motion.div
          className="grid md:grid-cols-2 gap-12"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          viewport={{ once: true }}
        >
          {/* Example 1 */}
          <div className="bg-black/20 backdrop-blur-md border border-gray-800/50 rounded-2xl p-8">
            <h3 className="text-2xl font-bold mb-6 text-cyan-400">Maximum Security Stack</h3>
            <div className="flex flex-wrap gap-3 mb-4">
              {["AES-256", "Blowfish", "ChaCha20", "Salsa20"].map((algo, index) => (
                <motion.div
                  key={algo}
                  className="px-4 py-2 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg border border-cyan-500/30"
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <span className="text-white font-mono text-sm">{algo}</span>
                </motion.div>
              ))}
            </div>
            <p className="text-gray-300 text-sm">
              Four-layer encryption with different algorithm families for maximum security
            </p>
          </div>

          {/* Example 2 */}
          <div className="bg-black/20 backdrop-blur-md border border-gray-800/50 rounded-2xl p-8">
            <h3 className="text-2xl font-bold mb-6 text-blue-400">Balanced Performance</h3>
            <div className="flex flex-wrap gap-3 mb-4">
              {["AES-128", "DES3", "CAST"].map((algo, index) => (
                <motion.div
                  key={algo}
                  className="px-4 py-2 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg border border-blue-500/30"
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <span className="text-white font-mono text-sm">{algo}</span>
                </motion.div>
              ))}
            </div>
            <p className="text-gray-300 text-sm">
              Three-layer setup optimized for speed while maintaining strong security
            </p>
          </div>
        </motion.div>

        {/* Algorithm Showcase */}
        <motion.div
          className="mt-16 text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          viewport={{ once: true }}
        >
          <h4 className="text-xl font-bold mb-8 text-gray-300">Available Encryption Algorithms</h4>
          <div className="flex flex-wrap justify-center gap-4">
            {multiLayerExamples.map((algo, index) => (
              <motion.div
                key={algo.name}
                className={`px-6 py-3 bg-gradient-to-r ${algo.color}/10 border border-gray-700/50 rounded-full hover:border-cyan-500/50 transition-colors cursor-pointer`}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05, y: -2 }}
              >
                <span className="text-white font-mono">{algo.name}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
