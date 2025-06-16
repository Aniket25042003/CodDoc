"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Copy, Download, ArrowLeft, Check } from "lucide-react"
import MarkdownEditor from "./markdown-editor"

interface ReadmeDisplayProps {
  readme: string
  repoUrl: string
  onBack: () => void
}

export default function ReadmeDisplay({ readme, repoUrl, onBack }: ReadmeDisplayProps) {
  const [copied, setCopied] = useState(false)
  const [editedMarkdown, setEditedMarkdown] = useState(readme)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(editedMarkdown)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy text: ", err)
    }
  }

  const handleDownload = () => {
    const watermark = "<!-- Created with CodDoc - AI-powered README generator -->\n\n"
    const content = watermark + editedMarkdown
    const blob = new Blob([content], { type: "text/markdown" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "README.md"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen px-4 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center justify-between mb-8"
        >
          <div className="flex items-center space-x-4">
            <Button
              onClick={onBack}
              variant="ghost"
              size="sm"
              className="text-gray-400 hover:text-white hover:bg-gray-800"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-white">CodDoc</h1>
              <p className="text-gray-400 text-sm">Generated for: {repoUrl.split("/").slice(-2).join("/")}</p>
            </div>
          </div>

          <div className="flex space-x-2">
            <Button
              onClick={handleCopy}
              variant="outline"
              size="sm"
              className="border-[#04a777] text-[#04a777] hover:bg-[#04a777] hover:text-white transition-colors"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  Copy README
                </>
              )}
            </Button>
            <Button
              onClick={handleDownload}
              variant="outline"
              size="sm"
              className="border-[#04a777] text-[#04a777] hover:bg-[#04a777] hover:text-white transition-colors"
            >
              <Download className="w-4 h-4 mr-2" />
              Download .md
            </Button>
          </div>
        </motion.div>

        {/* README Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Card className="bg-gray-900/50 border-gray-700/50 backdrop-blur-sm">
            <CardHeader className="border-b border-gray-700/50">
              <CardTitle className="text-white font-mono text-lg flex items-center">
                <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
                <span className="w-3 h-3 bg-green-500 rounded-full mr-4"></span>
                README.md
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <pre className="p-6 text-gray-300 font-mono text-sm leading-relaxed overflow-x-auto whitespace-pre-wrap">
                {readme}
              </pre>
            </CardContent>
          </Card>
        </motion.div>

        {/* Divider Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="mt-16 mb-8"
        >
          <div className="flex items-center justify-center">
            <div className="flex-grow h-px bg-gradient-to-r from-transparent via-gray-600 to-transparent"></div>
            <div className="px-6 text-gray-400 text-sm font-mono">
              ✨ Edit & Customize Your README
            </div>
            <div className="flex-grow h-px bg-gradient-to-r from-transparent via-gray-600 to-transparent"></div>
          </div>
        </motion.div>

        {/* Markdown Editor */}
        <MarkdownEditor 
          initialMarkdown={readme}
          onMarkdownChange={setEditedMarkdown}
        />

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="text-center mt-8 text-gray-500 text-sm"
        >
          <p>✨ Generated by CodDoc • Powered by LangGraph & Gemini AI</p>
        </motion.div>
      </div>
    </div>
  )
}
