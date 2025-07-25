"use client"

import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { FaShieldAlt, FaNewspaper, FaBuilding, FaUserSecret, FaGlobe, FaLock, FaEye, FaUsers } from "react-icons/fa"

const useCases = [
  {
    icon: FaShieldAlt,
    title: "Military Communications",
    sector: "Defense",
    description:
      "Secure field communications and intelligence sharing through covert channels embedded in routine media files",
    features: ["Battlefield communications", "Intelligence reports", "Operational security", "Chain of command"],
    gradient: "from-red-500 to-red-700",
    bgGradient: "from-red-500/10 to-red-700/5",
  },
  {
    icon: FaNewspaper,
    title: "Investigative Journalism",
    sector: "Media",
    description:
      "Protect sources and sensitive information while maintaining plausible deniability in hostile environments",
    features: ["Source protection", "Document security", "Whistleblower safety", "Evidence preservation"],
    gradient: "from-blue-500 to-blue-700",
    bgGradient: "from-blue-500/10 to-blue-700/5",
  },
  {
    icon: FaUserSecret,
    title: "Blue Team Operations",
    sector: "Cybersecurity",
    description: "Covert data exfiltration detection and secure internal communications for security operations",
    features: ["Threat hunting", "Incident response", "Secure coordination", "Evidence collection"],
    gradient: "from-cyan-500 to-cyan-700",
    bgGradient: "from-cyan-500/10 to-cyan-700/5",
  },
  {
    icon: FaBuilding,
    title: "Corporate Security",
    sector: "Business",
    description: "Protect trade secrets, financial data, and strategic communications from corporate espionage",
    features: ["IP protection", "Executive communications", "M&A confidentiality", "Compliance reporting"],
    gradient: "from-purple-500 to-purple-700",
    bgGradient: "from-purple-500/10 to-purple-700/5",
  },
  {
    icon: FaGlobe,
    title: "Diplomatic Communications",
    sector: "Government",
    description: "Secure diplomatic channels and international negotiations through undetectable communication methods",
    features: ["Embassy communications", "Treaty negotiations", "Intelligence sharing", "Crisis management"],
    gradient: "from-green-500 to-green-700",
    bgGradient: "from-green-500/10 to-green-700/5",
  },
  {
    icon: FaUsers,
    title: "Human Rights Organizations",
    sector: "NGO",
    description: "Protect activists and document human rights violations in oppressive regimes safely and securely",
    features: ["Activist protection", "Evidence documentation", "Safe communications", "Witness security"],
    gradient: "from-orange-500 to-orange-700",
    bgGradient: "from-orange-500/10 to-orange-700/5",
  },
]

const securityLevels = [
  { level: "CONFIDENTIAL", color: "text-yellow-400", bg: "bg-yellow-400/10" },
  { level: "SECRET", color: "text-orange-400", bg: "bg-orange-400/10" },
  { level: "TOP SECRET", color: "text-red-400", bg: "bg-red-400/10" },
]

export function UseCasesSection() {
  return (
    <section id="use-cases" className="relative z-10 py-32 px-6 bg-gradient-to-r from-gray-900/20 to-slate-900/20">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <motion.div
            className="flex justify-center mb-6"
            initial={{ scale: 0.8, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <Badge className="bg-gradient-to-r from-cyan-500/10 to-blue-500/10 text-cyan-400 border-cyan-500/20 px-6 py-2 text-sm">
              <FaLock className="mr-2" />
              Professional Applications
            </Badge>
          </motion.div>

          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Real-World Use Cases
          </h2>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto">
            Trusted by professionals across critical sectors where security and discretion are paramount
          </p>
        </motion.div>

        {/* Security Classification Levels */}
        <motion.div
          className="flex justify-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          viewport={{ once: true }}
        >
          <div className="flex space-x-6">
            {securityLevels.map((level, index) => (
              <motion.div
                key={level.level}
                className={`px-4 py-2 ${level.bg} border border-gray-700/50 rounded-lg backdrop-blur-sm`}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.1 + 0.5 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
              >
                <span className={`${level.color} font-mono text-sm font-bold`}>{level.level}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Use Cases Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {useCases.map((useCase, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -10, scale: 1.02 }}
            >
              <Card className="bg-black/40 backdrop-blur-md border-gray-800/50 hover:border-cyan-500/30 transition-all duration-300 h-full group">
                <CardContent className="p-8">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-6">
                    <div
                      className={`w-16 h-16 rounded-xl bg-gradient-to-r ${useCase.gradient} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}
                    >
                      <useCase.icon className="text-white text-2xl" />
                    </div>
                    <Badge
                      className={`bg-gradient-to-r ${useCase.bgGradient} border-gray-700/50 text-gray-300 text-xs`}
                    >
                      {useCase.sector}
                    </Badge>
                  </div>

                  {/* Content */}
                  <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-cyan-400 transition-colors">
                    {useCase.title}
                  </h3>
                  <p className="text-gray-300 leading-relaxed mb-6">{useCase.description}</p>

                  {/* Features */}
                  <div className="space-y-2">
                    <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">Key Applications</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {useCase.features.map((feature, featureIndex) => (
                        <motion.div
                          key={featureIndex}
                          className="flex items-center space-x-2"
                          initial={{ opacity: 0, x: -20 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.4, delay: index * 0.1 + featureIndex * 0.05 }}
                          viewport={{ once: true }}
                        >
                          <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full" />
                          <span className="text-gray-400 text-sm">{feature}</span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Statistics Section */}
        <motion.div
          className="grid md:grid-cols-3 gap-8 mb-16"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
        >
          {[
            { number: "99.9%", label: "Undetection Rate", icon: FaEye },
            { number: "256-bit", label: "Military-Grade Encryption", icon: FaLock },
            { number: "50+", label: "Supported File Formats", icon: FaGlobe },
          ].map((stat, index) => (
            <motion.div
              key={index}
              className="text-center p-8 bg-black/20 backdrop-blur-md border border-gray-800/50 rounded-2xl hover:border-cyan-500/30 transition-colors"
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: index * 0.1 + 0.6 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="w-16 h-16 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <stat.icon className="text-cyan-400 text-2xl" />
              </div>
              <div className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent mb-2">
                {stat.number}
              </div>
              <div className="text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Compliance Section */}
        <motion.div
          className="bg-gradient-to-r from-cyan-900/10 to-blue-900/10 rounded-3xl p-12 border border-gray-800/50"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          viewport={{ once: true }}
        >
          <div className="text-center mb-8">
            <h3 className="text-3xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Security Compliance
            </h3>
            <p className="text-gray-300 max-w-2xl mx-auto">
              Built to meet the highest security standards and compliance requirements across industries
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            {["FIPS 140-2", "Common Criteria", "ISO 27001", "NIST Framework"].map((standard, index) => (
              <motion.div
                key={standard}
                className="text-center p-6 bg-black/20 backdrop-blur-sm border border-gray-700/50 rounded-xl hover:border-cyan-500/30 transition-colors"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 + 0.8 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
              >
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <FaShieldAlt className="text-cyan-400" />
                </div>
                <span className="text-white font-semibold text-sm">{standard}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
