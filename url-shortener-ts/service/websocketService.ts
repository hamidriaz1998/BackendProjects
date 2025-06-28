import type { Server } from "npm:socket.io@^4.7.0";
import { UrlModel } from "../db/db.ts";

let io: Server | null = null;
let statsInterval: NodeJS.Timeout | null = null;

export function initializeWebSocket(socketServer: Server) {
  io = socketServer;
  console.log("📡 WebSocket service initialized");

  // Start periodic stats broadcasting
  startStatsInterval();
}

function startStatsInterval() {
  if (statsInterval) {
    clearInterval(statsInterval);
  }

  // Broadcast stats every 30 seconds
  statsInterval = setInterval(async () => {
    try {
      const stats = await getSystemStats();
      emitStatsUpdate(stats);
    } catch (error) {
      console.error("Error broadcasting stats:", error);
    }
  }, 30000);
}

async function getSystemStats() {
  try {
    const totalUrls = await UrlModel.countDocuments();
    const totalClicksResult = await UrlModel.aggregate([
      { $group: { _id: null, totalClicks: { $sum: "$clicks" } } },
    ]);
    const totalClicks = totalClicksResult[0]?.totalClicks || 0;
    const connectedClients = getConnectedClients();

    return {
      totalUrls,
      totalClicks,
      connectedClients,
    };
  } catch (error) {
    console.error("Error getting system stats:", error);
    return {
      totalUrls: 0,
      totalClicks: 0,
      connectedClients: getConnectedClients(),
    };
  }
}

export function emitClickUpdate(data: {
  shortCode: string;
  clicks: number;
  originalUrl: string;
  shortUrl: string;
}) {
  if (!io) {
    console.warn("⚠️ WebSocket server not initialized");
    return;
  }

  console.log(
    `📈 Broadcasting click update for ${data.shortCode}: ${data.clicks} clicks`,
  );

  io.emit("clickUpdate", {
    shortCode: data.shortCode,
    clicks: data.clicks,
    originalUrl: data.originalUrl,
    shortUrl: data.shortUrl,
    timestamp: new Date().toISOString(),
  });
}

export function emitNewUrl(data: {
  shortCode: string;
  originalUrl: string;
  shortUrl: string;
  clicks: number;
  createdAt: Date;
}) {
  if (!io) {
    console.warn("⚠️ WebSocket server not initialized");
    return;
  }

  console.log(`📝 Broadcasting new URL creation: ${data.shortCode}`);

  io.emit("newUrl", {
    shortCode: data.shortCode,
    originalUrl: data.originalUrl,
    shortUrl: data.shortUrl,
    clicks: data.clicks,
    createdAt: data.createdAt,
    timestamp: new Date().toISOString(),
  });
}

export function getConnectedClients(): number {
  if (!io) {
    return 0;
  }
  return io.engine.clientsCount;
}

export function emitToClient(socketId: string, event: string, data: any) {
  if (!io) {
    console.warn("⚠️ WebSocket server not initialized");
    return;
  }

  io.to(socketId).emit(event, data);
}

export function emitStatsUpdate(data: {
  totalUrls: number;
  totalClicks: number;
  connectedClients: number;
}) {
  if (!io) {
    console.warn("⚠️ WebSocket server not initialized");
    return;
  }

  console.log(
    `📊 Broadcasting stats: ${data.totalUrls} URLs, ${data.totalClicks} clicks, ${data.connectedClients} clients`,
  );

  io.emit("statsUpdate", {
    ...data,
    timestamp: new Date().toISOString(),
  });
}

export function stopStatsInterval() {
  if (statsInterval) {
    clearInterval(statsInterval);
    statsInterval = null;
    console.log("📊 Stats broadcasting stopped");
  }
}
