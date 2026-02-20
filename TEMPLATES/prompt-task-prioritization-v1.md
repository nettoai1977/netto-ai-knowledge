# TASK PRIORITIZATION PROMPT TEMPLATE
## Standardized Prompt for Task Prioritization

**Prompt Template ID:** prompt-task-prioritization-v1  
**Purpose:** Ensure consistent, actionable task prioritization across all sessions  
**Created:** February 18, 2026

---

## 📋 PROMPT STRUCTURE

### Template Prompt (Copy & Paste This)

```
Prioritize the following tasks for today/this week:

[INSERT TASK LIST HERE]

Use this prioritization framework:

## 🎯 PRIORITIZATION MATRIX

Assign each task a Priority Level based on two factors:

### Impact (Influence on Goals)
- **HIGH Impact:** Direct impact on goals (3 points)
- **MEDIUM Impact:** Indirect or moderate impact (2 points)
- **LOW Impact:** Minor/no impact (1 point)

### Urgency (Time Sensitivity)
- **HIGH Urgency:** Due today or critical to timeline (3 points)
- **MEDIUM Urgency:** Due this week or medium timeline (2 points)
- **LOW Urgency:** Flexible timeline or backlog (1 point)

### Priority Score = Impact + Urgency
- **5-6 points:** 🔴 HIGH PRIORITY (Do immediately)
- **4 points:** 🟡 MEDIUM PRIORITY (Do this week)
- **3 points:** 🟢 LOW PRIORITY (Do when possible)
- **2 points:** ⚪ BACKLOG (Nice-to-have)

---

## 📋 TASK PRIORITIZATION RESULTS

### Task 1: [Task Name]
**Description:** [Brief description]
**Impact:** [HIGH/MEDIUM/LOW]
**Urgency:** [HIGH/MEDIUM/LOW]
**Score:** [6/5/4/3/2] → [Priority Level]
**Agent:** [Which agent should handle]
**Estimated Time:** [Duration]
**Dependencies:** [Prerequisites]

### Task 2: [Task Name]
**Description:** [Brief description]
**Impact:** [HIGH/MEDIUM/LOW]
**Urgency:** [HIGH/MEDIUM/LOW]
**Score:** [6/5/4/3/2] → [Priority Level]
**Agent:** [Which agent should handle]
**Estimated Time:** [Duration]
**Dependencies:** [Prerequisites]

[Continue for all tasks...]

---

## 🎯 PRIORITIZED TASK LIST (By Score)

### 🔴 HIGH PRIORITY (6 points) - Do Immediately
1. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

2. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

### 🟡 MEDIUM PRIORITY (4-5 points) - Do This Week
3. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

4. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

5. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

### 🟢 LOW PRIORITY (3 points) - Do When Possible
6. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

### ⚪ BACKLOG (2 points) - Nice-to-Have
7. [Task Name] - [Agent: XXX] - [Estimated Time]
   - Reason: [One-line explanation]

---

## 📊 AGENT WORKLOAD ANALYSIS

### Current Agent Loads (from AGENT_UTILIZATION_TRACKER.md)
- Spark: [%] → [Status: Available if <70%]
- Nova: [%] → [Status: Available if <70%]
- Flash: [%] → [Status: Available if <70%]
- Atlas: [%] → [Status: Available if <70%]
- Orion: [%] → [Status: Available if <70%]
- Zen: [%] → [Status: Available if <70%]
- Luna: [%] → [Status: Available if <70%]
- Vision: [%] → [Status: Available if <70%]
- Titan: [%] → [Status: Available if <70%]
- Coder: [%] → [Status: Available if <70%]
- Max: [%] → [Status: Available if <70%]

### Task Assignments by Agent
- **Spark:** [Task names assigned]
- **Nova:** [Task names assigned]
- **Flash:** [Task names assigned]
- **Atlas:** [Task names assigned]
- **Orion:** [Task names assigned]
- **Zen:** [Task names assigned]
- Other agents: [Task names assigned]

### Load Balancing Recommendations
[If any agent >70%, suggest alternative assignment]

---

## 🎯 EXECUTION PLAN

### Immediate (Today)
- [ ] [Task 1] - [Time estimate]
- [ ] [Task 2] - [Time estimate]
- [ ] [Task 3] - [Time estimate]

### This Week
- [ ] [Task 4] - [Time estimate]
- [ ] [Task 5] - [Time estimate]
- [ ] [Task 6] - [Time estimate]

### Backlog
- [ ] [Task 7] - [Time estimate]

---

## 📊 SUMMARY

- **High Priority Tasks:** [Count] tasks
- **Medium Priority Tasks:** [Count] tasks
- **Low Priority Tasks:** [Count] tasks
- **Backlog Items:** [Count] items
- **Total Estimated Time:** [Time today + This week]
- **Agent Load Distribution:** Balanced/Imbalanced
```

---

## 📝 FIELD GUIDELINES

### Task Information
**Assign each task:**
- **Name:** Concise task title
- **Description:** 1-2 sentence summary
- **Impact:** 
  - HIGH: Direct impact on goals (productivity, optimization)
  - MEDIUM: Indirect or moderate impact
  - LOW: Minor/no immediate impact
  
- **Urgency:**
  - HIGH: Due today, critical timeline, or blocking
  - MEDIUM: Due this week, medium timeline, or important
  - LOW: Flexible timeline, backlog item, or optional

