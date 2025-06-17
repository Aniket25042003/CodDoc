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
  verification: {
    google: 'QHzkptsQCDQ8B5TqtXBlX8ou_RyFcHKDY-wcNrsFwQA',
  },
  openGraph: {
    title: 'CodDoc - AI-Powered README Generator and Editor',
    description: 'Generate and edit professional README files for your GitHub repositories using AI.',
    url: 'https://cod-doc.vercel.app',
    siteName: 'CodDoc',
    images: [
      {
        url: '/CodDoc.png',
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
    images: ['/CodDoc.png'],
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
