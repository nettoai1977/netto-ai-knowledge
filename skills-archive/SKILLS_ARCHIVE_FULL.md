# Skills Archive - Full Inventory

**Exported:** 2026-02-23 22:45 NZT
**Total Skills:** 860+
**Reason:** Performance optimization - reducing context bloat

---

## Skills to KEEP (Active)

### Trading
- `market-matrix.js` - Multi-timeframe scanner (local)
- `paper_executor.js` - Position monitoring (local)
- `paper_executor_v2.js` - Risk-managed executor (local)
- `trailing_tp.js` - Profit protection (local)
- `binance_api.py` - Binance testnet integration (local)

### Research
- `web_search` - Brave Search API (built-in)
- `web_fetch` - Content extraction (built-in)

### Browser
- `browser` - Native browser control (built-in)
- `agent-browser` - Advanced automation skill

### YouTube
- `youtube-transcript` - Transcript extraction

---

## Skills to ARCHIVE (Available on-demand)

### AI & API
- 1password
- agents-sdk
- api-provider-setup
- gemini
- gemini-api-dev
- oracle
- openai-whisper

### Documentation & Notes
- apple-notes
- apple-reminders
- bear-notes
- docx
- obsidian
- pdf
- pptx
- xlsx

### Development
- algorithmic-art
- canvas-design
- clawhub
- coding-agent
- durable-objects
- frontend-design
- hugging-face-cli
- hugging-face-datasets
- hugging-face-evaluation
- hugging-face-jobs
- hugging-face-model-trainer
- hugging-face-paper-publisher
- hugging-face-tool-builder
- hugging-face-trackio
- mcp-builder
- building-mcp-server-on-cloudflare
- web-artifacts-builder
- webapp-testing
- wrangler

### Media & Audio
- fal-audio
- fal-generate
- fal-image-edit
- fal-upscale
- gifgrep
- songsee
- video-frames

### Business & Productivity
- blogwatcher
- eightctl
- gh-issues
- gog
- healthcheck
- himalaya
- mcporter
- nano-pdf
- ordercli

### Home & Devices
- blucli
- openhue
- sonoscli

### Communication
- discord
- imsg
- slack-gif-creator
- wacli

### System & Monitoring
- peekaboo
- session-logs
- tmux
- weather

### User-Created Skills
- skill-creator
- theme-factory

---

## How to Restore Skills

1. **From ClawHub:** `clawhub install <skill-name>`
2. **From Archive:** Copy from `~/netto-ai-knowledge/skills-archive/`
3. **Manual:** Add to `~/.openclaw/openclaw.json` under `skills`

---

## Performance Impact

**Before cleanup:**
- Skills loaded: 860+
- Estimated token cost: ~50,000+ tokens per session
- Decision overhead: High

**After cleanup:**
- Skills loaded: 9 essential
- Estimated token cost: ~5,000 tokens
- Decision overhead: Minimal

**Expected improvement:** 10x faster decision-making, 90% token reduction

---

*This archive preserves all skills for future restoration.*
