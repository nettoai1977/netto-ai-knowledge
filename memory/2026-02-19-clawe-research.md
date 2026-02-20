# HEARTBEAT LOG - 2026-02-19 1:13 PM

## Clawe Multi-Agent Coordination System Research

### Repository: getclawe/clawe
**URL:** https://github.com/getclawe/clawe
**Type:** Multi-agent coordination layer built on top of OpenClaw
**Analogy:** "Trello for OpenClaw agents"

---

### Key Features Identified

| Feature | Description |
|---------|-------------|
| **Agent Gateway** | Runs multiple agents with distinct roles & personalities |
| **Scheduled Heartbeats** | Agents wake on cron schedules (default every 15 min, staggered) |
| **Kanban Task Board** | Visual task management with drag-and-drop UI |
| **Instant Notifications** | @mentions deliver updates in near real-time |
| **Agent CLI** | Commands: `clawe task:status`, `clawe notify`, `clawe squad`, `clawe feed` |
| **Web Dashboard** | Squad status, task board, agent chat at http://localhost:3000 |
| **Shared Backend** | Convex backend (real-time database) for state management |
| **Routines** | Scheduled recurring tasks with 1-hour trigger windows |

---

### Pre-Configured Squad

| Agent | Emoji | Role | Heartbeat |
|-------|-------|------|-----------|
| Clawe | 🦞 | Squad Lead | Every 15 min |
| Inky | ✍️ | Content Editor | Every 15 min |
| Pixel | 🎨 | Designer | Every 15 min |
| Scout | 🔍 | SEO | Every 15 min |

**Design:** Staggered heartbeats to avoid API rate limits

---

### Architecture

```
┌─────────────────────────────────────────┐
│ DOCKER COMPOSE                          │
├─────────────┬────────────┬──────────────┤
│ squadhub    │ watcher    │ clawe (web)  │
│ (4 agents)  │ (cron +    │ Kanban UI    │
│             │  notifs)    │ + chat       │
└──────┬──────┴──────┬─────┴──────┬───────┘
       │             │            │
       └─────────────┼────────────┘
                     │
             ┌───────▼────────┐
             │ CONVEX Backend │
             │ • Tasks       │
             │ • Activities  │
             │ • Notifications│
             └────────────────┘
```

---

### Comparison: Current Setup vs Clawe

| Aspect | Current (OpenClaw) | Clawe |
|--------|-------------------|-------|
| **Agents** | 12 (1 Main + 11 specialists) | 4 pre-configured (expandable) |
| **Task Management** | Manual (sessions_spawn) | Kanban board with drag-and-drop |
| **Scheduling** | Cron jobs | Heartbeat per agent + routines |
| **Dashboard** | List view + session tracking | Visual task board + agent chat |
| **Notifications** | Sub-agent reporting | @mentions + instant delivery |
| **Backend** | File-based (JSON/JSONL) | Convex (real-time db) |
| **CLI Commands** | OpenClaw CLI | Custom `clawe` CLI with task mgmt |
| **Agent Workspace** | Agent directories | Isolated workspace templates |

---

### Agent Workspace Structure (Clawe)

Each agent gets standard workspace files:

```
/data/workspace-{agent}/
├── AGENTS.md      # Instructions and conventions
├── SOUL.md        # Agent identity and personality
├── USER.md        # Info about the human they serve
├── HEARTBEAT.md   # What to do on each wake
├── MEMORY.md      # Long-term memory
├── TOOLS.md       # Local tool notes
└── shared/        # Symlink to shared state
    ├── WORKING.md # Current team status
    └── WORKFLOW.md# Standard operating procedures
```

**Observation:** Similar to current OpenClaw setup, but Clawe standardizes it.

---

### Installation Requirements

**Prerequisites:**
- Docker & Docker Compose
- Convex account (free tier available)
- Anthropic API key (❌ different from NVIDIA!)

**Quick Start:**
```bash
git clone https://github.com/getclawe/clawe.git
cd clawe
cp .env.example .env

# Edit .env
ANTHROPIC_API_KEY=sk-ant-...
SQUADHUB_TOKEN=your-secure-token
CONVEX_URL=https://your-deployment.convex.cloud

# Deploy
pnpm install
cd packages/backend
npx convex deploy

# Start production stack
./scripts/start.sh
```

---

### Key Differences

| Aspect | Current Stack | Clawe Stack |
|--------|--------------|-------------|
| **Models** | NVIDIA + Groq (FREE) | Anthropic only (paid) |
| **Backend** | File-based (flat files) | Convex (real-time db) |
| **Auth** | Custom (token-based) | Convex auth + SQUADHUB_TOKEN |
| **Deployment** | Local Node.js | Docker Compose |
| **Task System** | Session-based | Kanban board + routines |

---

### Integration Options

#### Option 1: Run Alongside (Recommended)
Keep existing OpenClaw setup, use Clawe for:
- Visual task tracking UI
- Agent collaboration chat
- Scheduled routines
- Extract useful CLI commands

#### Option 2: Extend Clawe
- Fork repository
- Add all 11 specialists to agent config
- Use Clawe's architecture for full agent army

#### Option 3: Extract Features
- Copy Kanban UI concepts to existing dashboard
- Implement agent CLI commands
- Add heartbeat schedule concept to cron jobs
- Add workspace templates to existing agents

---

### Valuable Takeaways

1. **Kanban UI Pattern:** Drag-and-drop task board is valuable for multi-agent coordination
2. **Heartbeat Schedules:** Staggered cron schedules prevent rate limits
3. **Agent CLI:** Specialized commands (`clawe task:status`, `clawe notify`) improve agent functionality
4. **Workspace Standardization:** Uniform workspace structure aids agent understanding
5. **Routines:** Scheduled recurring tasks with trigger windows provide crash tolerance

---

### Recommended Next Steps

1. **Clone Clawe locally** to explore the demo
2. **Review agent workspace templates** for best practices
3. **Consider adding CLI commands** to current agents
4. **Evaluate Kanban UI** for dashboard improvement
5. **Document agent coordination patterns** from Clawe's implementation

---

### Session Status Update

During this heartbeat check, discovered:
- Main agent: 1 session (agent:main:main)
- Specialist agents: 0 sessions each (atlas, luna, orion, nova, zen, flash, titan, coder, max, spark, vision)

**Observation:** Earlier test sessions (via sessions_spawn) may not persist in sessions.json format. The sub-agent spawn system appears to create ephemeral sessions for task execution.

---

**Heartbeat Summary:**
- ✅ System Health: All APIs working, context 49% optimal
- ✅ Knowledge Management: Memory files current (no files >7 days old)
- ✅ Productivity: Clawe research provides valuable insights for multi-agent coordination
- ⏳ Agent Army: Session tracking discrepancy noted (sub-agent vs persistent sessions)

---

**Context:** 99k/200k (49%) - Optimal
