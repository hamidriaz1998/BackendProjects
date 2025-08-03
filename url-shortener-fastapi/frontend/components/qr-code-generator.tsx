"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { QrCode, Download } from "lucide-react"
import { toast } from "@/hooks/use-toast"

interface QRCodeGeneratorProps {
  url: string
  disabled?: boolean
}

export function QRCodeGenerator({ url, disabled = false }: QRCodeGeneratorProps) {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)

  const generateQRCode = async () => {
    setIsLoading(true)
    try {
      // Using QR Server API for QR code generation
      const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(url)}`
      setQrCodeUrl(qrUrl)
    } catch (error) {
      toast({
        title: "Error generating QR code",
        description: "Failed to generate QR code. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const downloadQRCode = async () => {
    if (!qrCodeUrl) return

    try {
      const response = await fetch(qrCodeUrl)
      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = downloadUrl
      link.download = `qr-code-${Date.now()}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)

      toast({
        title: "QR code downloaded",
        description: "The QR code has been saved to your downloads.",
      })
    } catch (error) {
      toast({
        title: "Download failed",
        description: "Failed to download QR code. Please try again.",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" onClick={generateQRCode} disabled={disabled} className="h-6 w-6 p-0">
          <QrCode className="h-3 w-3" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>QR Code</DialogTitle>
          <DialogDescription>Scan this QR code to access the shortened URL</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col items-center space-y-4">
          {isLoading ? (
            <div className="w-[300px] h-[300px] bg-muted animate-pulse rounded-lg flex items-center justify-center">
              <QrCode className="h-12 w-12 text-muted-foreground" />
            </div>
          ) : qrCodeUrl ? (
            <div className="space-y-4">
              <img
                src={qrCodeUrl || "/placeholder.svg"}
                alt="QR Code"
                className="w-[300px] h-[300px] border rounded-lg"
                crossOrigin="anonymous"
              />
              <div className="flex justify-center space-x-2">
                <Button onClick={downloadQRCode} size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </div>
            </div>
          ) : (
            <div className="w-[300px] h-[300px] bg-muted rounded-lg flex items-center justify-center">
              <QrCode className="h-12 w-12 text-muted-foreground" />
            </div>
          )}
          <div className="text-center space-y-2">
            <p className="text-sm font-medium">Short URL:</p>
            <code className="text-sm bg-muted px-2 py-1 rounded">{url}</code>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
