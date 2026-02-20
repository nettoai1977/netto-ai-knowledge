# SYSTEM RECOVERY PLAN
**Generated:** February 19, 2026 - 12:45 AM
**Purpose:** Emergency rollback procedures
**Status:** Active safeguards in place

---

## 🛡️ RECOVERY PLAN: Rolling Back Changes

### What This Plan Covers
1. Configuration file backups
2. Gateway rollback procedures
3. Model provider restoration
4. Agent army reset
5. Emergency diagnostic commands

---

## 📂 CRITICAL BACKUPS

### 1. Configuration Backup (BEFORE CHANGES)

**Timestamp:** 2026-02-19 00:45 GMT+13

**Backup Created:**
```bash
# Main config backup
cp ~/.openclaw/openclaw.json ~/.openclaw/backup/openclaw.json.backup-$(date +%Y%m%d-%H%M%S)

# Workspace backup
cp ~/.openclaw/workspace/TODO.md ~/.openclaw/backup/TODO.md.backup-$(date +%Y%m%d-%H%M%S)
cp ~/.openclaw/workspace/AGENT_ARMY_KNOWLEDGE.md ~/.openclaw/backup/AGENT_ARMY_KNOWLEDGE.md.backup-$(date +%Y%m%d-%H%M%S)
```

### 2. Current System Baseline

**Providers Configuration:**
- NVIDIA: 6 models, working ✅
- Groq: 6 models, 1 transient error (401) ✅
- OpenRouter: 1 model, working ✅
- Cloudflare: 4 models, just added, tested ✅
- **Total:** 17 models across 4 providers

**Agent Army Status:**
- 11 specialist agents + main
- All operational
- Session stores clean

**Gateway Status:**
- Running: port 18789
- Last restart: ~12 hours ago
- Health: OK

---

## 🔄 ROLLBACK PROCEDURES

### Procedure 1: Gateway Configuration Rollback

**If configuration becomes invalid:**

```bash
# Stop gateway
pkill -f "openclaw gateway" || true

# Restore main config
cp ~/.openclaw/backup/openclaw.json.backup-YEARMMDD-HHMMSS ~/.openclaw/openclaw.json

# Verify JSON syntax
cat ~/.openclaw/openclaw.json | jq empty

# Restart gateway
openclaw gateway restart

# Verify health
curl http://localhost:18789/api/health
```

### Procedure 2: Remove New Provider If Fails

**If Cloudflare causes issues:**

```bash
# Stop gateway
pkill -f "openclaw gateway" || true

# Remove cloudflare provider from config
# Edit openclaw.json, remove the "cloudflare" section from providers

# Restart
openclaw gateway restart

# Verify doctors pass
openclaw doctor --non-interactive
```

### Procedure 3: Reset Agent Workspaces

**If agent behavior becomes unstable:**

```bash
# Stop gateway
pkill -f "openclaw gateway" || true

# Clear all agent sessions (preserves config)
rm -rf ~/.openclaw/agents/*/sessions/*.json

# Clear memory (optional - resets learning)
rm -f ~/.openclaw/agents/*/memory/*.db

# Restart
openclaw gateway restart

# Verify health
openclaw doctor --non-interactive
```

---

## 🚨 EMERGENCY DIAGNOSTIC COMMANDS

### Check System Health

```bash
# Gateway status
openclaw doctor --non-interactive

# Gateway health endpoint
curl http://localhost:18789/api/health

# List all models
openclaw models list

# List all agents
openclaw agents list

# Session status
ls -la ~/.openclaw/agents/*/sessions/
```

### Check Provider Status

```bash
# NVIDIA API
curl -s -o /dev/null -w "NVIDIA: %{http_code}\n" https://integrate.api.nvidia.com/v1/models

# Groq API
curl -s -o /dev/null -w "Groq: %{http_code}\n" https://api.groq.com/openai/v1/models

# OpenRouter API
curl -s -o /dev/null -w "OpenRouter: %{http_code}\n" https://openrouter.ai/api/v1/models

# Cloudflare API (token from config)
curl -s https://api.cloudflare.com/client/v4/user/tokens/verify \
  -H "Authorization: Bearer gcMntOA243NeDPHlDL39XuWrzrlY5dsALh-AqRtE"
```

