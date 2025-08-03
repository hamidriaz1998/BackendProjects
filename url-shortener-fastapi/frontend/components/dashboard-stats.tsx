import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, Link, MousePointer, TrendingUp } from "lucide-react"

interface ShortenedUrl {
  id: string
  originalUrl: string
  shortUrl: string
  createdAt: Date
  expiresAt: Date | null
  clicks: number
}

interface DashboardStatsProps {
  urls: ShortenedUrl[]
}

export function DashboardStats({ urls }: DashboardStatsProps) {
  const totalUrls = urls.length
  const totalClicks = urls.reduce((sum, url) => sum + url.clicks, 0)
  const avgClicksPerUrl = totalUrls > 0 ? Math.round(totalClicks / totalUrls) : 0
  const urlsThisWeek = urls.filter((url) => {
    const weekAgo = new Date()
    weekAgo.setDate(weekAgo.getDate() - 7)
    return url.createdAt >= weekAgo
  }).length

  const expiredUrls = urls.filter((url) => {
    if (!url.expiresAt) return false
    return new Date() > url.expiresAt
  }).length

  const stats = [
    {
      title: "Total URLs",
      value: totalUrls.toString(),
      description: "URLs shortened",
      icon: Link,
    },
    {
      title: "Total Clicks",
      value: totalClicks.toString(),
      description: "Across all URLs",
      icon: MousePointer,
    },
    {
      title: "Expired URLs",
      value: expiredUrls.toString(),
      description: "No longer accessible",
      icon: BarChart3,
    },
    {
      title: "This Week",
      value: urlsThisWeek.toString(),
      description: "New URLs created",
      icon: TrendingUp,
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">{stat.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