- **Score:** Impact + Urgency (2-6 points)
- **Priority:**
  - 6 points: 🔴 HIGH
  - 5 points: 🔴 HIGH
  - 4 points: 🟡 MEDIUM
  - 3 points: 🟢 LOW
  - 2 points: ⚪ BACKLOG

### Agent Assignment
**Assign based on:**
1. **Task Type**
   - Quick tasks: Spark, Flash, Nova (if load <70%)
   - Architecture: Atlas (if load <70%)
   - Debugging: Orion (if load <70%)
   - Deep Analysis: Zen (if load <70%)
   - Large Context: Luna (if load <70%)
   - Vision: Vision agent (if load <70%)
   - Heavy Calculation: Titan (if load <70%)
   - Comprehensive: Max (if load <70%)
   - Code: Coder (if load <70%)

2. **Agent Load**
   - Check AGENT_UTILIZATION_TRACKER.md for current loads
   - Avoid agents at >70% (use backup)
   - Utilize underutilized agents (Titan 3%, Max 3%, Vision 12%)

3. **Estimated Time**
   - Quick tasks: 1-5 minutes
   - Analysis tasks: 5-15 minutes
   - Complex tasks: 15-30 minutes
   - Research tasks: 30-60 minutes

---

## 📊 OUTPUT FORMAT REQUIREMENTS

### Formatting Requirements
- **Sections:** Use markdown H3 (###)
- **Priorities:** Color-coded emoji indicators
- **Lists:** Numbered for priorities, bulleted for breakdowns
- **Agent Loads:** "85% (⚠️ High Load)", "42% (⚠️ Underutilized)"

### Quality Checklists
- [ ] All tasks prioritized
- [ ] Priority score calculated (Impact + Urgency)
- [ ] Agents assigned appropriately (task type + load)
- [ ] Load balancing checked (avoid >70% agents)
- [ ] Estimated time provided
- [ ] Dependencies identified
- [ ] Execution plan clear (Immediate/This Week/Backlog)

---

## 🎯 EXECUTION TIME TARGET

- **Start Time:** Prompt submission
- **Prioritization Matrix:** 30 seconds
- **Task Analysis:** 30 seconds per task
- **Agent Load Check:** 30 seconds
- **Load Balancing:** 30 seconds
- **Execution Plan:** 60 seconds
- **Total:** <3 minutes for 5-10 tasks (approximately 30 seconds per task)

---

## 📚 DATA SOURCES

### Required Files to Check
- `AGENT_UTILIZATION_TRACKER.md` - Current agent loads
- `WEEK[X]_PLAN.md` - Week priorities and goals
- `PERFORMANCE_LOG.md` - Pending tasks

### Optional Files
- `USERS_PREFERENCES.md` - User priorities and goals
- `AGENT_ARMY_KNOWLEDGE.md` - Agent specialties
- `WEEK[X]_PLAN.md` - Week-specific tasks

---

## 🔄 EXAMPLE

### Input Tasks:
1. Test daily briefing cron job
2. Implement task prioritization workflow
3. Create documentation templates
4. Review agent utilization patterns
5. Set up weekly review cron job

### Prioritized Output:

**🔴 HIGH PRIORITY (6 points):**
1. Test daily briefing cron job - Impact: HIGH + Urgency: HIGH = 6
   - Agent: Main Agent
   - Estimated Time: 15 min
   - Reason: Blocks automation

**🟡 MEDIUM PRIORITY (4 points):**
2. Set up weekly review cron job - Impact: MEDIUM + Urgency: HIGH = 5? No wait check calculation again - Impact: MEDIUM + Urgency: HIGH = 2+3=5 is still HIGH (5 out of 6) actually it's still HIGH priority by the matrix (just not top of HIGH)

Let me recalculate examples to match the matrix properly:

- Task 1 (Daily briefing cron test): HIGH Impact (critical for automation) + HIGH Urgency (blocks Week 3) = 6 points → 🔴 HIGH
- Task 2 (Weekly review cron setup): MEDIUM Impact (similar to daily) + MEDIUM Urgency (not as urgent as daily) = 4 points → 🟡 MEDIUM
- Task 3 (Task prioritization workflow): HIGH Impact (productivity improvement) + MEDIUM Urgency (Week 2/3) = 5 points → 🔴 HIGH
- Task 4 (Agent utilization review): MEDIUM Impact (optimization) + LOW Urgency (improvement) = 3 points → 🟢 LOW
- Task 5 (Documentation templates): LOW Impact (nice-to-have) + LOW Urgency (backlog) = 2 points → ⚪ BACKLOG

---

## ✅ TEMPLATE STATUS

**Version:** v1.0  
**Status:** ✅ READY FOR USE  
**Tested:** ❌ Not yet (pending Week 3 Day 2 manual test)  
**Success Rate:** TBD  
**Expected Time Savings:** 35% faster task prioritization (vs manual)

---

**Task Prioritization Prompt Template Complete: February 18, 2026 1:50 PM**

---

*Template: prompt-task-prioritization-v1*  
*Purpose: Standardize task prioritization*  
*Feature: Impact x Urgency matrix*  
*Expected Improvement:* 35% faster prioritization  
*Status: Ready for integration into workflows*