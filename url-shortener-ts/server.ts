import express from "express";
import { createServer } from "node:http";
import { Server } from "npm:socket.io@^4.7.0";
import { UrlModel } from "./db/db.ts";
import { shortenUrl } from "./service/urlService.ts";
import {
  initializeWebSocket,
  emitClickUpdate,
  emitNewUrl,
} from "./service/websocketService.ts";

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static HTML for the frontend
app.use(express.static("public"));

// API endpoint to shorten URL
app.post("/api/shorten", async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({ error: "URL is required" });
    }

    const shortenedUrl = await shortenUrl(url);

    // Emit new URL creation to all connected clients
    emitNewUrl({
      shortCode: shortenedUrl.shortUrl,
      originalUrl: shortenedUrl.originalUrl,
      shortUrl: `http://localhost:${PORT}/${shortenedUrl.shortUrl}`,
      clicks: shortenedUrl.clicks,
      createdAt: shortenedUrl.createdAt,
    });

    res.json({
      originalUrl: shortenedUrl.originalUrl,
      shortUrl: `http://localhost:${PORT}/${shortenedUrl.shortUrl}`,
      shortCode: shortenedUrl.shortUrl,
    });
  } catch (error) {
    console.error("Error shortening URL:", error);
    res.status(400).json({ error: error.message });
  }
});

// Redirect endpoint - handles short URL redirection
app.get("/:shortCode", async (req, res) => {
  try {
    const { shortCode } = req.params;

    const urlDoc = await UrlModel.findOne({ shortUrl: shortCode });

    if (!urlDoc) {
      return res.status(404).json({ error: "Short URL not found" });
    }

    // Increment click count
    urlDoc.clicks += 1;
    await urlDoc.save();

    // Emit real-time update to all connected clients
    emitClickUpdate({
      shortCode: shortCode,
      clicks: urlDoc.clicks,
      originalUrl: urlDoc.originalUrl,
      shortUrl: `http://localhost:${PORT}/${shortCode}`,
    });

    // Redirect to original URL
    res.redirect(urlDoc.originalUrl);
  } catch (error) {
    console.error("Error redirecting:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// API endpoint to get URL stats
app.get("/api/stats/:shortCode", async (req, res) => {
  try {
    const { shortCode } = req.params;

    const urlDoc = await UrlModel.findOne({ shortUrl: shortCode });

    if (!urlDoc) {
      return res.status(404).json({ error: "Short URL not found" });
    }

    res.json({
      originalUrl: urlDoc.originalUrl,
      shortUrl: `http://localhost:${PORT}/${urlDoc.shortUrl}`,
      shortCode: urlDoc.shortUrl,
      clicks: urlDoc.clicks,
      createdAt: urlDoc.createdAt,
    });
  } catch (error) {
    console.error("Error getting stats:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// API endpoint to list all URLs
app.get("/api/urls", async (req, res) => {
  try {
    const urls = await UrlModel.find({}).sort({ createdAt: -1 });

    const urlsWithFullPath = urls.map((url) => ({
      originalUrl: url.originalUrl,
      shortUrl: `http://localhost:${PORT}/${url.shortUrl}`,
      shortCode: url.shortUrl,
      clicks: url.clicks,
      createdAt: url.createdAt,
    }));

    res.json(urlsWithFullPath);
  } catch (error) {
    console.error("Error fetching URLs:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", timestamp: new Date().toISOString() });
});

// WebSocket stats endpoint
app.get("/api/stats/websocket", (req, res) => {
  try {
    const connectedClients = io ? io.engine.clientsCount : 0;
    res.json({
      connectedClients,
      status: "OK",
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Error getting WebSocket stats:", error);
    res.status(500).json({ error: "Failed to get WebSocket stats" });
  }
});

// Root endpoint - serve the main page
app.get("/", (req, res) => {
  res.sendFile("index.html", { root: "./public" });
});

// Error handling middleware
app.use(
  (
    err: Error,
    req: express.Request,
    res: express.Response,
    next: express.NextFunction,
  ) => {
    console.error("Unhandled error:", err);
    res.status(500).json({ error: "Internal server error" });
  },
);

// Initialize WebSocket service
initializeWebSocket(io);

// WebSocket connection handling
io.on("connection", (socket) => {
  console.log("👤 Client connected:", socket.id);

  socket.on("disconnect", () => {
    console.log("👋 Client disconnected:", socket.id);
  });

  // Send current stats to newly connected client
  socket.emit("welcome", {
    message: "Connected to URL Shortener WebSocket",
    timestamp: new Date().toISOString(),
  });
});

// Start server
server.listen(PORT, () => {
  console.log(`🚀 URL Shortener server running on http://localhost:${PORT}`);
  console.log(`🔌 WebSocket server enabled for real-time updates`);
  console.log(`📝 API endpoints:`);
  console.log(`   POST /api/shorten - Shorten a URL`);
  console.log(`   GET /:shortCode - Redirect to original URL`);
  console.log(`   GET /api/stats/:shortCode - Get URL statistics`);
  console.log(`   GET /api/urls - List all URLs`);
  console.log(`   GET /api/health - Health check`);
});

export default app;
