"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowRight } from "lucide-react"

interface LandingPageProps {
  onGenerateReadme: (url: string) => void
}

export default function LandingPage({ onGenerateReadme }: LandingPageProps) {
  const [repoUrl, setRepoUrl] = useState("")
  const [typewriterText, setTypewriterText] = useState("")
  const fullText = "🧠 Paste a GitHub link. ✍️ Get a README. 🚀 Instantly."

  useEffect(() => {
    let index = 0
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypewriterText(fullText.slice(0, index))
        index++
      } else {
        clearInterval(timer)
      }
    }, 50)

    return () => clearInterval(timer)
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (repoUrl.trim()) {
      onGenerateReadme(repoUrl.trim())
    }
  }

  const isValidGitHubUrl = (url: string) => {
    return url.includes("github.com") && url.includes("/")
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
            <span className="bg-gradient-to-r from-white via-gray-200 to-white bg-clip-text text-transparent">
              <span 
                dangerouslySetInnerHTML={{ 
                  __html: typewriterText
                    .replace('🧠', '<span style="color: #ec4899; text-shadow: 0 0 10px rgba(236, 72, 153, 0.5);">🧠</span>')
                    .replace('✍️', '<span style="color: #fbbf24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.5);">✍️</span>')
                    .replace('🚀', '<span style="color: #3b82f6; text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);">🚀</span>')
                }} 
              />
              <span className="animate-pulse">|</span>
            </span>
          </h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 2, duration: 0.8 }}
            className="text-xl md:text-2xl text-gray-400 mb-12"
          >
            Created with LangGraph agents. Powered by Gemini AI.
          </motion.p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.5, duration: 0.8 }}
          onSubmit={handleSubmit}
          className="max-w-2xl mx-auto"
        >
          <div className="flex flex-col md:flex-row gap-4 p-2 rounded-2xl bg-gradient-to-r from-gray-900/50 to-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <Input
              type="url"
              placeholder="GitHub repository URL"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              className="flex-1 bg-transparent border-none text-white placeholder-gray-400 text-lg focus:ring-2 focus:ring-[#04a777] focus:outline-none"
              required
            />
            <Button
              type="submit"
              disabled={!isValidGitHubUrl(repoUrl)}
              className="px-8 py-3 bg-gradient-to-r from-[#04a777] to-[#00d4aa] hover:from-[#059669] hover:to-[#04a777] text-white font-semibold rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-[#04a777]/25 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              Generate README
            </Button>
          </div>
        </motion.form>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 3, duration: 0.8 }}
          className="mt-12 text-gray-500 text-sm"
        >
          <p>✨ Powered by AI • 🚀 Instant generation • 📝 Professional quality</p>
        </motion.div>
        </div>
      </div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="mt-48 max-w-6xl mx-auto px-4"
      >
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Powered by <span className="text-[#04a777]">AI Intelligence</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Advanced LangGraph agents analyze your code, understand dependencies, and craft perfect documentation
          </p>
        </div>

                 <div className="flex flex-col md:flex-row gap-12 md:gap-16">
          {[
            {
              icon: "🤖",
              title: "Multi-Agent Analysis",
              description: "5 specialized AI agents work together to understand your codebase structure, dependencies, and purpose"
            },
            {
              icon: "⚡",
              title: "Lightning Fast",
              description: "Generate comprehensive README files in seconds, not hours of manual writing"
            },
            {
              icon: "🎯",
              title: "Smart & Accurate",
              description: "AI reads your code, package.json, and project structure to create relevant documentation"
            }
          ].map((feature, index) => (
                         <motion.div
               key={index}
               initial={{ opacity: 0, y: 30 }}
               whileInView={{ opacity: 1, y: 0 }}
               whileHover={{ 
                 scale: 1.05,
                 y: -10,
               }}
               transition={{ duration: 0.6, delay: index * 0.2 }}
               viewport={{ once: true }}
               className="bg-gradient-to-br from-gray-900/30 to-gray-800/30 backdrop-blur-sm border border-gray-700/30 rounded-2xl p-8 hover:border-[#04a777] hover:shadow-2xl hover:shadow-[#04a777]/20 transition-all duration-500 group relative overflow-hidden flex-1 min-w-[280px] md:min-w-0"
             >
                             {/* Glowing background effect */}
               <div className="absolute inset-0 bg-gradient-to-r from-[#04a777]/0 via-[#04a777]/10 to-[#00d4aa]/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl" />
               
               <div className="relative z-10">
                 <div className="text-5xl mb-6 text-center group-hover:scale-110 transition-transform duration-300">{feature.icon}</div>
                 <h3 className="text-xl font-semibold text-white mb-4 text-center group-hover:text-[#04a777] transition-colors duration-300">{feature.title}</h3>
                 <p className="text-gray-400 text-center leading-relaxed group-hover:text-gray-300 transition-colors duration-300">{feature.description}</p>
               </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* How It Works Section */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="mt-56 max-w-6xl mx-auto px-4"
      >
        <div className="text-center mb-20">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            How It <span className="text-[#04a777]">Works</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            From GitHub link to professional README in 4 simple steps
          </p>
        </div>

                 <div className="space-y-32">
          {[
            {
              step: "01",
              title: "Paste GitHub URL",
              description: "Simply paste your GitHub repository URL into our smart input field. Our system will validate and prepare for analysis.",
              icon: "🔗",
              details: ["Public or private repos", "Automatic validation", "Instant preview"]
            },
            {
              step: "02", 
              title: "AI Agent Analysis",
              description: "Watch as 3 specialized AI agents analyze your code structure, dependencies, documentation, and project purpose in real-time.",
              icon: "🧠",
              details: ["Code structure analysis", "Dependency extraction", "Purpose understanding"]
            },
            {
              step: "03",
              title: "README Generation",
              description: "Our AI writes a comprehensive, professional README with installation steps, usage examples, and proper formatting.",
              icon: "📝",
              details: ["Professional formatting", "Installation guides", "Usage examples"]
            },
            {
              step: "04",
              title: "Edit & Export",
              description: "Use our built-in markdown editor to customize your README, then copy to clipboard or download as .md file.",
              icon: "✨",
              details: ["Live markdown editor", "Real-time preview", "Copy or download"]
            }
          ].map((step, index) => (
                         <motion.div
               key={index}
               initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
               whileInView={{ opacity: 1, x: 0 }}
               whileHover={{ scale: 1.03 }}
               transition={{ duration: 0.8, delay: 0.2 }}
               viewport={{ once: true }}
               className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-12 p-6 rounded-3xl border border-gray-700/20 hover:border-[#04a777]/50 hover:shadow-2xl hover:shadow-[#04a777]/10 transition-all duration-500 group relative overflow-hidden max-w-[90%] mx-auto`}
             >
                             {/* Glowing background effect for steps */}
               <div className="absolute inset-0 bg-gradient-to-r from-[#04a777]/0 via-[#04a777]/5 to-[#00d4aa]/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl" />
               
               {/* Content */}
               <div className="flex-1 space-y-8 relative z-10">
                <div className="flex items-center gap-4">
                                     <div className="w-16 h-16 bg-gradient-to-r from-[#04a777] to-[#00d4aa] rounded-2xl flex items-center justify-center text-2xl font-bold text-white group-hover:scale-110 group-hover:shadow-lg group-hover:shadow-[#04a777]/30 transition-all duration-300">
                     {step.step}
                   </div>
                   <div>
                     <h3 className="text-2xl md:text-3xl font-bold text-white group-hover:text-[#04a777] transition-colors duration-300">{step.title}</h3>
                   </div>
                </div>
                
                                 <p className="text-lg text-gray-400 leading-relaxed max-w-lg group-hover:text-gray-300 transition-colors duration-300">
                   {step.description}
                 </p>

                <div className="flex flex-wrap gap-2">
                  {step.details.map((detail, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-gray-800/50 border border-gray-700/50 rounded-full text-sm text-gray-300"
                    >
                      {detail}
                    </span>
                  ))}
                </div>
              </div>

                             {/* Visual */}
               <div className="flex-1 flex justify-center relative z-10">
                <motion.div
                  whileHover={{ scale: 1.05, rotate: 5 }}
                  transition={{ duration: 0.3 }}
                  className="w-64 h-64 bg-gradient-to-br from-gray-900/80 to-gray-800/80 backdrop-blur-sm border border-gray-700/50 rounded-3xl flex items-center justify-center relative overflow-hidden group"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-[#04a777]/10 to-[#00d4aa]/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                   {index === 0 && (
                     <svg className="w-full h-full p-4" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                       <rect x="20" y="20" width="160" height="40" rx="8" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <text x="100" y="45" textAnchor="middle" fill="#9CA3AF" fontSize="14">github.com/username/repo</text>
                       <path d="M40 80 L160 80" stroke="#4B5563" strokeWidth="2" strokeDasharray="4 4"/>
                       <circle cx="100" cy="100" r="30" fill="#04a777" fillOpacity="0.2" stroke="#04a777" strokeWidth="2"/>
                       <path d="M85 100 L95 110 L115 90" stroke="#04a777" strokeWidth="2"/>
                     </svg>
                   )}
                   {index === 1 && (
                     <svg className="w-full h-full p-4" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                       <circle cx="50" cy="50" r="20" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <circle cx="100" cy="50" r="20" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <circle cx="150" cy="50" r="20" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M50 70 L50 130" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M100 70 L100 130" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M150 70 L150 130" stroke="#4B5563" strokeWidth="2"/>
                       <rect x="30" y="130" width="140" height="40" rx="8" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <text x="100" y="155" textAnchor="middle" fill="#9CA3AF" fontSize="12">Analyzing Codebase</text>
                     </svg>
                   )}
                   {index === 2 && (
                     <svg className="w-full h-full p-4" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                       <rect x="20" y="20" width="160" height="120" rx="8" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <line x1="40" y1="40" x2="160" y2="40" stroke="#4B5563" strokeWidth="2"/>
                       <line x1="40" y1="60" x2="140" y2="60" stroke="#4B5563" strokeWidth="2"/>
                       <line x1="40" y1="80" x2="120" y2="80" stroke="#4B5563" strokeWidth="2"/>
                       <line x1="40" y1="100" x2="100" y2="100" stroke="#4B5563" strokeWidth="2"/>
                       <circle cx="170" cy="100" r="10" fill="#04a777" fillOpacity="0.2" stroke="#04a777" strokeWidth="2"/>
                       <path d="M165 100 L170 105 L175 95" stroke="#04a777" strokeWidth="2"/>
                     </svg>
                   )}
                   {index === 3 && (
                     <svg className="w-full h-full p-4" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                       <rect x="20" y="20" width="160" height="120" rx="8" fill="#1F2937" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M40 50 L160 50" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M40 80 L160 80" stroke="#4B5563" strokeWidth="2"/>
                       <path d="M40 110 L160 110" stroke="#4B5563" strokeWidth="2"/>
                       <rect x="140" y="140" width="40" height="20" rx="4" fill="#04a777" fillOpacity="0.2" stroke="#04a777" strokeWidth="2"/>
                       <text x="160" y="155" textAnchor="middle" fill="#04a777" fontSize="12">Export</text>
                     </svg>
                   )}
                </motion.div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Call to Action */}
    </div>
  )
}
