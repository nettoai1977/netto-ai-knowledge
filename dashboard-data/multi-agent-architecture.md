# Multi-Agent Dashboard Architecture

**Document Version:** 1.0  
**Author:** Atlas (Deep Reasoning Specialist)  
**Date:** 2026-02-17  
**Status:** Design Proposal

---

## Executive Summary

This document outlines the architecture for extending the OpenClaw Dashboard to support monitoring and managing all 12 agents in the OpenClaw ecosystem: **main, atlas, luna, orion, nova, zen, flash, titan, coder, max, spark, vision**.

The current dashboard monitors only a single agent (determined by `OPENCLAW_AGENT` environment variable) and requires architectural changes to support multi-agent operations while maintaining backward compatibility.

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Architecture Overview](#architecture-overview)
3. [Data Model Design](#data-model-design)
4. [API Endpoint Design](#api-endpoint-design)
5. [UI/UX Recommendations](#uiux-recommendations)
6. [Implementation Phases](#implementation-phases)
7. [Performance Considerations](#performance-considerations)
8. [Security Considerations](#security-considerations)

---

## 1. Current State Analysis

### 1.1 Existing Architecture

**Server-side (`server.js`):**
- Single-agent session directory: `~/.openclaw/agents/${AGENT_ID}/sessions/`
- Environment-driven agent selection: `process.env.OPENCLAW_AGENT || 'main'`
- Session data stored in JSONL files with metadata in `sessions.json`
- Real-time file watching via `fs.watch()` for live feed
- Authentication system with MFA support
- Cost tracking, token usage, and health monitoring

**Client-side (`index.html`):**
- Single-Page Application (SPA) with 9 pages
- No awareness of multiple agents
- Dashboard assumes it's monitoring one agent
- Navigation, data fetching, and state management are agent-agnostic

### 1.2 Limitations

| Limitation | Impact |
|------------|--------|
| Single AGENT_ID environment variable | Can only monitor one agent at a time |
| Hardcoded session directory path | no mechanism to switch between agents |
| No multi-agent UI components | No way to view/compare agents side-by-side |
| Single live feed stream | Cannot monitor all agents simultaneously |
| Monolithic cost tracking | Costs cannot be attributed per-agent |

### 1.3 Agent Directory Structure

```
~/.openclaw/
├── agents/
│   ├── main/
│   │   ├── sessions/
│   │   │   ├── sessions.json
│   │   │   └── *.jsonl
│   │   └── AGENT_CONFIG.json (proposed)
│   ├── atlas/
│   │   ├── sessions/
│   │   └── AGENT_CONFIG.json
│   ├── luna/
│   ├── orion/
│   ├── nova/
│   ├── zen/
│   ├── flash/
│   ├── titan/
│   ├── coder/
│   ├── max/
│   ├── spark/
│   └── vision/
└── dashboard-multi-agent-index.json (proposed)
```

---

## 2. Architecture Overview

### 2.1 Design Principles

1. **Backward Compatibility**: Existing single-agent deployments must continue working
2. **Explicit Selection**: Users must knowingly select which agent(s) to view
3. **Performance-conscious**: Minimize overhead when monitoring multiple agents
4. **Extensible**: Easy to add new agents or agent groups in the future
5. **Consistent UI**: Multi-agent view should feel like a natural extension

### 2.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Multi-Agent Dashboard UI                      │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐   │  │
│  │  │ Agent    │ │ Agent    │ │ Comparative Views     │   │  │
│  │  │ Switcher │ │ Health   │ │ (costs, sessions...)  │   │  │
│  │  └────┬─────┘ └────┬─────┘ └──────────┬───────────┘   │  │
│  └───────┼───────────┴──────────────────┘                 │  │
└──────────┼────────────────────────────────────────────┬───┘
           │                                            │
           │ HTTP/WebSocket                             │
           │                                            │
┌──────────┼────────────────────────────────────────────┼───┐
│  ┌───────▼────────────────────────────────────────────▼───┐ │
│  │              Server.js (Enhanced)                       │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │        AgentRegistry Service                      │  │  │
│  │  │  - Tracks all 12 agents                          │  │  │
│  │  │  - Health status per agent                       │  │  │
│  │  │  - Session directories per agent                 │  │  │
│  │  └────────────┬─────────────────────────────────────┘  │ │
│  │  ┌─────────────▼──────────────────────────────────┐    │ │
│  │  │        Session Aggregator                       │    │ │
│  │  │  - Collects sessions across agents              │    │ │
│  │  │  - Merges/cost/token aggregation                │    │ │
│  │  │  - Live feed from all agents                    │    │ │
│  │  └────────────┬───────────────────────────────────┘    │ │
│  │  ┌─────────────▼──────────────────────────────────┐    │ │
│  │  │        Cost Tracker (Multi-Agent)               │    │ │
│  │  │  - Per-agent cost attribution                  │    │ │
│  │  │  - Cross-agent cost breakdown                  │    │ │
│  │  └────────────┬───────────────────────────────────┘    │ │
│  └──────────────┼────────────────────────────────────────┘ │
│                 │                                           │
└─────────────────┼───────────────────────────────────────────┘
                  │
                  │ File System
                  │
    ┌─────────────┼───────────────────────────────────┐
    │     ┌───────▼─────────────────────────────────┐ │
    │     │  ~/.openclaw/agents/*/sessions/         │ │
    │     │  - main/                                │ │
    │     │  - atlas/                               │ │
    │     │  - luna/                                │ │
    │     │  - ... (12 agents total)                │ │
    │     └─────────────────────────────────────────┘ │
    │                                                 │
    │     ┌─────────────────────────────────────────┐ │
    │     │  AGENT_CONFIG.json (per agent)         │ │
    │     │  - Agent metadata, capabilities,      │ │
    │     │    model preferences, status          │ │
    │     └─────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────┘
```

### 2.3 Multi-Agent Modes

The dashboard will support three modes of operation:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Single-Agent** | View one agent at a time (default) | Focused work on specific agent |
| **Multi-Agent (Selected)** | View 2-4 agents side-by-side | Compare selected agents |
| **Multi-Agent (All)** | View all 12 agents in grid/tile view | System-wide monitoring |

---

## 3. Data Model Design

### 3.1 Agent Registry

**File:** `~/.openclaw/dashboard-multi-agent-index.json`

```json
{
  "version": "1.0",
  "lastUpdated": "2026-02-17T10:12:00.000Z",
  "agents": {
    "main": {
      "id": "main",
      "name": "Main Agent",
      "description": "Primary coordination agent",
      "color": "#6366f1",
      "icon": "⭐",
      "directory": "~/.openclaw/agents/main",
      "status": "active",
      "lastSeen": "2026-02-17T10:10:00.000Z",
      "sessionCount": 42,
      "totalCost": 15.23,
      "modelPreference": "claude-sonnet-4-20250514"
    },
    "atlas": {
      "id": "atlas",
      "name": "Atlas",
      "description": "Deep reasoning specialist",
      "color": "#a855f7",
      "icon": "🧠",
      "directory": "~/.openclaw/agents/atlas",
      "status": "active",
      "lastSeen": "2026-02-17T09:55:00.000Z",
      "sessionCount": 18,
      "totalCost": 8.45,
      "modelPreference": "claude-opus-4-20250514"
    },
    "luna": {
      "id": "luna",
      "name": "Luna",
      "description": "Intuition and pattern matching",
      "color": "#06b6d4",
      "icon": "🌙",
      "directory": "~/.openclaw/agents/luna",
      "status": "idle",
      "lastSeen": "2026-02-17T10:00:00.000Z",
      "sessionCount": 7,
      "totalCost": 3.12,
      "modelPreference": "claude-sonnet-4-20250514"
    },
    /* ... additional agents following same structure ... */
    "orion": {
      "id": "orion",
      "name": "Orion",
      "color": "#3b82f6",
      "icon": "🔭"
    },
    "nova": {
      "id": "nova",
      "name": "Nova",
      "color": "#f59e0b",
      "icon": "💥"
    },
    "zen": {
      "id": "zen",
      "name": "Zen",
      "color": "#10b981",
      "icon": "☯️"
    },
    "flash": {
      "id": "flash",
      "name": "Flash",
      "color": "#ec4899",
      "icon": "⚡"
    },
    "titan": {
      "id": "titan",
      "name": "Titan",
      "color": "#64748b",
      "icon": "🏔️"
    },
    "coder": {
      "id": "coder",
      "name": "Coder",
      "color": "#8b5cf6",
      "icon": "💻"
    },
    "max": {
      "id": "max",
      "name": "Max",
      "color": "#ef4444",
      "icon": "📈"
    },
    "spark": {
      "id": "spark",
      "name": "Spark",
      "color": "#f97316",
      "icon": "✨"
    },
    "vision": {
      "id": "vision",
      "name": "Vision",
      "color": "#14b8a6",
      "icon": "👁️"
    }
  },
  "userPreferences": {
    "defaultAgent": "main",
    "quickAccess": ["main", "atlas", "luna", "coder"],
    "viewMode": "single",
    "enabledAgents": ["main", "atlas", "luna"]
  }
}
```

### 3.2 Per-Agent Session Data Enhancement

Each agent's session directory will maintain the existing structure with additional metadata in `sessions.json`:

**Extended `sessions.json` format:**

```json
{
  "metadata": {
    "agentId": "atlas",
    "agentName": "Atlas",
    "lastIndexed": "2026-02-17T10:12:00.000Z",
    "indexVersion": "1.0"
  },
  "sessions": {
    "telegram-group:main:atlas:abc123": {
      "label": "Planning Sprint #42",
      "sessionId": "abc123-def456-789",
      "agentId": "atlas",
      "modelOverride": "claude-opus-4-20250514",
      "totalTokens": 45230,
      "cost": 2.85,
      "kind": "group",
      "channel": "telegram-group-123",
      "createdAt": "2026-02-17T09:00:00.000Z",
      "updatedAt": "2026-02-17T10:10:00.000Z",
      "status": "running",
      "thinkingLevel": "high",
      "tags": ["planning", "architecture"]
    }
  }
}
```

### 3.3 Cross-Agent Comparative Data

**New file:** `~/.openclaw/dashboard-agent-comparisons.json`

```json
{
  "version": "1.0",
  "lastComputed": "2026-02-17T10:12:00.000Z",
  "timeWindows": {
    "today": {
      "start": "2026-02-17T00:00:00.000Z",
      "costs": {
        "main": 5.23,
        "atlas": 3.45,
        "luna": 0.89,
        /* ... totals per agent ... */
        "_total": 12.50
      },
      "tokens": {
        "main": {
          "input": 450000,
          "output": 125000,
          "cacheRead": 52000,
          "cacheWrite": 18000
        },
        "atlas": {
          "input": 230000,
          "output": 78000,
          "cacheRead": 28000,
          "cacheWrite": 12000
        }
        /* ... */
      },
      "sessionCounts": {
        "main": 8,
        "atlas": 5,
        "luna": 2,
        "_total": 15
      }
    },
    "week": { /* similar structure for weekly data */ },
    "month": { /* similar structure for monthly data */ }
  }
}
```

### 3.4 Agent Health Model

**Health status structure:**

```typescript
interface AgentHealth {
  agentId: string;
  status: 'active' | 'idle' | 'offline' | 'error';
  lastActivity: string;         // ISO timestamp
  uptime: number;               // milliseconds
  recentErrorCount: number;     // last 24 hours
  heartbeat: {
    file: string;               // path to HEARTBEAT.md
    lastModified: string;       // ISO timestamp
    content?: string;           // latest heartbeat content
  };
  sessions: {
    active: number;
    total: number;
  };
  systemMetrics?: {
    cpuPercent: number;
    memoryPercent: number;
    diskPercent: number;
  };
}
```

---

## 4. API Endpoint Design

### 4.1 New Endpoints

All endpoints require authentication (existing `Bearer` token).

#### Agent Registry

```
GET  /api/agents
GET  /api/agents/{agentId}
GET  /api/agents/{agentId}/health
GET  /api/agents/{agentId}/config
POST /api/agents/{agentId}/enable
POST /api/agents/{agentId}/disable
GET  /api/agents/comparivals?window={today|week|month}
```

#### Multi-Agent Session Data

```
GET  /api/sessions?agent={agentId|all}
GET  /api/sessions/compare?agents={agent1,agent2,...}
GET  /api/sessions/{agentId}?id={sessionId}
```

#### Multi-Agent Cost Data

```
GET  /api/costs?agent={agentId|all}
GET  /api/costs/timeline?agents={agent1,agent2,...}&window={today|week|month}
GET  /api/costs/compare?agent1={id}&agent2={id}
```

#### Multi-Agent Live Feed

```
GET  /api/live?agent={agentId|all}
GET  /api/live?agents={agent1,agent2,...}
```

### 4.2 Modified Endpoints

Existing endpoints will be enhanced with optional `agent` query parameter:

```
GET  /api/sessions           -> ?agent=main|atlas|all
GET  /api/usage              -> ?agent=main|atlas|all
GET  /api/costs              -> ?agent=main|atlas|all
GET  /api/crons              -> ?agent=main|atlas|all
GET  /api/lifetime-stats     -> ?agent=main|atlas|all
GET  /api/memory-files       -> ?agent=main|atlas|all
```

### 4.3 API Response Examples

#### GET /api/agents

```json
{
  "agents": [
    {
      "id": "main",
      "name": "Main Agent",
      "status": "active",
      "color": "#6366f1",
      "icon": "⭐",
      "sessionCount": 42,
      "totalCost": 15.23,
      "lastActivity": "2026-02-17T10:10:00.000Z"
    },
    /* ... */
  ],
  "summary": {
    "totalAgents": 12,
    "activeAgents": 5,
    "totalCost": 45.67,
    "totalSessions": 156
  }
}
```

#### GET /api/costs?agent=all

```json
{
  "byAgent": {
    "main": {
      "today": 5.23,
      "week": 32.45,
      "total": 215.67
    },
    "atlas": {
      "today": 3.45,
      "week": 18.90,
      "total": 98.23
    }
    /* ... */
  },
  "aggregated": {
    "today": 14.56,
    "week": 87.34,
    "total": 512.45
  },
  "distribution": [
    { "agent": "main", "percentage": 42.1 },
    { "agent": "atlas", "percentage": 19.2 }
    /* ... */
  ]
}
```

#### GET /api/agents/{agentId}/health

```json
{
  "agentId": "atlas",
  "status": "active",
  "lastActivity": "2026-02-17T10:10:00.000Z",
  "uptime": 86400000,
  "recentErrorCount": 0,
  "heartbeat": {
    "file": "~/.openclaw/agents/atlas/HEARTBEAT.md",
    "lastModified": "2026-02-17T10:10:00.000Z",
    "content": "Atlas active. Processing reasoning request #12345."
  },
  "sessions": {
    "active": 2,
    "total": 18
  },
  "recentErrors": []
}
```

### 4.4 Server-Side Service Layer

New service classes to encapsulate multi-agent logic:

```javascript
// Agent Registry Service
class AgentRegistry {
  constructor() {
    this.registryFile = path.join(OPENCLAW_DIR, 'dashboard-multi-agent-index.json');
    this.registry = {};
    this.lastUpdate = 0;
    this.TTL = 60000; // 1 minute cache
  }

  async loadRegistry() {
    // Load or create registry file
    // Scan ~/.openclaw/agents/ for all agents
    // Populate metadata
  }

  getAgents() { return Object.values(this.registry.agents); }
  getAgent(agentId) { return this.registry.agents[agentId]; }
  async updateAgentStatus(agentId, status) { /* ... */ }
  async markActive(agentId) { /* ... */ }
}

// Multi-Agent Session Service
class MultiAgentSessionService {
  constructor(agentRegistry) {
    this.registry = agentRegistry;
  }

  async getSessions(options = {}) {
    const { agentId = 'main', filters = {} } = options;
    const agents = agentId === 'all' 
      ? this.registry.getAgents()
      : [this.registry.getAgent(agentId)];
    
    // Aggregate sessions across agents
    return sessions;
  }

  async compareAgents(agentIds, metrics = []) {
    // Compare sessions, costs, tokens across agents
  }
}

// Multi-Agent Cost Service
class MultiAgentCostService {
  async getCosts(agentId = 'main', window = 'all') {
    // Aggregate costs by agent and time window
  }

  async getComparativeCosts(agentIds, window) {
    // Return cost comparison data for visualization
  }
}

// Agent Health Monitor
class AgentHealthMonitor {
  async checkAllAgents() {
    // Check heartbeat files for all agents
    // Return health status for each
  }
}
```

---

## 5. UI/UX Recommendations

### 5.1 Agent Switcher Interface

**Location:** Sidebar header with dropdown or dedicated modal

```html
<div class="agent-switcher">
  <button class="agent-switcher-btn" onclick="toggleAgentSelector()">
    <span class="agent-icon" id="currentAgentIcon">⭐</span>
    <span class="agent-name" id="currentAgentName">Main Agent</span>
    <span class="dropdown-arrow">▼</span>
  </button>
  
  <div class="agent-selector-popup" id="agentSelector">
    <div class="agent-search">
      <input type="text" placeholder="Search agents..." />
    </div>
    <div class="agent-list">
      <div class="agent-item active" data-agent="main">
        <span class="agent-status-dot active"></span>
        <span class="agent-icon">⭐</span>
        <span class="agent-name">Main</span>
        <span class="agent-meta">42 sessions</span>
      </div>
      <div class="agent-item" data-agent="atlas">
        <span class="agent-status-dot active"></span>
        <span class="agent-icon">🧠</span>
        <span class="agent-name">Atlas</span>
        <span class="agent-meta">18 sessions</span>
      </div>
      <!-- ... -->
    </div>
    <div class="agent-selector-footer">
      <button class="multi-compare-btn">Compare Selected (2)</button>
    </div>
  </div>
</div>
```

### 5.2 Multi-Agent Health Dashboard

**New Page:** `#agents-health`

```
┌─────────────────────────────────────────────────────────────┐
│                    Health Dashboard                         │
├─────────────────────────────────────────────────────────────┤
│  [Filter: Active All] [View: Grid List]                     │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐  │
│  │ ⭐ Main   │ │ 🧠 Atlas  │ │ 🌙 Luna   │ │ 🔭 Orion  │  │
│  │ ● Active  │ │ ● Active  │ │ ○ Idle    │ │ ○ Idle    │  │
│  │ 5 sessions│ │ 2 sessions│ │ 0 sessions│ │ 1 session │  │
│  │ $5.23/tday│ │ $3.45/tday│ │ $0.89/tday│ │ $1.23/tday│  │
│  │ ↑ 12%     │ │ ↑ 8%      │ │ ↓ 2%      │ │ ↑ 5%      │  │
│  │ [Details] │ │ [Details] │ │ [Details] │ │ [Details] │  │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘  │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐  │
│  │ 💥 Nova   │ │ ☯️ Zen    │ │ ⚡ Flash  │ │ 🏔️ Titan  │  │
│  │○ Offline  │ │ ● Active  │ │ ● Active  │ │ ○ Idle    │  │
│  │ ...       │ │ ...       │ │ ...       │ │ ...       │  │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Agent Comparison View

**New Page:** `#agents-compare`

```
┌─────────────────────────────────────────────────────────────┐
│              Compare Agents: Atlas vs Luna                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Metric                     Atlas      Luna      Difference  │
│  ─────────────────────────────────────────────────────────   │
│  Sessions (today)               5        2       +3         │
│  Total Tokens             45,230    12,450   +32,780       │
│  Cost (today)            $3.45     $0.89    +$2.56         │
│  Avg Response Time        4.2s      5.8s     -1.6s         │
│  Active Now                  2        0       +2           │
│  Errors (24h)                0        0        0           │
│                                                              │
│  [Visual Comparison Charts]                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Token Usage Bar Chart                             │   │
│  │ Atlas: ████████████████████████ 45,230            │   │
│  │ Luna:  ████████████████         12,450            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Enhanced Sessions Table

Existing sessions table will include agent column:

```
┌────┬──────┬─────────────────┬───────┬────────┬────────┬──────┬────────────────────┬─────────┐
│    │ Agent│ Name            │ Type  │ Model  │ Tokens │ Cost │ Last Message       │ Updated │
├────┼──────┼─────────────────┼───────┼────────┼────────┼──────┼────────────────────┼─────────┤
│ ●  │ ⭐    │ Planning #42    │ group │ opus   │ 45,230 │ $2.85│ Reviewing arch...  │ 2m ago  │
│ ●  │ 🧠    │ Deep Reason...  │ sub   │ opus   │ 23,450 │ $1.45│ Synthesizing...   │ 5m ago  │
│ ○  │ 🌙    │ Pattern Match   │ group │ sonnet │ 8,900  │ $0.45│ Completed          │ 1h ago  │
└────┴──────┴─────────────────┴───────┴────────┴────────┴──────┴────────────────────┴─────────┘
```

### 5.5 Multi-Agent Live Feed

Enhanced live feed with agent filtering and color-coding:

```html
<div class="live-feed">
  <div class="feed-controls">
    <div class="agent-filters">
      <label class="agent-filter active" data-agent="all">
        <span>All Agents</span>
      </label>
      <label class="agent-filter" data-agent="main">
        <span class="agent-icon">⭐</span> Main
      </label>
      <label class="agent-filter" data-agent="atlas">
        <span class="agent-icon">🧠</span> Atlas
      </label>
      <label class="agent-filter" data-agent="luna">
        <span class="agent-icon">🌙</span> Luna
      </label>
    </div>
  </div>
  
  <div class="feed-stream">
    <div class="feed-item agent-atlas role-assistant">
      <div class="feed-header">
        <span class="agent-indicator color-purple">🧠 Atlas</span>
        <span class="timestamp">10:12:03</span>
      </div>
      <div class="feed-content">
        Analyzing the architectural patterns...
      </div>
    </div>
    <div class="feed-item agent-main role-user">
      <div class="feed-header">
        <span class="agent-indicator color-indigo">⭐ Main</span>
        <span class="timestamp">10:12:05</span>
      </div>
      <div class="feed-content">
        Please review the multi-agent design proposal.
      </div>
    </div>
  </div>
</div>
```

### 5.6 Cost Allocation View

New cost breakdown page showing per-agent cost distribution:

```
┌─────────────────────────────────────────────────────────────┐
│                    Cost Allocation                         │
│                    Total: $45.67 (This Month)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Pie Chart: Cost Distribution by Agent]                    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Main    42.1% $19.23 ████████████████████████████   │   │
│  │ Atlas   19.2% $8.76  ████████████                   │   │
│  │ Luna    12.8% $5.85  ████████                       │   │
│  │ Orion    8.4% $3.84  ██████                         │   │
│  │ Nova     7.2% $3.29  █████                          │   │
│  │ Others  10.3% $4.70  ███████                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [Trend Chart: Daily Cost by Agent Over Time]                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ $20 ┤     ╭───╮                                       │   │
│  │ $15 ┤   ╭─╯   ╰─╮     ╭───╮                           │   │
│  │ $10 ┤ ╭─╯         ╰───╯   ╰─╮                         │   │
│  │ $5  ┤╯                    ╰───╮                       │   │
│  │ $0  └──────────────────────────────────              │   │
│  │      12  13  14  15  16  17  18  19  20              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.7 Navigation Updates

Sidebar will include new navigation items:

```html
<nav class="nav">
  <!-- Existing items -->
  <div class="nav-item active" data-page="overview">Overview</div>
  <div class="nav-item" data-page="sessions">Sessions</div>
  <div class="nav-item" data-page="costs">Costs</div>
  
  <!-- NEW: Multi-Agent pages -->
  <div class="nav-item" data-page="agents-health">All Agents</div>
  <div class="nav-item" data-page="agents-compare">Compare</div>
  
  <div class="nav-divider"></div>
  
  <!-- Remaining existing items -->
  <div class="nav-item" data-page="limits">Limits</div>
  <!-- ... -->
</nav>
```

---

## 6. Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Server Changes:**
- [ ] Create `AgentRegistry` service class
- [ ] Implement `~/.openclaw/dashboard-multi-agent-index.json`
- [ ] Add agent directory scanning
- [ ] Create basic health check endpoints
- [ ] Add `?agent=` query parameter support to existing endpoints

**Client Changes:**
- [ ] Create `AgentSelector` component
- [ ] Add agent switcher to sidebar header
- [ ] Implement agent context in state management
- [ ] Update page content to show current agent

**Deliverable:** Single-agent dashboard with agent switching capability

### Phase 2: Multi-Agent Data (Week 3)

**Server Changes:**
- [ ] Implement `MultiAgentSessionService`
- [ ] Implement `MultiAgentCostService`
- [ ] Add `/api/agents` endpoints
- [ ] Add `/api/costs?agent=all` support
- [ ] Implement cost aggregation and comparison data

**Client Changes:**
- [ ] Create "All Agents" overview page
- [ ] Add agent columns to sessions table
- [ ] Implement agent filter controls
- [ ] Update cost page to show per-agent breakdown

**Deliverable:** View and filter all agents from one dashboard

### Phase 3: Visualization and Comparison (Week 4)

**Server Changes:**
- [ ] Add `/api/agents/comparivals` endpoint
- [ ] Implement cross-agent statistics
- [ ] Optimize multi-agent query performance

**Client Changes:**
- [ ] Create Agent Health Dashboard page
- [ ] Create Agent Comparison page
- [ ] Implement comparison charts and metrics
- [ ] Add visual agent status indicators

**Deliverable:** Full multi-agent visualization and comparison

### Phase 4: Live Monitoring (Week 5)

**Server Changes:**
- [ ] Enhance SSE (Server-Sent Events) for multi-agent live feed
- [ ] Implement per-agent file watchers
- [ ] Add event source filtering

**Client Changes:**
- [ ] Update Live Feed page for multi-agent
- [ ] Add agent filtering to live feed
- [ ] Color-code events by agent
- [ ] Add per-agent activity indicators

**Deliverable:** Real-time monitoring of all agents

### Phase 5: Polish and Optimization (Week 6)

**All Areas:**
- [ ] Add caching layer for multi-agent queries
- [ ] Implement data pagination for large datasets
- [ ] Add user preferences for default agent view
- [ ] Performance optimization and testing
- [ ] Documentation updates
- [ ] Error handling improvements

**Deliverable:** Production-ready multi-agent dashboard

---

## 7. Performance Considerations

### 7.1 Caching Strategy

| Data Type | Cache Duration | Invalidation |
|-----------|----------------|--------------|
| Agent Registry | 60 seconds | Agent directory changes |
| Session Lists | 30 seconds | New sessions detected |
| Cost Data | 60 seconds | Aggregated computation |
| Health Status | 5 seconds | Heartbeat file changes |
| Live Feed Events | Real-time | SSE (no caching) |

### 7.2 Query Optimization

**Problems to solve:**
1. Scanning 12 agent directories for session files is expensive
2. Aggregating costs across all agents requires parsing many JSONL files
3. Real-time health checks on all agents could be slow

**Solutions:**

1. **Index File Caching**
   - Maintain pre-computed `sessions.json` index per agent
   - Cache aggregated session list in memory (30s TTL)

2. **Incremental Cost Computation**
   - Track last-scanned position per agent
   - Only parse new/modified JSONL lines
   - Persist computed totals to registry

3. **Lazy Health Loading**
   - Health status computed on-demand per agent
   - Background periodic refresh (every 5s)
   - Cache results in memory

4. **Streaming Large Results**
   - Use pagination for sessions list (limit 50)
   - Stream SSE events instead of bulk polling
   - Server-side filtering before data transfer

### 7.3 File System Efficiency

```javascript
// Efficient multi-agent directory scanner
class AgentDirectoryScanner {
  constructor() {
    this.lastScanCache = new Map(); // agentId -> file list + mtime
    this.scanInterval = 30000; // 30 seconds
  }

  async scanAgents(agentIds) {
    const results = {};
    for (const agentId of agentIds) {
      const agentDir = this.getAgentDirectory(agentId);
      const cached = this.lastScanCache.get(agentId);
      
      // Check if cache is still valid (directory unchanged)
      if (cached && this.isCacheValid(agentDir, cached)) {
        results[agentId] = cached.files;
        continue;
      }
      
      // Perform actual scan
      const files = await this.scanDirectory(agentDir);
      this.lastScanCache.set(agentId, {
        files,
        mtime: await this.getDirectoryMtime(agentDir)
      });
      results[agentId] = files;
    }
    return results;
  }
}
```

### 7.4 Memory Management

- Limit concurrent file watchers (max 12 agents)
- Cache key results in memory with TTL
- Use streaming JSON parsing for large JSONL files
- Implement connection pooling for SSE clients
- Clear inactive session caches after 5 minutes

---

## 8. Security Considerations

### 8.1 Agent Access Control

**Proposed agent-level permissions:**

| Role | View Single | View All | Compare | Cost Data |
|------|-------------|----------|---------|-----------|
| Admin | ✓ | ✓ | ✓ | ✓ |
| User | ✓ | ✗ | ✗ | Single only |
| Viewer | ✓ | ✗ | ✗ | Single only |

**Implementation:**

```javascript
function canUserAccessAgent(user, agentId, action) {
  if (user.role === 'admin') return true;
  
  // Regular users can only access their assigned agent
  if (action === 'view-single') {
    return user.assignedAgent === agentId;
  }
  
  // Multi-agent actions require admin
  return false;
}
```

### 8.2 Data Isolation

- Each agent's session data remains in its own directory
- No cross-agent file access
- Cost data aggregated and computed server-side
- Session IDs include agent prefix to prevent conflicts

### 8.3 Audit Trail

Extend existing audit logging:

```json
{
  "timestamp": "2026-02-17T10:12:00.000Z",
  "event": "agent_switch",
  "ip": "127.0.0.1",
  "userId": "admin",
  "details": {
    "fromAgent": "main",
    "toAgent": "atlas",
    "mode": "single"
  }
}
```

### 8.4 API Rate Limiting

Maintain existing rate limiting and add multi-agent considerations:

```javascript
// Enhanced rate limiting for multi-agent queries
function checkMultiAgentRateLimit(ip, agentCount) {
  // More agents queried = higher cost, stricter limits
  const baseLimit = 20; // base requests per 15 min
  const multiplier = Math.max(1, Math.floor(agentCount / 3));
  return baseLimit / multiplier;
}
```

---

## Appendix A: Agent Configuration Template

**File:** `~/.openclaw/agents/{agentId}/AGENT_CONFIG.json`

```json
{
  "agentId": "atlas",
  "name": "Atlas",
  "description": "Deep reasoning specialist",
  "version": "1.0.0",
  "created": "2026-01-15T00:00:00.000Z",
  "preferences": {
    "defaultModel": "claude-opus-4-20250514",
    "thinkingLevel": "high",
    "maxTokens": 200000,
    "temperature": 0.7
  },
  "capabilities": [
    "deep-reasoning",
    "architecture-design",
    "code-review",
    "system-analysis"
  ],
  "limits": {
    "dailyCost": 50.00,
    "monthlyCost": 500.00,
    "maxSessions": 100
  },
  "notifications": {
    "costAlert": {
      "enabled": true,
      "threshold": 40.00,
      "channel": "telegram"
    },
    "errorAlert": {
      "enabled": true,
      "channel": "telegram"
    }
  }
}
```

## Appendix B: Testing Checklist

### Unit Tests
- [ ] AgentRegistry service methods
- [ ] MultiAgentSessionService aggregation
- [ ] MultiAgentCostService calculations
- [ ] AgentHealthMonitor status detection

### Integration Tests
- [ ] Multi-agent session retrieval
- [ ] Cross-agent cost aggregation
- [ ] Agent switching workflow
- [ ] SSE streaming from multiple agents

### UI Tests
- [ ] Agent selector dropdown
- [ ] Agent filter controls
- [ ] Comparison view rendering
- [ ] Live feed agent filtering

### Performance Tests
- [ ] Query all agents response time < 2s
- [ ] Cost aggregation for all agents < 3s
- [ ] Memory usage with 12 agent watchers
- [ ] SSE handling with multiple concurrent clients

---

## Appendix C: Backward Compatibility Checklist

- [ ] Single-agent deployments (no other agents exist) work unchanged
- [ ] `OPENCLAW_AGENT` environment variable still respected
- [ ] Existing `sessions.json` files remain compatible
- [ ] No breaking changes to current API endpoints
- [ ] Existing authentication/authorization unchanged
- [ ] UI defaults to single-agent mode for simplicity

---

## Conclusion

This architecture provides a comprehensive foundation for multi-agent support in the OpenClaw Dashboard while maintaining backward compatibility and focusing on performance, security, and usability.

The phased implementation approach allows for incremental delivery of features, with each phase building on the previous one. Key to success will be:

1. **Proper caching strategy** to avoid expensive file system operations
2. **Graceful degradation** when agents are offline or inactive  
3. **Intuitive UI** that doesn't overwhelm users with multi-agent data
4. **Robust error handling** given the distributed nature of agent data

---

**Next Steps:**
1. Review and approve this architecture design
2. Create detailed task breakdown for Phase 1
3. Set up development/testing environment
4. Begin Phase 1 implementation

---

*Document prepared by Atlas - Deep Reasoning Specialist*
*Last updated: 2026-02-17*
