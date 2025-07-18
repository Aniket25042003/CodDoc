import type { Metadata } from 'next'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import './globals.css'

export const metadata: Metadata = {
  title: 'CodDoc - AI-Powered README Generator and Editor',
  description: 'CodDoc is an AI-powered tool that instantly generates and edits professional, high-quality README files for your GitHub repositories. Just paste your repo URL and get a beautifully structured README with options to edit and customize it.',
  generator: 'Next.js',
  icons: {
    icon: '/favicon.ico',
    apple: '/favicon.ico',
    shortcut: '/favicon.ico',
  },
  verification: {
    google: 'QHzkptsQCDQ8B5TqtXBlX8ou_RyFcHKDY-wcNrsFwQA',
  },
  openGraph: {
    title: 'CodDoc - AI-Powered README Generator and Editor',
    description: 'CodDoc is an AI-powered tool that instantly generates and edits professional, high-quality README files for your GitHub repositories. Just paste your repo URL and get a beautifully structured README with options to edit and customize it.',
    url: 'https://cod-doc.vercel.app',
    siteName: 'CodDoc',
    images: [
      {
        url: 'https://cod-doc.vercel.app/CodDoc.png',
        width: 1200,
        height: 630,
        alt: 'CodDoc Logo',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CodDoc - AI-Powered README Generator and Editor',
    description: 'Generate and edit professional README files for your GitHub repositories using AI.',
    images: ['https://cod-doc.vercel.app/CodDoc.png'],
  },
  other: {
    'article:author': 'Aniket Patel',
    'article:published_time': '2025-06-17',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <GoogleAnalytics measurementId="G-LQT7GDE13T" />
        {children}
      </body>
    </html>
  )
}
