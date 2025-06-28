// URL Shortener Frontend JavaScript with WebSocket Support

class URLShortenerApp {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.initializeWebSocket();
    this.loadRecentUrls();
  }

  setupEventListeners() {
    // Form submission
    const shortenForm = document.getElementById("shortenForm");
    shortenForm.addEventListener("submit", (e) => this.handleFormSubmit(e));

    // Copy button functionality
    document.addEventListener("click", (e) => {
      if (e.target.classList.contains("copy-btn")) {
        this.copyToClipboard(e.target.dataset.url);
      }
    });
  }

  initializeWebSocket() {
    console.log("🔌 Initializing WebSocket connection...");

    try {
      this.socket = io();
      this.setupSocketListeners();
    } catch (error) {
      console.error("❌ Failed to initialize WebSocket:", error);
      this.updateConnectionStatus("disconnected");
    }
  }

  setupSocketListeners() {
    // Connection events
    this.socket.on("connect", () => {
      console.log("✅ Connected to WebSocket server");
      this.isConnected = true;
      this.updateConnectionStatus("connected");
      this.updateConnectedUsers();
    });

    this.socket.on("disconnect", () => {
      console.log("❌ Disconnected from WebSocket server");
      this.isConnected = false;
      this.updateConnectionStatus("disconnected");
    });

    // Welcome message
    this.socket.on("welcome", (data) => {
      console.log("👋 WebSocket welcome:", data.message);
      this.showNotification("Connected to real-time updates", "success");
    });

    // Real-time click updates
    this.socket.on("clickUpdate", (data) => {
      console.log("📈 Real-time click update:", data);
      this.handleClickUpdate(data);
    });

    // New URL creation
    this.socket.on("newUrl", (data) => {
      console.log("📝 New URL created:", data);
      this.handleNewUrl(data);
    });

    // Stats updates
    this.socket.on("statsUpdate", (data) => {
      console.log("📊 Stats update:", data);
      this.updateStats(data);
    });

    // Connection errors
    this.socket.on("connect_error", (error) => {
      console.error("🔥 Connection error:", error);
      this.updateConnectionStatus("error");
    });
  }

  async handleFormSubmit(e) {
    e.preventDefault();

    const urlInput = document.getElementById("url");
    const resultDiv = document.getElementById("result");
    const submitButton = e.target.querySelector('button[type="submit"]');

    const url = urlInput.value.trim();

    if (!url) {
      this.showError("Please enter a URL");
      return;
    }

    // Show loading state
    this.setLoadingState(submitButton, true);

    try {
      const response = await fetch("/api/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (response.ok) {
        this.showSuccess(data);
        urlInput.value = ""; // Clear the input
      } else {
        throw new Error(data.error || "Failed to shorten URL");
      }
    } catch (error) {
      console.error("❌ Error shortening URL:", error);
      this.showError(error.message);
    } finally {
      this.setLoadingState(submitButton, false);
    }
  }

  showSuccess(data) {
    const resultDiv = document.getElementById("result");
    resultDiv.className = "result";
    resultDiv.innerHTML = `
            <div class="result-content">
                <div class="result-header">
                    <span class="result-icon">✨</span>
                    <h4>URL Shortened Successfully!</h4>
                </div>
                <div class="result-details">
                    <div class="result-row">
                        <span class="result-label">🌐 Original:</span>
                        <span class="result-value" title="${this.escapeHtml(data.originalUrl)}">${this.truncateUrl(data.originalUrl, 60)}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label">🔗 Short URL:</span>
                        <a href="${data.shortUrl}" target="_blank" class="result-link" rel="noopener noreferrer">${data.shortUrl}</a>
                    </div>
                </div>
                <div class="result-actions">
                    <button class="copy-btn primary" data-url="${data.shortUrl}" aria-label="Copy shortened URL">
                        <span class="copy-icon">📋</span>
                        <span class="copy-text">Copy Short URL</span>
                    </button>
                    <button class="share-btn" onclick="navigator.share ? navigator.share({url: '${data.shortUrl}'}) : null" aria-label="Share shortened URL">
                        <span class="share-icon">📤</span>
                        <span class="share-text">Share</span>
                    </button>
                </div>
            </div>
        `;
    resultDiv.style.display = "block";

    // Auto-hide after 10 seconds
    setTimeout(() => {
      resultDiv.style.display = "none";
    }, 10000);
  }

  showError(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.className = "result error";
    resultDiv.innerHTML = `
      <div class="result-content">
          <div class="result-header">
              <span class="result-icon">⚠️</span>
              <h4>Error</h4>
          </div>
          <div class="result-details">
              <p class="error-message">${this.escapeHtml(message)}</p>
          </div>
      </div>
  `;
    resultDiv.style.display = "block";

    // Auto-hide after 5 seconds
    setTimeout(() => {
      resultDiv.style.display = "none";
    }, 5000);
  }

  setLoadingState(button, loading) {
    if (loading) {
      button.disabled = true;
      button.innerHTML = `
        <span class="loading"></span>
        <span class="btn-text">Shortening...</span>
      `;
      button.classList.add("loading-state");
    } else {
      button.disabled = false;
      button.innerHTML = `
        <span class="btn-icon">⚡</span>
        <span class="btn-text">Shorten URL</span>
      `;
      button.classList.remove("loading-state");
    }
  }

  async loadRecentUrls() {
    try {
      const response = await fetch("/api/urls");
      if (!response.ok) {
        throw new Error("Failed to fetch URLs");
      }

      const urls = await response.json();
      this.displayUrls(urls.slice(0, 10)); // Show top 10

      // Update stats with current data
      this.updateStatsFromUrlData(urls);
    } catch (error) {
      console.error("❌ Error loading URLs:", error);
      const urlListDiv = document.getElementById("urlList");
      urlListDiv.innerHTML = '<p class="error">Failed to load URLs</p>';
    }
  }

  displayUrls(urls) {
    const urlListDiv = document.getElementById("urlList");

    if (urls.length === 0) {
      urlListDiv.innerHTML =
        "<p>No URLs created yet. Create your first shortened URL!</p>";
      return;
    }

    urlListDiv.innerHTML = urls
      .map(
        (url) => `
            <div class="url-item" data-short-code="${url.shortCode}" role="listitem">
                <div class="url-content">
                    <div class="url-info">
                        <div class="url-row">
                            <span class="url-label">🔗 Short URL:</span>
                            <a href="${url.shortUrl}" target="_blank" class="short-link" rel="noopener noreferrer">${url.shortUrl}</a>
                        </div>
                        <div class="url-row">
                            <span class="url-label">🌐 Original:</span>
                            <span class="original-url" title="${this.escapeHtml(url.originalUrl)}">${this.truncateUrl(url.originalUrl)}</span>
                        </div>
                        <div class="url-row">
                            <span class="url-label">🎯 Clicks:</span>
                            <span class="click-count">${url.clicks}</span>
                            <span class="click-indicator" aria-live="polite"></span>
                        </div>
                    </div>
                </div>
                <div class="url-meta">
                    <span class="creation-time" title="${new Date(url.createdAt).toLocaleString()}">
                        📅 ${this.formatDate(url.createdAt)}
                    </span>
                    <button class="copy-btn" data-url="${url.shortUrl}" aria-label="Copy ${url.shortUrl}">
                        <span class="copy-icon">📋</span>
                        <span class="copy-text">Copy</span>
                    </button>
                </div>
            </div>
        `,
      )
      .join("");
  }

  handleClickUpdate(data) {
    // Find the URL item in the list and update its click count
    const urlItem = document.querySelector(
      `[data-short-code="${data.shortCode}"]`,
    );
    if (urlItem) {
      const clickCountElement = urlItem.querySelector(".click-count");
      const clickIndicator = urlItem.querySelector(".click-indicator");

      if (clickCountElement) {
        // Animate the count change
        clickCountElement.style.transform = "scale(1.2)";
        clickCountElement.style.color = "#dc3545";
        clickCountElement.textContent = data.clicks;

        // Add visual indicator
        if (clickIndicator) {
          clickIndicator.innerHTML = "🔴 LIVE";
          clickIndicator.style.color = "red";
          clickIndicator.style.fontWeight = "bold";
        }

        // Add highlight animation to the entire item
        urlItem.classList.add("updated");

        // Reset styles after animation
        setTimeout(() => {
          clickCountElement.style.transform = "scale(1)";
          clickCountElement.style.color = "#28a745";
          if (clickIndicator) {
            clickIndicator.innerHTML = "";
          }
          urlItem.classList.remove("updated");
        }, 3000);
      }
    }

    // Show notification for click updates
    this.showNotification(
      `🎯 ${data.shortCode} clicked! Total: ${data.clicks}`,
      "info",
    );
  }

  handleNewUrl(data) {
    // Refresh the URL list to show the new URL
    this.loadRecentUrls();

    // Show notification
    this.showNotification(`📝 New URL created: ${data.shortCode}`, "success");

    // Scroll to the URL list to show the new addition
    const urlList = document.querySelector(".url-list");
    if (urlList) {
      urlList.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  updateConnectionStatus(status) {
    const statusElement = document.getElementById("connectionStatus");
    if (statusElement) {
      statusElement.className = `stat-value ${status}`;

      switch (status) {
        case "connected":
          statusElement.textContent = "🟢 Connected";
          break;
        case "disconnected":
          statusElement.textContent = "🔴 Disconnected";
          break;
        case "error":
          statusElement.textContent = "⚠️ Error";
          break;
        default:
          statusElement.textContent = "🟡 Connecting...";
      }
    }
  }

  updateConnectedUsers(count = 1) {
    const usersElement = document.getElementById("connectedUsers");
    if (usersElement) {
      usersElement.textContent = count;
    }
  }

  updateStatsFromUrlData(urls) {
    // Calculate stats from URL data as fallback
    const totalUrls = urls.length;
    const totalClicks = urls.reduce((sum, url) => sum + (url.clicks || 0), 0);

    const totalUrlsElement = document.getElementById("totalUrls");
    const totalClicksElement = document.getElementById("totalClicks");

    if (totalUrlsElement && totalUrlsElement.textContent === "-") {
      totalUrlsElement.textContent = totalUrls;
    }

    if (totalClicksElement && totalClicksElement.textContent === "-") {
      totalClicksElement.textContent = totalClicks;
    }
  }

  async fetchAndUpdateStats() {
    try {
      const response = await fetch("/api/stats/websocket");
      if (response.ok) {
        const data = await response.json();
        this.updateConnectedUsers(data.connectedClients);
      }
    } catch (error) {
      console.error("❌ Error fetching WebSocket stats:", error);
    }
  }

  updateStats(data) {
    this.updateConnectedUsers(data.connectedClients);

    const totalUrlsElement = document.getElementById("totalUrls");
    const totalClicksElement = document.getElementById("totalClicks");

    if (totalUrlsElement) {
      totalUrlsElement.textContent = data.totalUrls || 0;
    }

    if (totalClicksElement) {
      totalClicksElement.textContent = data.totalClicks || 0;
    }
  }

  async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      this.showNotification("📋 URL copied to clipboard!", "success");
    } catch (error) {
      console.error("Failed to copy to clipboard:", error);
      // Fallback for older browsers
      this.fallbackCopyToClipboard(text);
    }
  }

  fallbackCopyToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand("copy");
      this.showNotification("📋 URL copied to clipboard!", "success");
    } catch (error) {
      console.error("Fallback copy failed:", error);
      this.showNotification("❌ Failed to copy URL", "error");
    }

    document.body.removeChild(textArea);
  }

  showNotification(message, type = "info") {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll(".notification");
    existingNotifications.forEach((notification) => notification.remove());

    // Create new notification
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Style the notification
    Object.assign(notification.style, {
      position: "fixed",
      top: "20px",
      right: "20px",
      padding: "12px 20px",
      borderRadius: "8px",
      color: "white",
      fontWeight: "bold",
      zIndex: "10000",
      maxWidth: "400px",
      boxShadow: "0 8px 32px rgba(0, 0, 0, 0.15)",
      animation: "slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
      backdropFilter: "blur(12px)",
      border: "1px solid rgba(255, 255, 255, 0.18)",
    });

    // Set background color based on type
    switch (type) {
      case "success":
        notification.style.background =
          "linear-gradient(135deg, #10b981 0%, #059669 100%)";
        notification.innerHTML = `<span style="margin-right: 8px;">✅</span>${message}`;
        break;
      case "error":
        notification.style.background =
          "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)";
        notification.innerHTML = `<span style="margin-right: 8px;">❌</span>${message}`;
        break;
      case "info":
        notification.style.background =
          "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)";
        notification.innerHTML = `<span style="margin-right: 8px;">ℹ️</span>${message}`;
        break;
      default:
        notification.style.background =
          "linear-gradient(135deg, #6b7280 0%, #4b5563 100%)";
        notification.innerHTML = `<span style="margin-right: 8px;">📢</span>${message}`;
    }

    document.body.appendChild(notification);

    // Auto-remove notification after 3 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.style.animation = "fadeOut 0.3s ease forwards";
        setTimeout(() => {
          if (notification.parentNode) {
            notification.remove();
          }
        }, 300);
      }
    }, 3000);
  }

  escapeHtml(text) {
    const map = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
  }

  truncateUrl(url, maxLength = 50) {
    if (url.length <= maxLength) return this.escapeHtml(url);
    return this.escapeHtml(url.substring(0, maxLength)) + "...";
  }

  formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
  }
}

