"use client"

import { FaShieldAlt } from "react-icons/fa"

export function Footer() {
  return (
    <footer className="relative z-10 py-12 px-6 border-t border-gray-800/50 bg-black/40 backdrop-blur-md">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-3 mb-4 md:mb-0">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
              <FaShieldAlt className="text-white text-sm" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Inscrypt
            </span>
          </div>
          <div className="text-gray-400 text-sm">© 2025 Inscrypt. Advanced Steganography Platform.</div>
        </div>
      </div>
    </footer>
  )
}
