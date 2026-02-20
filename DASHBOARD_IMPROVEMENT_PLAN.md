# Dashboard Improvement Plan

## Research Summary

Based on analysis of leading multi-agent observability tools (Langfuse, Azure Agent Factory, ServiceNow AI Agent Dashboard), here are the key features needed:

### What Leaders Have (Langfuse, Azure, etc.)

1. **Agent Graph Visualization**
   - Visual representation of agent workflows
   - Shows multi-step reasoning processes
   - Displays agent-to-agent handoffs

2. **Real-Time Observability**
   - Trace each agent flow with full execution context
   - Latency tracking per step
   - Cost tracking per agent/call
   - Error rate monitoring

3. **Multi-Agent Dashboard Features**
   - Agent status cards (active/idle/error)
   - Session count per agent
   - Model assignment display
   - Quick agent selection for chat

4. **Chat Interface**
   - Direct chat with any agent
   - Spawn child agents from chat
   - Message history

5. **Evaluation & Testing**
   - Performance benchmarks
   - Custom evaluation metrics
   - A/B testing capabilities

---

## Current State Analysis

### ✅ Already Implemented
- [x] Agent discovery (reads from ~/.openclaw/agents/)
- [x] Agent metadata (icons, colors, descriptions)
- [x] Session counting
- [x] Cost tracking
- [x] Multi-agent grid UI
- [x] Chat interface
- [x] Child agent spawning

### ⚠️ Needs Improvement
- [ ] Agent graph visualization (workflow diagrams)
- [ ] Real-time traces (step-by-step execution)
- [ ] Error tracking dashboard
- [ ] Agent comparison view
- [ ] Performance metrics (latency, success rate)
- [ ] Better login UX (explain why agents aren't showing)

### ❌ Missing
- [ ] Agent-to-agent handoff visualization
- [ ] Workflow builder/visualizer
- [ ] Evaluation framework
- [ ] Alert configuration
- [ ] Export/sharing capabilities

---

## Improvement Phases

### Phase 1: UX Quick Wins (1 day)
1. **Fix Login Flow**
   - Add onboarding message explaining registration
   - Show agent count on login screen
   - Add "demo mode" preview

2. **Improve Agent Cards**
   - Add model badge (e.g., "GLM-5", "Kimi K2.5")
   - Add last activity timestamp
   - Add quick action buttons (chat, view sessions)

3. **Add Agent Status Legend**
   - Active (green) = activity in last hour
   - Idle (yellow) = activity in last 24h
   - Offline (gray) = no recent activity

### Phase 2: Observability (2 days)
1. **Add Traces Tab**
   - Show last 50 agent interactions
   - Display step-by-step execution
   - Add timing per step

2. **Add Metrics Dashboard**
   - Total cost per agent (today/week/month)
   - Average latency per agent
   - Success rate (%)
   - Token usage charts

3. **Add Error Tracking**
   - Recent errors list
   - Error rate per agent
   - Stack traces

### Phase 3: Advanced Features (3 days)
1. **Agent Graph Visualization**
   - Use Mermaid.js or D3 for workflow diagrams
   - Show multi-agent collaboration
   - Display decision points

2. **Comparison View**
   - Side-by-side agent comparison
   - Cost/latency/accuracy benchmarks

3. **Workflow Builder**
   - Drag-and-drop agent composition
   - Define handoff rules
   - Save workflow templates

---

## Recommended Tech Stack

| Feature | Tool | Why |
|---------|------|-----|
| Graphs | Mermaid.js | Lightweight, built-in to many tools |
| Charts | Chart.js | Simple, beautiful |
| Real-time | WebSocket | Live updates |
| Metrics | Custom JSON | No external dependency |

---

## Immediate Actions

1. **Update Dashboard UI** - Show agent count before login
2. **Add Model Badges** - Display model per agent
3. **Add Quick Actions** - Chat button on agent cards
4. **Fix Navigation** - Clear Multi-Agent page access

---

## References

- Langfuse Agent Observability: https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse
- Azure Agent Factory: https://azure.microsoft.com/en-us/blog/agent-factory-top-5-agent-observability-best-practices-for-reliable-ai/
- Fuselab AI Agent UI Design: https://fuselabcreative.com/ui-design-for-ai-agents/
