"use client"

import Link from "next/link"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Copy, Check, ExternalLink, BarChart3 } from "lucide-react"
import { toast } from "@/hooks/use-toast"
import { QRCodeGenerator } from "./qr-code-generator"

interface ShortenedUrl {
  id: string
  originalUrl: string
  shortUrl: string
  createdAt: Date
  expiresAt: Date | null
  clicks: number
}

interface UrlListProps {
  urls: ShortenedUrl[]
}

export function UrlList({ urls }: UrlListProps) {
  const [copiedId, setCopiedId] = useState<string | null>(null)

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

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date)
  }

  const truncateUrl = (url: string, maxLength = 50) => {
    return url.length > maxLength ? `${url.substring(0, maxLength)}...` : url
  }

  const isExpired = (expiresAt: Date | null) => {
    if (!expiresAt) return false
    return new Date() > expiresAt
  }

  const formatExpirationDate = (expiresAt: Date | null) => {
    if (!expiresAt) return "Never"
    const now = new Date()
    const diffMs = expiresAt.getTime() - now.getTime()

    if (diffMs < 0) return "Expired"

    const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
    const diffHours = Math.ceil(diffMs / (1000 * 60 * 60))

    if (diffDays > 1) return `${diffDays} days`
    if (diffHours > 1) return `${diffHours} hours`
    return "Less than 1 hour"
  }

  if (urls.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Your URLs
          </CardTitle>
          <CardDescription>Your shortened URLs will appear here</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Link className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No URLs shortened yet</p>
            <p className="text-sm">Create your first shortened URL above</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5" />
          Your URLs ({urls.length})
        </CardTitle>
        <CardDescription>Manage and track your shortened URLs</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Original URL</TableHead>
                <TableHead>Short URL</TableHead>
                <TableHead>Clicks</TableHead>
                <TableHead>Created</TableHead>
                <TableHead>Expires</TableHead>
                <TableHead className="w-[100px]">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {urls.map((url) => (
                <TableRow key={url.id} className={isExpired(url.expiresAt) ? "opacity-50" : ""}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span
                        className={`font-medium ${isExpired(url.expiresAt) ? "line-through text-muted-foreground" : ""}`}
                        title={url.originalUrl}
                      >
                        {truncateUrl(url.originalUrl)}
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => window.open(url.originalUrl, "_blank")}
                        className="h-6 w-6 p-0"
                        disabled={isExpired(url.expiresAt)}
                      >
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <code
                        className={`text-sm bg-muted px-2 py-1 rounded ${isExpired(url.expiresAt) ? "line-through text-muted-foreground" : ""}`}
                      >
                        {url.shortUrl}
                      </code>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(url.shortUrl, url.id)}
                        className="h-6 w-6 p-0"
                        disabled={isExpired(url.expiresAt)}
                      >
                        {copiedId === url.id ? (
                          <Check className="h-3 w-3 text-green-600" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                      </Button>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={isExpired(url.expiresAt) ? "opacity-50" : ""}>
                      {url.clicks}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    <div className="space-y-1">
                      <div>{formatDate(url.createdAt)}</div>
                      <div className={`text-xs ${isExpired(url.expiresAt) ? "text-red-500" : "text-muted-foreground"}`}>
                        Expires: {formatExpirationDate(url.expiresAt)}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => window.open(url.shortUrl, "_blank")}
                        disabled={isExpired(url.expiresAt)}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                      <QRCodeGenerator url={url.shortUrl} disabled={isExpired(url.expiresAt)} />
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}
