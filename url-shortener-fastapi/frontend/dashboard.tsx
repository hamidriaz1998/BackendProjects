"use client"

import { useState } from "react"
import { DashboardHeader } from "./components/dashboard-header"
import { DashboardStats } from "./components/dashboard-stats"
import { UrlShortenerForm } from "./components/url-shortener-form"
import { UrlList } from "./components/url-list"
import { Toaster } from "@/components/ui/toaster"

interface ShortenedUrl {
  id: string
  originalUrl: string
  shortUrl: string
  createdAt: Date
  expiresAt: Date | null
  clicks: number
}

export default function Dashboard() {
  const [urls, setUrls] = useState<ShortenedUrl[]>([
    {
      id: "1",
      originalUrl: "https://www.example.com/very-long-url-that-needs-shortening",
      shortUrl: "https://short.ly/abc123",
      createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
      expiresAt: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000), // 5 days from now
      clicks: 42,
    },
    {
      id: "2",
      originalUrl: "https://github.com/user/repository-name",
      shortUrl: "https://short.ly/def456",
      createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 days ago
      expiresAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // Expired 1 day ago
      clicks: 18,
    },
    {
      id: "3",
      originalUrl: "https://docs.example.com/documentation/getting-started",
      shortUrl: "https://short.ly/ghi789",
      createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
      expiresAt: null, // Never expires
      clicks: 7,
    },
  ])

  const handleUrlShortened = (newUrl: ShortenedUrl) => {
    setUrls((prev) => [newUrl, ...prev])
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto py-6 space-y-6">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Manage your shortened URLs and track their performance</p>
        </div>

        <DashboardStats urls={urls} />

        <div className="grid gap-6 lg:grid-cols-2">
          <UrlShortenerForm onUrlShortened={handleUrlShortened} />
          <div className="lg:col-span-2">
            <UrlList urls={urls} />
          </div>
        </div>
      </main>

      <Toaster />
    </div>
  )
}
