import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CodDoc - AI-Powered README Generator and Editor',
  description: 'Generate and Edit professional README files for your GitHub repositories using AI',
  generator: 'Next.js',
  icons: {
    icon: '/CodDoc.png',
    apple: '/CodDoc.png',
    shortcut: '/CodDoc.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
