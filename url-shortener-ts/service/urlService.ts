import { UrlModel } from "../db/db.ts";

function isValidUrl(string: string): boolean {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

export async function shortenUrl(originalUrl: string) {
  if (!isValidUrl(originalUrl)) {
    throw new Error("Invalid URL provided");
  }

  // Check if URL already exists
  const existingUrl = await UrlModel.findOne({ originalUrl });
  if (existingUrl) {
    return existingUrl;
  }

  // Generate unique short URL
  let shortUrl: string;
  let isUnique = false;

  while (!isUnique) {
    shortUrl = Math.random().toString(36).substring(2, 8);
    const existing = await UrlModel.findOne({ shortUrl });
    if (!existing) {
      isUnique = true;
    }
  }

  const url = new UrlModel({ originalUrl, shortUrl: shortUrl! });
  await url.save();
  return url;
}

export async function getOriginalUrl(shortCode: string) {
  try {
    const urlDoc = await UrlModel.findOne({ shortUrl: shortCode });
    return urlDoc;
  } catch (error) {
    console.error("Error finding URL:", error);
    throw new Error("Failed to retrieve URL");
  }
}

export async function incrementClicks(shortCode: string) {
  try {
    const urlDoc = await UrlModel.findOneAndUpdate(
      { shortUrl: shortCode },
      { $inc: { clicks: 1 } },
      { new: true },
    );
    return urlDoc;
  } catch (error) {
    console.error("Error incrementing clicks:", error);
    throw new Error("Failed to update click count");
  }
}

export async function getUrlStats(shortCode: string) {
  try {
    const urlDoc = await UrlModel.findOne({ shortUrl: shortCode });
    if (!urlDoc) {
      throw new Error("Short URL not found");
    }
    return urlDoc;
  } catch (error) {
    console.error("Error getting URL stats:", error);
    throw error;
  }
}

export async function getAllUrls() {
  try {
    const urls = await UrlModel.find({}).sort({ createdAt: -1 });
    return urls;
  } catch (error) {
    console.error("Error fetching URLs:", error);
    throw new Error("Failed to fetch URLs");
  }
}