### Test Model Functionality

```bash
# Test main model (nvidia/z-ai/glm5)
openclaw agent message "What is 2+2?" --model nvidia/z-ai/glm5

# Test Cloudflare model
curl --request POST \
  --url https://api.cloudflare.com/client/v4/accounts/a73b1087139d3cd7ad5d35a9b077d534/ai/v1/chat/completions \
  --header "Authorization: Bearer gcMntOA243NeDPHlDL39XuWrzrlY5dsALh-AqRtE" \
  --header "Content-Type: application/json" \
  --data '{"model": "@cf/openai/gpt-oss-120b", "messages": [{"role": "user", "content": "Test"}]}'
```

---

## 📊 SYSTEM MONITORING CHECKS

### Every 30 Minutes (automated loop)

```bash
while true; do
  echo "=== health check $(date) ===" >> ~/health-check.log
  openclaw doctor --non-interactive >> ~/health-check.log 2>&1
  curl -s http://localhost:18789/api/health >> ~/health-check.log 2>&1
  sleep 1800  # 30 minutes
done
```

### Monitor Logs

```bash
# Gateway logs
tail -f ~/.openclaw/gateway.log

# Agent logs
tail -f ~/.openclaw/agents/main/sessions/sessions.log

# System logs
tail -f ~/health-check.log
```

---

## ⚙️ FAIL-SAFE CONFIGURATIONS

### Gateway Safe Mode

If critical issues occur, set gateway to safe mode:

```json
{
  "models": {
    "providers": {
      "nvidia": {
        "baseUrl": "https://integrate.api.nvidia.com/v1",
        "apiKey": "nvapi-...",
        "api": "openai-completions",
        "models": [only 1 model: z-ai/glm5]
      }
    }
  }
}
```

### Minimum Viable Configuration

```json
{
  "meta": {
    "lastTouchedVersion": "2026.2.15"
  },
  "models": {
    "providers": {
      "nvidia": {
        "baseUrl": "https://integrate.api.nvidia.com/v1",
        "apiKey": "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",
        "api": "openai-completions"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "nvidia/z-ai/glm5"
      }
    }
  }
}
```

---

## 🚨 EMERGENCY STOP SIGNALS

If ANY of these occur, STOP and ROLLBACK:

1. **Gateway crashes repeatedly** (>3 times in 10 minutes)
2. **All providers return 401/403 errors**
3. **Agent sessions exceed 100MB each**
4. **Context window usage exceeds 90%**
5. **Doctors report critical errors consistently**
6. **Response time exceeds 30 seconds repeatedly**
7. **System becomes unresponsive**

---

## 📞 ESCALATION PROCEDURES

If autonomous improvement fails:

### Level 1: Minor Issues
- Rollback last change only
- Continue with next improvement area

### Level 2: Moderate Issues
- Rollback last 2-3 changes
- Pause improvement for 1 hour
- Re-evaluate approach

### Level 3: Critical Issues
- Full system reset to baseline
- Stop all autonomous improvements
- Wait for manual review

---

## 📁 RECOVERY FILES LOCATIONS

```
~/.openclaw/backup/
├── openclaw.json.backup-YYYYMMDD-HHMMSS
├── TODO.md.backup-YYYYMMDD-HHMMSS
├── AGENT_ARMY_KNOWLEDGE.md.backup-YYYYMMDD-HHMMSS
└── RECOVERY_LOG.txt (records all rollbacks)

~/health-check.log (continuous health monitoring)
~/.openclaw/gateway.log (gateway operations)
```

---

## ✅ PRE-IMPROVEMENT CHECKLIST

Before each autonomous improvement cycle:

- [ ] Current backup created
- [ ] Health check passed
- [ ] All providers responding
- [ ] Context window <80%
- [ ] Agent session sizes minimal
- [ ] Emergency stop signal script ready

---

**Recovery Plan Active: February 19, 2026 00:45**
**Baseline Recorded: 4 providers, 17 models, 11 agents**
**Autonomous Improvement Authorization: Pending user confirmation**
