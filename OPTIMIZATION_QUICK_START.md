# OPTIMIZATION PLAN - QUICK START GUIDE

## 🚀 Start Right Now (Next 10 Minutes)

### Step 1: Enable Cost Tracking
```bash
# Add to openclaw.json
{
  "commands": {
    "responseUsage": "cost"
  }
}

# Or via gateway restart
```

### Step 2: Establish Baseline
```bash
# Run these commands NOW
/usage full
/context detail
```

### Step 3: Document Findings
Create `COST_BASELINE.md`:
```markdown
# COST BASELINE
Date: 2026-02-18

Current Session:
- Context: ??k/200k
- Tokens in: ??k
- Tokens out: ??k
- Cost: $??

Next Steps:
- [ ] Monitor for 24 hours
- [ ] Re-run /usage full
- [ ] Compare and identify patterns
```

### Step 4: Set Heartbeat Interval (If Applicable)
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "55m"
      }
    }
  }
}
```

---

## 📋 THIS WEEK - DAY BY DAY

### Day 1 (Today)
- [ ] Enable cost tracking
- [ ] Run token audit
- [ ] Create COST_BASELINE.md
- [ ] Review bootstrap files

### Day 2
- [ ] Optimize bootstrap files
- [ ] Run `/compact` if needed
- [ ] Monitor token usage

### Day 3
- [ ] Review day 1-2 findings
- [ ] Identify top 3 bottlenecks
- [ ] Fix top bottleneck

### Day 4
- [ ] Review cost patterns
- [ ] Identify expensive workflows
- [ ] Optimize 1 expensive workflow

### Day 5
- [ ] Weekly review
- [ ] Update OPTIMIZATION_REPORT.md
- [ ] Plan week 2

---

## ⚡ INSTANT WINS (Do Today)

### 1. Use Free Models
**Already doing this!** ✅
- NVIDIA models are FREE
- You're optimizing already

### 2. Compact Context
```bash
/compact
```
Use when context > 80%

### 3. Prefer Smaller Models
- Quick tasks: spark, flash
- Code: coder (Devstral 2)
- Deep thinking: atlas, zen

### 4. Review Agent Utilization
```bash
# Check which agents are being used
# If some agents never used:
# - Remove from config
# - Or create use cases for them
```

---

## 🎯 TOP 3 PRIORITIES (Based on Research)

#1: **Productivity Skills** (Week 2)
**Why:** Research shows 50+ skills tested, only 10 worked  
**Action:** Install triple-memory-skill, flowmind  
**Impact:** 30-50% productivity gain

#2: **Agent Coordination** (Week 3)
**Why:** You have 11 agents - use them!  
**Action:** Test multi-agent handoffs, enable sub-agent spawning  
**Impact:** 20-30% faster tasks, better specialization

#3: **Knowledge Management** (Week 6)
**Why:** Don't lose what you learned  
**Action:** Regular MEMORY.md updates, document patterns  
**Impact:** Continuous improvement, no repeated work

---

## 📊 TRACKING TEMPLATE

Create `PERFORMANCE_LOG.md`:

```markdown
# PERFORMANCE LOG

## 2026-02-18 (Baselines)
### Productivity
- Tasks Completed: 4
- Avg Time/Task: 7.75 min
- Sub-Agents Spawned: 1

### Cost
- Model: nvidia/z-ai/glm4.7
- Cost: $0.00
- Free Model Usage: 100%

### Next Review: 2026-02-19
```

---

## 🚀 INSTANT ACTIONS (Pick One)

**Option A: Token Optimization**
```bash
/compact  # If context > 80%
/usage full  # Check current usage
```

**Option B: Test Coordination**
```bash
# Spawn 3 subagents to research 3 skills
sessions_spawn(task="Research skill X from inventory")
sessions_spawn(task="Research skill Y from inventory")
sessions_spawn(task="Research skill Z from inventory")
subagents list  # Wait and check status
```

**Option C: Cost Check**
```bash
/usage cost  # Check local cost summary
```

---

## 📚 KEY FILES TO CREATE

1. ✅ `OPTIMIZATION_PLAN_PRODUCTIVITY.md` - Master plan (DONE)
2. `COST_BASELINE.md` - Starting metrics
3. `PERFORMANCE_LOG.md` - Daily tracking
4. `OPTIMIZATION_REPORT.md` - Weekly summary
5. `OPTIMIZATION_CHECKLIST.md` - Progress tracking

---

*Quick Start: 2026-02-18*