// Initialize the app when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Initializing URL Shortener App...");

  // Add loading animation to the container
  const container = document.querySelector(".container");
  if (container) {
    container.style.opacity = "0";
    container.style.transform = "translateY(20px)";

    setTimeout(() => {
      container.style.transition = "all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)";
      container.style.opacity = "1";
      container.style.transform = "translateY(0)";
    }, 100);
  }

  const app = new URLShortenerApp();

  // Fetch initial stats
  setTimeout(() => {
    app.fetchAndUpdateStats();
  }, 1000);

  // Add enhanced keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !e.target.matches("input, textarea")) {
      e.preventDefault();
      const urlInput = document.getElementById("url");
      if (urlInput) {
        urlInput.focus();
      }
    }
  });
});

// Add enhanced CSS animations dynamically
const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }

    .notification {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .activity-pulse {
        animation: activityPulse 1.5s ease-in-out;
    }

    @keyframes activityPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    .loading-state {
        position: relative;
        overflow: hidden;
    }

    .loading-state::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: loadingShimmer 1.5s infinite;
    }

    @keyframes loadingShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .url-content {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .url-item:hover .url-content {
        transform: translateX(4px);
    }

    .result-actions {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .result-actions button {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .share-btn {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    .primary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .url-info {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .url-row {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }

    .url-label {
        font-weight: 600;
        min-width: 100px;
        flex-shrink: 0;
        opacity: 0.8;
    }

    .short-link {
        font-family: 'Monaco', 'Consolas', monospace;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
    }

    .result-content {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .result-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .result-icon {
        font-size: 1.5rem;
    }

    .result-details {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .result-row {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }

    .result-label {
        font-weight: 600;
        min-width: 100px;
        flex-shrink: 0;
    }

    .result-value, .result-link {
        word-break: break-all;
    }

    .result-link {
        font-family: 'Monaco', 'Consolas', monospace;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
    }
`;
document.head.appendChild(style);
