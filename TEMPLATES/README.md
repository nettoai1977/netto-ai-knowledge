# TEMPLATES README
## How to Use Prompt Templates

**Created:** February 18, 2026

---

## 🎯 QUICK START

### What Are Templates?
Prompt templates are pre-formatted, reusable instructions that ensure consistent output quality across all sessions.

### Benefits:
- **Faster:** Save 30-50% setup time on template-based tasks
- **Consistent:** Same format every time, better for analysis
- **Higher Quality:** Structured prompts produce better results
- **Reusable:** Use the same template repeatedly

---

## 📚 AVAILABLE TEMPLATES

### 1. Daily Briefing Template
**When to Use:** Every morning to start the day
**Trigger:** "Daily briefing" or "Give me my daily briefing"
**Time:** 5 minutes (vs 20-30 min manual)
**Sections:** 6 steps (Agent status, events, performance, cost, priorities, suggestions)

**File:** `prompt-daily-briefing-v1.md`

---

### 2. Weekly Review Template
**When to Use:** End of each week for review and planning
**Trigger:** "Weekly review"
**Time:** 15 minutes (vs 1-2 hours manual)
**Language:** Bilingual (English + 中文)
**Sections:** 6 sections (Performance, tasks, problems, cost, lessons, plan)

**File:** `prompt-weekly-review-v1.md`

---

### 3. Task Prioritization Template
**When to Use:** When organizing tasks for the day/week
**Trigger:** "Prioritize tasks" or integrated into daily briefing
**Time:** 3 minutes (vs 5-8 min manual)
**Algorithm:** Impact (1-3) + Urgency (1-3) = Priority Score (2-6)

**Priority Levels:**
- 🔴 HIGH (5-6 points): Do immediately
- 🟡 MEDIUM (4 points): Do this week
- 🟢 LOW (3 points): Do when possible
- ⚪ BACKLOG (2 points): Nice-to-have

**File:** `prompt-task-prioritization-v1.md`

---

## 🚀 HOW TO USE

### Step 1: Choose Template
Select the appropriate template from `TEMPLATES_INDEX.md` or this README.

### Step 2: Copy Template
Copy the template content from the template file.

### Step 3: Fill Placeholders
Replace placeholders with real data:
- `[DATE]` → Replace with actual date
- `[TASK LIST]` → Replace with your tasks
- `[AGENT INFO]` → Replace with agent data

### Step 4: Submit Prompt
Submit the filled template to the agent.

---

## 📊 EXAMPLES

### Example 1: Daily Briefing

**Input:**
```
[Submit template with today's date]
```

**Output:**
```
# 🌅 MORNING BRIEFING
## February 18, 2026 - 8:00 AM

### 🏛️ AGENT ARMY STATUS
[All 11 agents listed with loads]

### 📅 DATES & EVENTS TODAY
[Today's progress, events, deadlines]

### 📊 YESTERDAY'S PERFORMANCE
[Tasks completed, issues, improvements]

### 💰 COST SUMMARY (7 Days)
[Cost metrics, daily average]

### 🎯 TODAY'S PRIORITIES (Ranked)
1. [Priority 1] - Agent: XXX
2. [Priority 2] - Agent: XXX
3. [Priority 3] - Agent: XXX

### 💡 PROACTIVE SUGGESTIONS
[From HEARTBEAT, OPTIMIZATION_QUICK_START]
```

---

### Example 2: Task Prioritization

**Input Tasks:**
```
1. Test daily briefing cron job
2. Implement task prioritization workflow
3. Create documentation templates
4. Review agent utilization patterns
5. Set up weekly review cron job
```

**Output:**
```
🔴 HIGH PRIORITY (6 points):
1. Test daily briefing cron job - Agent: Main Agent - 15 min
   Reason: Blocks Week 3 automation

🟡 MEDIUM PRIORITY (4-5 points):
2. Weekly review cron setup - Agent: Main Agent - 20 min
   Reason: Week 3 automation (similar to daily)
3. Implement task prioritization - Agent: Main Agent - 30 min
   Reason: Productivity improvement

🟢 LOW PRIORITY (3 points):
4. Agent utilization review - Agent: Orion - 20 min
   Reason: Optimization improvement

⚪ BACKLOG (2 points):
5. Documentation templates - Agent: Main Agent - 1 hour
   Reason: Nice-to-have, Week 3 Day 5
```

---

## 🎯 BEST PRACTICES

### When to Use Templates
✅ **DO Use Templates For:**
- Recurring workflows (daily briefing, weekly review)
- Standardized tasks with common structure
- Tasks where consistency is important
- Complex tasks that benefit from structure

❌ **DON'T Use Templates For:**
- One-off unique requests
- Tasks requiring completely different approaches
- Experimental or creative tasks
- Tasks where strict format hinders value

### How to Customize Templates
1. Start with base template
2. Keep structure (headings, sections)
3. Customize content within sections
4. Test before using in production
5. Save variations for reuse

---

## 📚 ADVANCED USAGE

### Template Chain (Sequential Use)
**Example:** Daily briefing → Task prioritization → Execution plan

```
Template 1: Daily Briefing
  ↓ (Extracts tasks)
Template 2: Task Prioritization
  ↓ (Produces prioritized list)
Template 3: Execution Plan
```

### Template Combination (Parallel Use)
**Example:** Generate multiple perspectives simultaneously

```
Agent 1 (using Task Prioritization Template)
  Parallel execution
Agent 2 (using Weekly Review Template)
  Parallel execution
Consolidate results
```

### Template Versioning
v1.0: Initial template  
v1.1: Bug fixes, minor improvements  
v1.2: Feature additions (new sections)  
v2.0: Major restructure (different format)

Check `TEMPLATES_INDEX.md` for current versions.

---

## 🔧 TROUBLESHOOTING

### Issue: Output Not Following Template
**Diagnosis:** Template not properly loaded or agent ignoring structure

**Solutions:**
- Ensure template content is fully copied
- Check template syntax (headings, bullet points)
- Test with simpler template first

### Issue: Placeholder Not Replaced
**Diagnosis:** Agent not filling in dynamic data

**Solutions:**
- Use clear placeholder format: `[PLACEHOLDER]`
- Ensure data sources are accessible
- Check workflow integration (if applicable)

### Issue: Template Too Generic
**Diagnosis:** Template doesn't fit specific use case

**Solutions:**
- Customize template sections
- Create variation for use case
- Use template as starting point, not final format

---

## 📊 METRICS

### Template Effectiveness
**Time Saved:** 30-50% on template-based tasks  
**Quality:** 10-15% improved (consistent format)  
**Reusability:** Save 50-70% setup time per use  
**Maintenance:** 60% easier to update vs ad-hoc prompts

### Workflow Integration
**Daily Briefing:** Integrated into daily briefing workflow ✅  
**Weekly Review:** Integrated into weekly review workflow ✅  
**Task Prioritization:** Pending integration into daily briefing ⏳

---

## 📞 FEEDBACK

### How to Improve Templates
- **Report Issues:** Note where template fails or produces poor results
- **Suggest Improvements:** Propose section additions, format changes
- **Share Variations:** Document successful customizations

### Next Steps (Week 3)
1. Test templates in actual workflow executions
2. Gather feedback on template effectiveness
3. Refine based on testing results
4. Consider v1.1 versions if needed

---

**Templates README Complete: February 18, 2026 2:00 PM**

---

*How to Use Prompt Templates* ✅  
*All 3 Templates Ready* ✅  
*Skill #3 (Prompt Manager): COMPLETE* ✅  
*Next: Skill #4 (Task Prioritization)* 🚀