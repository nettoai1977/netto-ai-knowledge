#!/usr/bin/env node
/**
 * Trinity Dashboard Server
 * Serves the trading dashboard with live data
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8888;
const TRADING_DIR = __dirname;

// MIME types
const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml'
};

// Get latest data files
function getLatestData(pattern, limit = 1) {
  const matrixDir = path.join(TRADING_DIR, 'matrix-data');
  if (!fs.existsSync(matrixDir)) return [];
  
  const files = fs.readdirSync(matrixDir)
    .filter(f => f.includes(pattern))
    .sort()
    .reverse()
    .slice(0, limit);
  
  return files.map(f => {
    const filePath = path.join(matrixDir, f);
    try {
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch {
      return null;
    }
  }).filter(Boolean);
}

// Get paper positions
function getPaperPositions() {
  const positionsFile = path.join(TRADING_DIR, 'paper_positions.json');
  if (fs.existsSync(positionsFile)) {
    return JSON.parse(fs.readFileSync(positionsFile, 'utf8'));
  }
  return { positions: [], balance: 10000 };
}

// Build dashboard data
function buildDashboardData() {
  const latest15m = getLatestData('15m-tactical', 1)[0];
  const latest1h = getLatestData('1h-shift', 1)[0];
  const latest4h = getLatestData('4h-outlook', 1)[0];
  const latestDaily = getLatestData('daily-macro', 1)[0];
  const paper = getPaperPositions();
  
  // Extract watchlist from 15m data
  const watchlist = latest15m?.data || [];
  
  // Calculate stats
  const totalSignals = watchlist.length;
  const avgConfluence = totalSignals > 0 
    ? (watchlist.reduce((sum, s) => sum + s.confluence, 0) / totalSignals).toFixed(1)
    : 0;
  
  return {
    timestamp: new Date().toISOString(),
    stats: {
      capital: paper.balance || 4999.53,
      totalPnl: 0,
      winRate: 0,
      totalTrades: paper.positions?.length || 0,
      signalsToday: totalSignals,
      avgConfluence
    },
    timeframes: {
      daily: {
        lastRun: latestDaily?.timestamp || '-',
        bias: latestDaily?.bias || 'BEARISH',
        btcTrend: latestDaily?.btcTrend || 'DOWN',
        fearGreed: latestDaily?.fearGreed || '-'
      },
      fourH: {
        lastRun: latest4h?.timestamp || '-',
        alignment: latest4h?.alignment || 'BEARISH',
        divergences: latest4h?.divergences || 0,
        keyLevels: latest4h?.keyLevels || 'Testing support'
      },
      oneH: {
        lastRun: latest1h?.timestamp || '-',
        volumeSpikes: latest1h?.volumeSpikes || 0,
        srBreaks: latest1h?.srBreaks || 0,
        exhaustion: latest1h?.exhaustion || 'None'
      },
      fifteenM: {
        lastRun: latest15m?.timestamp || '-',
        signals: totalSignals,
        topConfluence: Math.max(...watchlist.map(s => s.confluence), 0),
        nextScan: 'Auto'
      }
    },
    watchlist,
    positions: paper.positions || [],
    signals: watchlist.filter(s => s.confluence >= 6).slice(0, 3)
  };
}

// Handle API requests
function handleAPI(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  if (url.pathname === '/api/dashboard') {
    const data = buildDashboardData();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data, null, 2));
    return;
  }
  
  if (url.pathname === '/api/positions') {
    const paper = getPaperPositions();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(paper, null, 2));
    return;
  }
  
  if (url.pathname === '/api/signals') {
    const latest = getLatestData('15m-tactical', 1)[0];
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(latest, null, 2));
    return;
  }
  
  res.writeHead(404);
  res.end('Not found');
}

// Serve static files
function serveStatic(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  let filePath = url.pathname;
  
  // Default to dashboard.html
  if (filePath === '/') {
    filePath = '/dashboard.html';
  }
  
  const fullPath = path.join(TRADING_DIR, filePath);
  
  // Security check
  if (!fullPath.startsWith(TRADING_DIR)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }
  
  // Check if file exists
  if (!fs.existsSync(fullPath)) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  
  // Get MIME type
  const ext = path.extname(fullPath);
  const mimeType = MIME_TYPES[ext] || 'application/octet-stream';
  
  // Serve file
  fs.readFile(fullPath, (err, data) => {
    if (err) {
      res.writeHead(500);
      res.end('Server error');
      return;
    }
    res.writeHead(200, { 'Content-Type': mimeType });
    res.end(data);
  });
}

// Create server
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  
  if (url.pathname.startsWith('/api/')) {
    handleAPI(req, res);
  } else {
    serveStatic(req, res);
  }
});

server.listen(PORT, () => {
  console.log(`🎯 Trinity Dashboard Server running at http://localhost:${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}/`);
  console.log(`📡 API: http://localhost:${PORT}/api/dashboard`);
  console.log(`\nPress Ctrl+C to stop`);
});
