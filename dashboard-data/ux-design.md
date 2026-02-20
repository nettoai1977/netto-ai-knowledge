# Multi-Agent Dashboard: UX Design Document

## Overview

This document outlines the user experience design for a multi-agent dashboard supporting up to 12 simultaneous agents. The design prioritizes clarity, efficiency, and scalability while avoiding cognitive overload.

---

## 1. Agent Selection Interface

### 1.1 Primary Selector: The Agent Rail

A persistent vertical sidebar on the left edge of the screen containing all 12 agent slots.

```
┌─────────────────────────────────────────────────────────────┐
│ ┌───┐  ┌─────────────────────────────────────────────────┐ │
│ │ 🎭│  │                                                 │ │
│ ├───┤  │                                                 │ │
│ │ ⏵ │  │                                                 │ │
│ ├───┤  │                                                 │ │
│ │ ○ │  │                 MAIN VIEWPORT                   │ │
│ ├───┤  │                                                 │ │
│ │ ○ │  │                                                 │ │
│ ├───┤  │                                                 │ │
│ │ ○ │  │                                                 │ │
│ ├───┤  └─────────────────────────────────────────────────┘ │
│ │ ▼ │  ┌─────────────────────────────────────────────────┐ │
│ ├───┤  │           CONTEXT / DETAILS PANEL               │ │
│ │ + │  └─────────────────────────────────────────────────┘ │
│ └───┘                                                      │
└─────────────────────────────────────────────────────────────┘
```

**Design Specifications:**
- **Width:** 56px collapsed (icon only), 200px expanded (icon + name + status)
- **Agent Icons:** 40x40px circular avatars with status indicators
- **Status Indicators:**
  - Green dot: Active and healthy
  - Yellow dot: Degraded/warning
  - Red dot: Error/failed
  - Gray dot: Idle/offline
  - Blue pulse: Currently selected

**Each Agent Card (Expanded View):**
```
┌─────────────────────────┐
│ [Icon] Name      [●]   │  ← Name truncated to 16 chars with ellipsis
│ Model: gpt-4      ◐    │  ← Circular progress for token usage
│ Task: summarizing      │  ← Current activity (optional)
└─────────────────────────┘
```

### 1.2 Grouping & Organization

Agents are automatically grouped by:

1. **Status-Based Grouping:**
   - Active agents (currently processing)
   - Standby agents (healthy but idle)
   - Warning/Error agents (need attention)

2. **User-Defined Groups (Optional):**
   - "Research Team"
   - "Code Reviewers"
   - "Creative Writers"
   - "Production Agents"

### 1.3 Quick Actions on Hover

Hovering over an agent reveals a contextual menu:
- Pin/Unpin (keep at top)
- Pause/Resume
- Settings
- Duplicate
- Delete

---

## 2. Multi-Agent Overview Screen

### 2.1 Dashboard Layout: "Command Center" View

A bird's-eye view showing all 12 agents in a grid.

```
┌──────────────────────────────────────────────────────────────────┐
│ AGENT DASHBOARD                    [Grid ▼] [Filter ▼] [🔍]    │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┤
│      │      │      │      │      │      │      │      │      │
│ AGT1 │ AGT2 │ AGT3 │ AGT4 │ AGT5 │ AGT6 │ AGT7 │ AGT8 │ AGT9 │
│ [●]  │ [●]  │ [●]  │ [●]  │ [●]  │ [●]  │ [●]  │ [●]  │ [●]  │
│ ●●●  │ ○○○  │ ●●○  │ ●●●  │ ○○○  │ ●○○  │ ●●●  │ ●●●  │ ○○○  │
│      │      │      │      │      │      │      │      │      │
├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┤
│ AGT10  │ AGT11  │ AGT12                                      │
│ [●]    │ [●]    │ [●]                                        │
│ ●●●    │ ○○○    │ ●●○                                        │
├──────────────────────────────────────────────────────────────────┤
│ HEALTH SUMMARY: [████████░░] 10/12 healthy │ 2 warnings       │
└──────────────────────────────────────────────────────────────────┘
```

