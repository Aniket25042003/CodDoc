"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"

interface AgentLoadingPanelProps {
  repoUrl: string
  logs?: string[]
}

export default function AgentLoadingPanel({ repoUrl, logs = [] }: AgentLoadingPanelProps) {
  const [currentMessage, setCurrentMessage] = useState(0)

  const defaultMessages = [
    "🧠 Agents are analyzing your repo...",
    "📊 Processing repository structure...",
    "🔍 Extracting key information...",
    "📝 Writing your README...",
    "✨ Adding final touches...",
  ]

  // Use backend logs if available, otherwise use default messages
  const messages = logs.length > 0 ? logs.map(log => `📋 ${log}`) : defaultMessages

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMessage((prev) => (prev + 1) % messages.length)
    }, 600)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-2xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-white">CodDoc</h2>
          <p className="text-gray-400 text-lg">Processing: {repoUrl.split("/").slice(-2).join("/")}</p>
        </motion.div>

        {/* Central Animation Hub */}
        <div className="relative w-80 h-80 mx-auto mb-8">
          {/* Central Core */}
          <motion.div
            className="absolute top-1/2 left-1/2 w-16 h-16 -mt-8 -ml-8 rounded-full border-2 border-[#04a777] bg-[#04a777]/20"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Number.POSITIVE_INFINITY,
              ease: "easeInOut",
            }}
          />

          {/* Orbiting Agents */}
          {[0, 1, 2, 3, 4].map((index) => (
            <motion.div
              key={index}
              className="absolute w-4 h-4 bg-[#04a777] rounded-full"
              style={{
                top: "50%",
                left: "50%",
                marginTop: "-8px",
                marginLeft: "-8px",
              }}
              animate={{
                rotate: 360,
                x: Math.cos((index * 72 * Math.PI) / 180) * 100,
                y: Math.sin((index * 72 * Math.PI) / 180) * 100,
              }}
              transition={{
                rotate: {
                  duration: 4,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "linear",
                  delay: index * 0.2,
                },
                x: {
                  duration: 4,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "linear",
                  delay: index * 0.2,
                },
                y: {
                  duration: 4,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "linear",
                  delay: index * 0.2,
                },
              }}
            />
          ))}

          {/* Pulse Rings */}
          {[0, 1, 2].map((index) => (
            <motion.div
              key={`ring-${index}`}
              className="absolute top-1/2 left-1/2 border border-[#04a777]/30 rounded-full"
              style={{
                width: `${120 + index * 40}px`,
                height: `${120 + index * 40}px`,
                marginTop: `-${60 + index * 20}px`,
                marginLeft: `-${60 + index * 20}px`,
              }}
              animate={{
                scale: [1, 1.1, 1],
                opacity: [0.3, 0.1, 0.3],
              }}
              transition={{
                duration: 3,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut",
                delay: index * 0.5,
              }}
            />
          ))}

          {/* Connecting Lines */}
          <svg className="absolute inset-0 w-full h-full">
            {[0, 1, 2, 3, 4].map((index) => (
              <motion.line
                key={`line-${index}`}
                x1="50%"
                y1="50%"
                x2={`${50 + Math.cos((index * 72 * Math.PI) / 180) * 30}%`}
                y2={`${50 + Math.sin((index * 72 * Math.PI) / 180) * 30}%`}
                stroke="#04a777"
                strokeWidth="1"
                opacity="0.5"
                animate={{
                  opacity: [0.2, 0.8, 0.2],
                }}
                transition={{
                  duration: 2,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "easeInOut",
                  delay: index * 0.3,
                }}
              />
            ))}
          </svg>
        </div>

        {/* Status Message */}
        <motion.div
          key={currentMessage}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
          className="text-xl text-[#04a777] font-medium"
        >
          {messages[currentMessage]}
        </motion.div>

        {/* Progress Dots */}
        <div className="flex justify-center mt-6 space-x-2">
          {messages.map((_, index) => (
            <motion.div
              key={index}
              className={`w-2 h-2 rounded-full ${index <= currentMessage ? "bg-[#04a777]" : "bg-gray-600"}`}
              animate={{
                scale: index === currentMessage ? [1, 1.3, 1] : 1,
              }}
              transition={{
                duration: 0.3,
                repeat: index === currentMessage ? Number.POSITIVE_INFINITY : 0,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
