"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Link } from "lucide-react"
import { toast } from "@/hooks/use-toast"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface ShortenedUrl {
  id: string
  originalUrl: string
  shortUrl: string
  createdAt: Date
  expiresAt: Date | null
  clicks: number
}

interface UrlShortenerFormProps {
  onUrlShortened: (url: ShortenedUrl) => void
}

export function UrlShortenerForm({ onUrlShortened }: UrlShortenerFormProps) {
  const [url, setUrl] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const [expirationOption, setExpirationOption] = useState("7days")

  const generateShortUrl = () => {
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    let result = ""
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return `https://short.ly/${result}`
  }

  const getExpirationDate = (option: string): Date | null => {
    const now = new Date()
    switch (option) {
      case "1hour":
        return new Date(now.getTime() + 60 * 60 * 1000)
      case "1day":
        return new Date(now.getTime() + 24 * 60 * 60 * 1000)
      case "7days":
        return new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
      case "30days":
        return new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)
      case "never":
        return null
      default:
        return new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!url) return

    setIsLoading(true)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const shortenedUrl: ShortenedUrl = {
      id: Math.random().toString(36).substr(2, 9),
      originalUrl: url,
      shortUrl: generateShortUrl(),
      createdAt: new Date(),
      expiresAt: getExpirationDate(expirationOption),
      clicks: 0,
    }

    onUrlShortened(shortenedUrl)
    setUrl("")
    setIsLoading(false)

    toast({
      title: "URL shortened successfully!",
      description: "Your shortened URL has been created.",
    })
  }

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
      toast({
        title: "Copied to clipboard!",
        description: "The URL has been copied to your clipboard.",
      })
    } catch (err) {
      toast({
        title: "Failed to copy",
        description: "Could not copy URL to clipboard.",
        variant: "destructive",
      })
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Link className="h-5 w-5" />
          Shorten URL
        </CardTitle>
        <CardDescription>Enter a long URL to create a shortened version</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="url">URL to shorten</Label>
            <Input
              id="url"
              type="url"
              placeholder="https://example.com/very-long-url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="expiration">Expiration</Label>
            <Select value={expirationOption} onValueChange={setExpirationOption}>
              <SelectTrigger>
                <SelectValue placeholder="Select expiration time" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1hour">1 Hour</SelectItem>
                <SelectItem value="1day">1 Day</SelectItem>
                <SelectItem value="7days">7 Days</SelectItem>
                <SelectItem value="30days">30 Days</SelectItem>
                <SelectItem value="never">Never</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? "Shortening..." : "Shorten URL"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
