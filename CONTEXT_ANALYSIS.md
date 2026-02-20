# CONTEXT ANALYSIS
## System Prompt Size & Token Usage Analysis

**Analysis Date:** 2026-02-18  
**Analysis Time:** 11:15 AM

---

## 📊 CURRENT CONTEXT STATE

**From Session Status:**
- **Context Window:** 147k/200k (74%)
- **Tokens In:** 1.4M
- **Tokens Out:** 9.7K
- **Compactions:** 0

**Assessment:** ✅ **OPTIMAL** - Well below 80% threshold, no compaction needed yet

---

## 🎯 SYSTEM PROMPT COMPONENTS

### What's Currently Injected (From Official Docs)

**System Prompt Includes:**
1. ✅ Tool list + short descriptions
2. ⏳ Skills list (metadata only, instructions loaded on demand)
3. ⏳ Self-update instructions
4. ⏳ Workspace + bootstrap files:
   - AGENTS.md
   - SOUL.md
   - TOOLS.md
   - IDENTITY.md
   - USER.md
   - HEARTBEAT.md
   - BOOTSTRAP.md
   - MEMORY.md and/or memory.md (when present)
5. ⏳ Time (UTC + user timezone)
6. ⏳ Reply tags + heartbeat behavior
7. ⏳ Runtime metadata (host/OS/model/thinking)

### Bootstrap Truncation Limits (Config)
- `bootstrapMaxChars`: 20000 (default)
- `bootstrapTotalMaxChars`: 150000 (default)

---

## 🔍 BOOTSTRAP FILE ANALYSIS

Let me analyze the bootstrap files to optimize them:

### Method: Check file sizes and identify potential candidates for truncation

**Analysis Needed:**
1. Check size of all bootstrap files
2. Identify files > 20000 chars
3. Recommend truncation or optimization

---

## 💡 OPTIMIZATION RECOMMENDATIONS

### Immediate Actions (Based on Context Usage at 74%)

**Status:** ✅ **NO IMMEDIATE ACTION NEEDED**

Context is at 74% which is safe. However, we should:

1. **Monitor closely** - If context exceeds 80%, run `/compact`
2. **Check bootstrap file sizes** - Identify oversized files
3. **Optimize skill descriptions** - Keep them short (skill list is injected)
4. **Trim tool outputs** - Reduce verbose responses from tools

---

## 📊 TOKEN OPTIMIZATION CHECKLIST

### Manual Compaction Trigger
```bash
# Run when context > 80%
/compact
```

### Usage Monitoring
```bash
# Check usage per response
/usage tokens

# Check local cost summary
/usage cost

# Check system prompt breakdown
/context detail
```

### Automatic Compaction
**Feature Check:** Determine if automatic compaction is configured

**Recommendation:** Enable automatic compaction if not already set:
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "threshold": 80
      }
    }
  }
}
```

---

## 🎯 NEXT STEPS

### Today
1. ⏳ List all bootstrap files with their sizes
2. ⏳ Identify files above truncation threshold (20000 chars)
3. ⏳ Review SKILLS_INVENTORY.md (large file)
4. ⏳ Check SKILLS.md files in agent workspaces

### This Week
1. ⏳ Optimize oversized bootstrap files (>20000 chars)
2. ⏳ Review and shorten skill descriptions
3. ⏳ Test compaction effectiveness
4. ⏳ Document token savings

---

## 📈 EXPECTED IMPACT

From research (official docs):
- **Short skill descriptions:** 10-20% token reduction
- **Bootstrap optimization:** 10-30% session reduction
- **Tool output trimming:** 15-25% token reduction

**Combined Potential:** 30-60% total token reduction if all optimizations are applied

---

**Analysis Status:** ✅ **INITIATED**  
**Context Usage:** 74% (OPTIMAL)  
**Next Analysis:** 24 hours from now

---
*Context Analysis: 2026-02-18 11:15 AM*
