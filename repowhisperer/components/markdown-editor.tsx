"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Edit3, Eye, Copy, Download, Check } from "lucide-react"

interface MarkdownEditorProps {
  initialMarkdown: string
  onMarkdownChange?: (markdown: string) => void
}

export default function MarkdownEditor({ initialMarkdown, onMarkdownChange }: MarkdownEditorProps) {
  const [markdown, setMarkdown] = useState(initialMarkdown)
  const [copied, setCopied] = useState(false)

  const handleMarkdownChange = (value: string) => {
    setMarkdown(value)
    onMarkdownChange?.(value)
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(markdown)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy text: ", err)
    }
  }

  const handleDownload = () => {
    const watermark = "<!-- Created with CodDoc - AI-powered README generator -->\n\n"
    const content = watermark + markdown
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

  // Enhanced markdown to HTML converter for preview
  const markdownToHtml = (md: string) => {
    let html = md
    
    // Escape HTML
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    
    // Code blocks (must be processed before inline code) - enhanced to handle whitespace before closing ```
    html = html.replace(/```(\w+)?\n([\s\S]*?)\n\s*```/gm, (match, lang, code) => {
      const cleanCode = code.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
      return `<pre class="bg-gray-800 border border-gray-700 rounded-lg p-4 my-4 overflow-x-auto"><code class="text-sm text-gray-300 font-mono">${cleanCode}</code></pre>`
    })
    
    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-800 text-[#04a777] px-2 py-1 rounded text-sm font-mono">$1</code>')
    
    // Headers (process in order of specificity)
    html = html.replace(/^#### (.*$)/gm, '<h4 class="text-base font-semibold text-white mb-2 mt-3">$1</h4>')
    html = html.replace(/^### (.*$)/gm, '<h3 class="text-lg font-semibold text-white mb-2 mt-4">$1</h3>')
    html = html.replace(/^## (.*$)/gm, '<h2 class="text-xl font-bold text-white mb-3 mt-6 border-b border-gray-700 pb-2">$1</h2>')
    html = html.replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold text-white mb-4 mt-6 border-b-2 border-[#04a777] pb-3">$1</h1>')
    
    // Bold and italic (process bold first to avoid conflicts)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
    html = html.replace(/\*(.*?)\*/g, '<em class="italic text-gray-300">$1</em>')
    
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[#04a777] hover:text-[#059669] underline transition-colors" target="_blank" rel="noopener noreferrer">$1</a>')
    
    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr class="border-gray-700 my-6" />')
    
    // Lists - simplified approach without complex grouping
    // Convert unordered lists directly
    html = html.replace(/^(\s*)[-*+] (.+)$/gm, (match, indent, content) => {
      const indentLevel = Math.floor(indent.length / 2)
      const marginClass = indentLevel > 0 ? `ml-${indentLevel * 4}` : ''
      return `<div class="flex items-start ${marginClass} my-1"><span class="text-gray-400 mr-2">•</span><span class="text-gray-300">${content}</span></div>`
    })
    
    // Convert ordered lists directly
    html = html.replace(/^(\s*)(\d+)\. (.+)$/gm, (match, indent, num, content) => {
      const indentLevel = Math.floor(indent.length / 2)
      const marginClass = indentLevel > 0 ? `ml-${indentLevel * 4}` : ''
      return `<div class="flex items-start ${marginClass} my-1"><span class="text-gray-400 mr-2">${num}.</span><span class="text-gray-300">${content}</span></div>`
    })
    
    // Blockquotes
    html = html.replace(/^> (.+)$/gm, '<blockquote class="border-l-4 border-[#04a777] pl-4 italic text-gray-400 my-3">$1</blockquote>')
    
    // Tables (basic support)
    html = html.replace(/\|(.+)\|/g, (match, content) => {
      const cells = content.split('|').map((cell: string) => cell.trim())
      return '<tr>' + cells.map((cell: string) => `<td class="border border-gray-700 px-3 py-2 text-gray-300">${cell}</td>`).join('') + '</tr>'
    })
    
    // Paragraphs and line breaks
    html = html.replace(/\n\n/g, '</p><p class="text-gray-300 mb-4">')
    html = html.replace(/\n/g, '<br/>')
    
    // Wrap in paragraph tags
    html = '<div class="text-gray-300"><p class="text-gray-300 mb-4">' + html + '</p></div>'
    
    // Clean up empty paragraphs
    html = html.replace(/<p class="text-gray-300 mb-4"><\/p>/g, '')
    
    return html
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.6 }}
      className="mt-8"
    >
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-bold text-white flex items-center">
          <Edit3 className="w-5 h-5 mr-2 text-[#04a777]" />
          Markdown Editor
        </h2>
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
                Copy
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
            Download
          </Button>
        </div>
      </div>
      
      <p className="text-gray-400 text-sm mb-6 leading-relaxed">
        Edit the AI-generated README content below. Changes are reflected in real-time in the preview panel. 
        Use markdown syntax for formatting, and your edits will be included when copying or downloading.
      </p>

      {/* Desktop: Side-by-side layout */}
      <div className="hidden lg:flex gap-4">
        {/* Editor Panel */}
        <Card className="flex-1 w-1/2 bg-gray-900/50 border-gray-700/50 backdrop-blur-sm">
          <CardHeader className="border-b border-gray-700/50 pb-3">
            <CardTitle className="text-white font-mono text-sm flex items-center">
              <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
              <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
              <span className="w-3 h-3 bg-green-500 rounded-full mr-4"></span>
              <Edit3 className="w-4 h-4 mr-2" />
              Editor
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <textarea
              value={markdown}
              onChange={(e) => handleMarkdownChange(e.target.value)}
              className="w-full h-[600px] bg-transparent text-gray-300 font-mono text-sm leading-relaxed p-6 resize-none focus:outline-none focus:ring-2 focus:ring-[#04a777] border-none transition-all duration-200"
              placeholder="Edit your markdown here..."
              style={{ 
                fontFamily: 'JetBrains Mono, Fira Code, Monaco, Consolas, monospace',
                lineHeight: '1.5',
                tabSize: 2
              }}
              spellCheck={false}
            />
          </CardContent>
        </Card>

        {/* Preview Panel */}
        <Card className="flex-1 w-1/2 bg-gray-900/50 border-gray-700/50 backdrop-blur-sm">
          <CardHeader className="border-b border-gray-700/50 pb-3">
            <CardTitle className="text-white font-mono text-sm flex items-center">
              <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
              <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
              <span className="w-3 h-3 bg-green-500 rounded-full mr-4"></span>
              <Eye className="w-4 h-4 mr-2" />
              Preview
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div 
              className="h-[600px] overflow-y-auto prose prose-invert max-w-none transition-all duration-300 ease-in-out"
              dangerouslySetInnerHTML={{ __html: markdownToHtml(markdown) }}
              style={{
                scrollbarWidth: 'thin',
                scrollbarColor: '#04a777 #374151'
              }}
            />
          </CardContent>
        </Card>
      </div>

      {/* Mobile: Tabbed layout */}
      <div className="lg:hidden">
        <Tabs defaultValue="editor" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-gray-800 border border-gray-700">
            <TabsTrigger 
              value="editor" 
              className="text-gray-400 data-[state=active]:text-white data-[state=active]:bg-[#04a777]"
            >
              <Edit3 className="w-4 h-4 mr-2" />
              Editor
            </TabsTrigger>
            <TabsTrigger 
              value="preview"
              className="text-gray-400 data-[state=active]:text-white data-[state=active]:bg-[#04a777]"
            >
              <Eye className="w-4 h-4 mr-2" />
              Preview
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="editor" className="mt-4">
            <Card className="bg-gray-900/50 border-gray-700/50 backdrop-blur-sm">
              <CardHeader className="border-b border-gray-700/50 pb-3">
                <CardTitle className="text-white font-mono text-sm flex items-center">
                  <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-4"></span>
                  Editor
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <textarea
                  value={markdown}
                  onChange={(e) => handleMarkdownChange(e.target.value)}
                  className="w-full h-[500px] bg-transparent text-gray-300 font-mono text-sm leading-relaxed p-6 resize-none focus:outline-none focus:ring-2 focus:ring-[#04a777] border-none transition-all duration-200"
                  placeholder="Edit your markdown here..."
                  style={{ 
                    fontFamily: 'JetBrains Mono, Fira Code, Monaco, Consolas, monospace',
                    lineHeight: '1.5',
                    tabSize: 2
                  }}
                  spellCheck={false}
                />
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="preview" className="mt-4">
            <Card className="bg-gray-900/50 border-gray-700/50 backdrop-blur-sm">
              <CardHeader className="border-b border-gray-700/50 pb-3">
                <CardTitle className="text-white font-mono text-sm flex items-center">
                  <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-4"></span>
                  Preview
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div 
                  className="h-[500px] overflow-y-auto prose prose-invert max-w-none transition-all duration-300 ease-in-out"
                  dangerouslySetInnerHTML={{ __html: markdownToHtml(markdown) }}
                  style={{
                    scrollbarWidth: 'thin',
                    scrollbarColor: '#04a777 #374151'
                  }}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </motion.div>
  )
} 