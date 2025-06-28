# 🔗 URL Shortener

A full-featured URL shortener built with Deno, Express, and MongoDB. Create short URLs, track clicks, and manage your links with both a web interface and CLI.

## ✨ Features

- **URL Shortening**: Convert long URLs into short, shareable links
- **Click Tracking**: Monitor how many times your short URLs are accessed
- **Web Interface**: Beautiful, responsive web UI for easy URL management
- **REST API**: Full API for programmatic access
- **CLI Interface**: Command-line tool for power users
- **Duplicate Detection**: Automatically returns existing short URLs for previously shortened links
- **URL Validation**: Ensures only valid URLs are shortened
- **Statistics**: View detailed stats for each shortened URL

## 🚀 Quick Start

### Prerequisites

- [Deno](https://deno.land/) (v1.0+)
- [MongoDB](https://www.mongodb.com/) running on `localhost:27017`

### Installation

1. Clone or download the project
2. Navigate to the project directory:

   ```bash
   cd url-shortener
   ```

3. Start MongoDB (make sure it's running on `mongodb://127.0.0.1/url-shortener`)

### Running the Application

#### Web Server (Recommended)

Start the web server with auto-reload:

```bash
deno task server
```

Then open your browser to: http://localhost:3000

## 📖 Usage

## 🔌 Real-Time Features

### WebSocket Events

The application uses WebSocket connections to provide real-time updates:

- **Click Updates**: See clicks happening live as users access short URLs
- **New URL Creation**: Get notified when new URLs are created
- **Connection Status**: Live connection status and user count
- **Statistics Updates**: Real-time stats broadcasting every 30 seconds

### Live Dashboard

The web interface shows:

- 👥 **Connected Users**: Number of active WebSocket connections
- 📊 **Total URLs**: Total number of shortened URLs
- 🎯 **Total Clicks**: Aggregate click count across all URLs
- 🔴 **Live Indicators**: Visual feedback when clicks happen in real-time

## 📚 API Reference

The URL Shortener provides a RESTful API for integration with other applications.

### Base URL

```
http://localhost:3000
```

### API Endpoints

#### Shorten a URL

```http
POST /api/shorten
Content-Type: application/json

{
  "url": "https://example.com"
}
```

Response:

```json
{
  "originalUrl": "https://example.com",
  "shortUrl": "http://localhost:3000/abc123",
  "shortCode": "abc123"
}
```

**Real-time effect**: All connected clients will see the new URL appear instantly in their dashboard.

#### Redirect to Original URL

```http
GET /:shortCode
```

Redirects to the original URL and increments click counter.

**Real-time effect**: All connected clients will see the click count update live with visual indicators.

#### Get URL Statistics

```http
GET /api/stats/:shortCode
```

Response:

```json
{
  "originalUrl": "https://example.com",
  "shortUrl": "http://localhost:3000/abc123",
  "shortCode": "abc123",
  "clicks": 42,
  "createdAt": "2024-01-15T10:30:00.000Z"
}
```

#### List All URLs

```http
GET /api/urls
```

#### WebSocket Statistics

```http
GET /api/stats/websocket
```

Response:

```json
{
  "connectedClients": 5,
  "status": "OK",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### Health Check

```http
GET /api/health
```

## 🏗️ Project Structure

```
url-shortener/
├── db/
│   └── db.ts              # MongoDB connection and schema
├── service/
│   └── urlService.ts      # URL shortening business logic
├── cli.ts                 # Command-line interface
├── server.ts              # Express web server
├── main.ts                # Simple console app
├── deno.json              # Deno configuration and tasks
└── README.md              # This file
```

## 🛠️ Development

### Available Tasks

```bash
# Start web server with auto-reload
deno task server

# Start production server
deno task start
```

### Database Schema

The URL documents are stored with the following schema:

```typescript
{
  originalUrl: string; // The original long URL
  shortUrl: string; // The short code (e.g., "abc123")
  clicks: number; // Number of times the short URL was accessed
  createdAt: Date; // When the URL was created
  updatedAt: Date; // When the URL was last modified
}
```

## 🔧 Configuration

### Database

By default, the app connects to `mongodb://127.0.0.1/url-shortener`. To use a different MongoDB connection string, you can modify the connection in `db/db.ts`.

### Port

The web server runs on port 3000 by default. You can modify this in `server.ts`.

### Short URL Length

Short codes are 6 characters long by default. You can adjust this in the `shortenUrl` function in `service/urlService.ts`.

## 🚨 Error Handling

The application includes comprehensive error handling for:

- Invalid URLs
- Database connection issues
- Short URL collisions
- Missing short codes
- Network errors

## 🔒 Security Considerations

- URLs are validated before shortening
- No authentication is implemented (consider adding for production)
- Short codes are randomly generated (consider using a more secure method for production)
- No rate limiting is implemented

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### MongoDB Connection Issues

- Ensure MongoDB is running: `mongod`
- Check if the database is accessible at `mongodb://127.0.0.1:27017`
- Verify the database name is `url-shortener`

### Permission Errors

Make sure to run Deno commands with necessary permissions:

```bash
deno run --allow-net --allow-read --allow-env [script.ts]
```

### Port Already in Use

If port 3000 is already in use, modify the `PORT` constant in `server.ts`.

## 📊 Features Roadmap

- [ ] User authentication
- [ ] Custom short codes
- [ ] Expiration dates for URLs
- [ ] Analytics dashboard
- [ ] QR code generation
- [ ] Bulk URL shortening
- [ ] Rate limiting
- [ ] URL categories/tags
