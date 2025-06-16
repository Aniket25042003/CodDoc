"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import LandingPage from "@/components/landing-page"
import AgentLoadingPanel from "@/components/agent-loading-panel"
import ReadmeDisplay from "@/components/readme-display"
import ParticleBackground from "@/components/particle-background"

export default function CodDoc() {
  const [currentView, setCurrentView] = useState<"landing" | "loading" | "readme">("landing")
  const [repoUrl, setRepoUrl] = useState("")
  const [generatedReadme, setGeneratedReadme] = useState("")
  const [generationLog, setGenerationLog] = useState<string[]>([])
  const [threadId, setThreadId] = useState<string | null>(null)

  const handleGenerateReadme = async (url: string) => {
    setRepoUrl(url)
    setCurrentView("loading")

    try {
      const response = await fetch("/api/generate-readme", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ repo_url: url }),
      })

      if (response.ok) {
        const data = await response.json()
        setGeneratedReadme(data.readme)
        setGenerationLog(data.log || [])
        setThreadId(data.thread_id)
        console.log("Generation completed:", { 
          log: data.log, 
          decisions: data.decisions,
          thread_id: data.thread_id 
        })
      } else {
        // Fallback demo content
        setGeneratedReadme(`# ${url.split("/").pop() || "Repository"}

## 🚀 Project Description

This is an AI-generated README for your repository. The content has been crafted by LangGraph agents powered by Gemini AI.

## ✨ Features

- Modern architecture
- Clean codebase
- Well-documented
- Easy to use

## 🛠️ Installation

\`\`\`bash
git clone ${url}
cd ${url.split("/").pop() || "repository"}
npm install
\`\`\`

## 📖 Usage

Follow the installation steps above and then run:

\`\`\`bash
npm start
\`\`\`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.`)
      }
    } catch (error) {
      console.error("Error generating README:", error)
      setGeneratedReadme("# Error\n\nFailed to generate README. Please try again.")
    }

    // Show loading for at least 3 seconds for better UX
    setTimeout(() => {
      setCurrentView("readme")
    }, 3000)
  }

  const handleBackToLanding = () => {
    setCurrentView("landing")
    setRepoUrl("")
    setGeneratedReadme("")
    setGenerationLog([])
    setThreadId(null)
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      <ParticleBackground />

      <div className="relative z-10">
        <AnimatePresence mode="wait">
          {currentView === "landing" && (
            <motion.div
              key="landing"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
            >
              <LandingPage onGenerateReadme={handleGenerateReadme} />
            </motion.div>
          )}

          {currentView === "loading" && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
            >
              <AgentLoadingPanel repoUrl={repoUrl} logs={generationLog} />
            </motion.div>
          )}

          {currentView === "readme" && (
            <motion.div
              key="readme"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <ReadmeDisplay readme={generatedReadme} repoUrl={repoUrl} onBack={handleBackToLanding} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
