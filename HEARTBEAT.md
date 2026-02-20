# HEARTBEAT.md - Proactive Monitoring Tasks

## ⚠️ CRITICAL RULES

### Before Every Tool Call
1. **VERIFY ALL REQUIRED PARAMETERS** - Never send empty params
2. **Double-check parameter names** - Case-sensitive!
3. **If unsure, print parameters first** - Don't guess

### During Long Tasks
1. **Report status every 30 seconds** - Never go silent
2. **Use yieldMs for waits** - Don't block
3. **Acknowledge before starting** - Don't disappear

---

## Periodic Checks (Every Heartbeat)

### Performance Self-Check (NEW!)
- [ ] Did I make any tool call errors last session?
- [ ] Did I leave the user waiting without updates?
- [ ] Did I validate ALL tool parameters?
- [ ] Did I acknowledge requests immediately?
- [ ] Check SELF_ANALYSIS_REPORT.md for issues

### System Health
- [ ] Check gateway status and uptime
- [ ] Verify all API keys are working (NVIDIA, Groq, OpenRouter)
- [ ] Monitor context window usage (optimize if >80%)

### Knowledge Management
- [ ] Review and update MEMORY.md with recent learnings
- [ ] Clean up old memory/YYYY-MM-DD.md files (keep last 7 days)
- [ ] Update AGENTS.md with new capabilities discovered

### Agent Army Coordination
- [ ] Check status of all configured agents
- [ ] Verify agent workspaces are clean
- [ ] Ensure agent model assignments are optimal

### Self-Improvement
- [ ] Analyze recent sessions for improvement opportunities
- [ ] Identify patterns in user requests
- [ ] Update TOOLS.md with new shortcuts or configurations

---

## Priority Focus Areas
1. **ZERO TOOL CALL ERRORS** - Validate before calling
2. **PROACTIVE STATUS UPDATES** - Never go silent
3. **Speed** - Reduce response time
4. **Accuracy** - Verify information before responding
5. **Cost-Effectiveness** - Use free models when possible

---

## Notes
- Perform 2-4 checks per heartbeat
- Rotate through different check categories
- Document significant findings in MEMORY.md
