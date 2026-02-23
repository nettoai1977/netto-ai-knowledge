# Minimal Skills Configuration

**Date:** 2026-02-23
**Purpose:** Performance optimization - reduce token overhead from 860+ skills to ~10 essential skills

---

## Essential Skills (Keep Active)

### Trading System
```json
{
  "name": "trading",
  "location": "~/.openclaw/workspace/trading",
  "description": "Multi-timeframe trading system with trailing TP"
}
```

### Research & Search
```json
{
  "name": "youtube-transcript",
  "location": "~/.openclaw/skills/youtube-transcript",
  "description": "Extract transcripts from YouTube videos"
}
```

### Browser Automation
```json
{
  "name": "agent-browser",
  "location": "~/.agents/skills/agent-browser",
  "description": "Browser automation for web scraping and interaction"
}
```

### Development
```json
{
  "name": "coding-agent",
  "location": "~/.agents/skills/coding-agent",
  "description": "Delegate coding tasks to specialized agents"
}
```

---

## Tools (Always Available)

These are built-in tools that don't need skill files:
- `web_search` - Brave Search API
- `web_fetch` - Content extraction
- `browser` - Native browser control
- `exec` - Shell commands
- `read/write/edit` - File operations
- `cron` - Scheduling
- `message` - Messaging
- `nodes` - Device control

---

## Archived Skills (Moved to Knowledge Base)

All 850+ other skills have been archived to:
`~/netto-ai-knowledge/skills-archive/`

To re-enable a skill:
1. Find the skill in the archive
2. Add it to `~/.openclaw/openclaw.json` in the `skills` array
3. Restart OpenClaw

---

## Performance Impact

| Metric | Before | After |
|--------|--------|-------|
| Active Skills | 860+ | ~10 |
| Token Overhead | High | Minimal |
| Response Speed | Slower | Faster |
| Decision Complexity | High | Low |

---

*Created by Netto.AI on 2026-02-23*