**Card Contents (Per Agent):**
- Avatar + Name (truncated)
- Status badge (icon + text)
- Last activity timestamp
- Token usage bar (0-100%)
- Quick action buttons (pause/resume icon)
- Contextual glow border:
  - Blue: Currently selected
  - Green: Healthy
  - Yellow: Warning
  - Red: Error

### 2.2 Alternative Views

**List View:**
- Better for detailed monitoring
- Columns: Name | Status | Model | Last Activity | Tokens Used | Actions

**Mini View:**
- Compact rows for high-density display
- Minimalist: Icon | Name | Status Dot

**Network View:**
- Shows agent interconnections
- Useful for workflows where agents communicate

---

## 3. Agent Switching Mechanism

### 3.1 Primary: Click-to-Switch

**Single Click:** Select agent, show in main viewport
**Double Click:** Select agent AND expand to full detail view

### 3.2 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` / `Shift+Tab` | Navigate between agents in rail |
| `1` - `=` | Jump to agent 1-12 (top row keys) |
| `Cmd+1` - `Cmd+=` | Switch to specific agent |
| `Cmd+[` / `Cmd+]` | Previous/Next agent |
| `Cmd+W` | Close/detach current agent view |
| `Option+Click` | Open agent in split view |

### 3.3 Quick Switch Mode

Press `Cmd+K` (or `Ctrl+K`) to open:

```
┌─────────────────────────────────────┐
│  >                                  │
├─────────────────────────────────────┤
│  Quick Switch                       │
│  ─────────────────────────────────  │
│  🎭 Nova (Research Agent)     ⌘1    │
│  💬 Echo (Chat Assistant)     ⌘2    │
│  🔍 Scout (Web Search)        ⌘3    │
│  📝 Scribe (Documentation)    ⌘4    │
│  ─────────────────────────────────  │
│  ⚠️ Pulse (Encoder - Warning) ⌘5    │
│  ⏸️  Sleep (Paused)           ⌘6    │
└─────────────────────────────────────┘
```

### 3.4 Persistent State

- Selected agent persists across sessions
- Each agent maintains its own scroll position
- Split view layouts are remembered

---

## 4. User Workflows

### 4.1 Workflow: Daily Monitoring

**Scenario:** User wants to check agent status quickly

```
1. User opens dashboard
   └─> Sees Overview (all 12 agents in grid)
   
2. Scans for visual cues:
   ├─> Red borders → click to investigate
   ├─> Yellow pulse → expand details
   └─> Green → all good
   
3. User clicks warning agent
   └─> Rail highlights agent
   └─> Main view shows agent details
   └─> Error log visible
   
4. User resolves issue
   └─> Status updates in real-time
   └─> Notification sent (optional)
```

### 4.2 Workflow: Comparative Analysis

**Scenario:** User wants to compare 3 agents side-by-side

```
1. User selects agent from rail (single click)
   └─> Agent opens in main viewport
   
2. User Cmd+clicks 2 more agents
   └─> Agents open in split view
   
3. View automatically adjusts to 3-column layout
   ├─> Agent 1 │ Agent 2 │ Agent 3
   └─> Shared metrics displayed below
   
4. User can scroll each independently
   └─> Sync scroll option available
```

### 4.3 Workflow: Batch Operations

**Scenario:** User needs to restart 5 agents

```
1. User enables "Selection Mode" (toggle or Cmd)
2. Checkboxes appear on agent cards
3. User selects 5 agents
4. Contextual toolbar appears at bottom:
   ┌─────────────────────────────────┐
   │ 5 selected  [Restart] [Delete]  │
   └─────────────────────────────────┘
5. User confirms action
6. Batch progress shown in modal
```

### 4.4 Workflow: Agent Onboarding

**Scenario:** User wants to add a new agent

```
1. User clicks "+" in rail
2. Presents: Templates │ Custom
3. User selects template
   ├─> Name field (auto-suggested)
   ├─> Model selector
   ├─> Role description
   └─> Initial instructions
4. User configures
5. "Add Agent" button creates
6. New agent appears in rail
7. Auto-switches to new agent view
```

---

## 5. Agent Comparison View

### 5.1 Comparison Interface

When 2-4 agents are selected for comparison:

```