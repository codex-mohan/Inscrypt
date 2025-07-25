"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { FaShieldAlt, FaGithub, FaRocket } from "react-icons/fa"
import Link from "next/link"

export function Header() {
  return (
    <motion.header
      className="relative z-50 p-6 backdrop-blur-md bg-black/20 border-b border-cyan-500/20"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <motion.div className="flex items-center space-x-3" whileHover={{ scale: 1.05 }}>
          <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
            <FaShieldAlt className="text-white text-xl" />
          </div>
          <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Inscrypt
          </span>
        </motion.div>

        <nav className="hidden md:flex space-x-8">
          {["Features", "Technology", "Use Cases", "Security", "Docs"].map((item, index) => (
            <motion.a
              key={item}
              href={`#${item.toLowerCase().replace(" ", "-")}`}
              className="text-gray-300 hover:text-cyan-400 transition-colors"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 + 0.5 }}
              whileHover={{ scale: 1.1 }}
            >
              {item}
            </motion.a>
          ))}
        </nav>

        <motion.div
          className="flex space-x-4"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.8 }}
        >
          <Button variant="ghost" size="icon" className="text-cyan-400 hover:bg-cyan-400/10">
            <FaGithub />
          </Button>
          <Link href="/app">
            <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700">
              <FaRocket className="mr-2" />
              Launch App
            </Button>
          </Link>
        </motion.div>
      </div>
    </motion.header>
  )
}
