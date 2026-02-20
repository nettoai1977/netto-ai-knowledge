# WEEKLY REVIEW WORKFLOW
## End-of-Week Reflection and Planning

**Workflow Name:** weekly-review  
**Created:** February 18, 2026  
**Trigger Schedule:** Weekly (Friday at 5:00 PM or Sunday at 10:00 AM)

---

## 🎯 WORKFLOW PURPOSE

Conduct a structured weekly review to:
- Review本周完成的任务
- Analyze本周性能
- Identify问题
- Plan下周计划
- Update记忆

---

## 🚀 WORKFLOW STEPS

### Step 1: Review Week Statistics
**From:** PERFORMANCE_METRICS.md

**What It Does:**
- Total tasks completed
- Average response time per task
- Agent utilization (which agents used)
- Token usage totals
- Cost summary

**Agent Routing:** Main Agent (orchestrator)

---

### Step 2: Analyze本周性能

**Questions to Answer:**
- What were the 3 best productivity wins this week?
- What were the 3 biggest challenges?
- Which agents were most/least utilized?
- Which workflows saved the most time?
- Did we stay within cost targets?

**Agent Routing:** Analyze → Zen (deep analysis)

---

### Step 3: Identify Problems (Identify问题)
**Review:**
- What went wrong this week?
- Any failures or bugs encountered?
- Agent coordination issues?
- Workflow breakdowns?
- Token efficiency issues?

**Agent Routing:** Main Agent (review) → Orion (debug) → Coder (fix if needed)

---

### 识别问题 (Identify Chinese: 识别问题)

**Check for:**
- Error patterns
- Failed tasks
- Agent coordination failures
- Workflows that broke
- API issues
- Skill conflicts

---

## 📋 OUTPUT FORMAT

### Weekly Review Template

```markdown
# 📊 WEEKLY REVIEW
## Week of: [Year]February 10-16, 2026
**Review Date:** February 18, 2026

### 📈 PERFORMANCE SUMMARY

#### Tasks Completed
**Total Tasks:** [X tasks this week]
**Completed:** [Y completed tasks]
**Completion Rate:** [Y/X = percentage]
**Target:** >90%

#### Agent Utilization
| Agent | Tasks Handled | % Utilization |
|-------|---------------|---------------|
| Main | [X] | [X]% |
| atlas | [X] | [X]% |
| flash | [X] | [X]% |
| nova | [X] | [X]% |
| orion | [X] | [X]% |
| zen | [X] | [X]% |
| coder | [X] | [X]%
| max | [X] | [X] |
| spark | [X] | [X]% |
| titan | [X] | [X]% |
| vision | [X] | [X]% |

#### Metrics
- **Avg Response Time:** [X]s
- **Success Rate:** [X]%
- **Cost:** $[X.XX]
- **Free Model Usage:** [X]%

### 🎯 本周完成的任务 (Tasks Completed This Week)

#### Top 3 Accomplishments
1. **[Accomplishment #1]:** [Description]
   - **Agent:** [Which agent handled it]
   - **Time:** [Duration]
   - **Impact:** [Result]

2. **[Accomplplishment #2]:** [Description]
   - **Agent:** [Which agent handled it]
   - **Time:** [Duration]
   - **Impact:** [Result]

3. **[Accomplplishment #3]:** [Description]
   - **Agent:** [Which agent handled it handled it]
   - **Time:** [Duration]
   - **Impact:** [Result]

#### Other Completed Tasks
- [ ] [Task 4]
- [ ] [Task 5]
- [ ] [Task 6]

### 🚨 ISSUES & BLOCKERS

#### Problems Encountered
1. **[Problem #1]:** [Description]
   - **When:** [When it happened]
   - **Impact:** [Effect]
   - **Status:** [Resolved/Pending]
   - **Agent Involved:** [Which agent handled it]
   - **Resolution:** [How it was/will be fixed]

2. **[Problem #2]:** [Description]
   - **When:** [When it happened]
   - **Impact:** [Effect]
   - **Status:** [Resolved/Pending]
   - **Agent Involved:** [Which agent handled it]
   - **Resolution:** [How it was/will be fixed]

3. **[Problem #3]:** [Description]
   - **When:** [When it happened]
   - **Impact:** [Effect]
   - **Status:** [Resolved/Pending]
   - **Agent Involved:** [Which agent handled it]
   - [Resolution:** [How it was/will be fixed]

### 📊 成本分析

#### Cost Breakdown
- **Total Cost:** $[X.XX] for the week
- **Daily Average:** $[X.XX]
- **Vs Last Week:** [Increase/Decrease]

#### Token Usage
- **Total Tokens:** [X]M tokens
- **Free Model Usage:** [X]%

#### Cost Per Task
- **Average:** $[X.XX]/task

### 💡 本周改进

#### Lessons Learned
1. **[Lesson #1]:** [What we learned]
   - **Impact:** [How it applies to future]

2. **[Lesson #2]:** [What we learned]
   - **Impact:** [How it applies to future]

3. **[Lesson #3]:** [What we learned]
   - **Impact:** [How it applies to future]

---

## 🎯 下周计划 (Next Week Plan)

### Priorities Ranked (High to Low)
1. **[Top Priority]:** [Description]
   - **Agent:** [Which agent should handle]
   - **Estimated Time:** [Duration]
   - **Dependencies:** [What needs to be completed first]

2. **[Priority]:** [Description]
   - **Agent:** [Which agent should handle]
   - **Estimated Time:** [Duration]
   - **Dependencies:** [What needs to be completed first]

3. **[Priority]:** [Description]
   - **Agent:** [Which agent should handle]
   - **Estimated Time:** [�� Duration]
   - **Dependencies:** [What needs to be completed first]

### Backlog Items
- [ ] [Backlog Item 1]
- [ ] [Backlog Item 2]
- [ [Backlog Item 3]

### 目标 (Goals)
- [ ] [Goal 1 for next week]
- [ ] [Goal 2 for next week]
- [ ] [Goal 3 for next week]

---

## 🔄 CONTINUOUS IMPROVEMENT

### Week 1: Manual Weekly Review
**Goal:** Establish weekly review process
**Outcome:** Document patterns and learnings
**Agent:** Atlas (analysis) → Main Agent (reporting)

### Week 2: Automate Summary
**Goal:** Create automated weekly review generation
**Trigger:** Every Sunday 10:00 AM or Friday 5:00 PM
**Outcome:** Weekly review auto-generated

### Week 3: Add Predictive Analytics
**Goal:** Add trends and forecasts to weekly review
**Trigger:** Weekly
**Agent:** Zen (deep analysis) + Luna (1M context for data analysis)
**Outcome:** Predictive insights for planning

---

## 📊 SUCCESS CRITERIA

### Successful Weekly Review Includes:
- ✅ Review of本周完成的任务
- ✅ Analyze本周性能
- ✅ Identify问题 with status
- 🎯 下周计划 documented
- 💡 本周改进记录
- 📊 成本分析
- 📋 Updated priorities

### Testing Checklist
- [ ] Agent can retrieve本周任务完成情况
- [ ] Agent can analyze 本周性能数据
- [ ] Problems are documented with resolutions
- [ ] Next week is planned with clear priorities
- [ ] Learnings are recorded for future reference

---

## 💡 PROACTIVE SUGGESTIONS

### Based on HEARTBEAT.md
- [ ] [Suggestion 1 from proactive monitoring]
- [ ] [Suggestion 2 from improvement tasks]
- [ ] [Suggestion 3 from optimization tasks]

### Based on OPTIMIZATION_QUICK_START.md
- [ ] [Suggestion 1 from quick wins]
- [ ] [Suggestion 2 from optimization tasks]
- [ ] [Suggestion 3 from cost optimization]

---

## 🎫 下周 (Next Week) FOCUS

### Primary Focus
1. **[Focus 1:]**
   - Why: [Reason for focus]
   - Agent: [Agent responsible]
   - Expected Outcome: [What we want to achieve]

### Secondary Focus
1. **[Focus 2:]**
   - Why: [Reason for focus]
   - Agent: [Agent responsible]
   - Expected Outcome: [What we want to achieve]

---

**Weekly Review Workflow Created: 2026-02-18 11:45 AM**  
**Status:** ✅ Ready for Testing**  
**Language:** Chinese + English (as designed for MichaelNettoNZ)

*Weekly Review Workflow Created: 2026-02-18 11:50 AM*
