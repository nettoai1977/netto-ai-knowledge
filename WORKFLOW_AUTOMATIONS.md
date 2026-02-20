# WORKFLOW AUTOMATIONS
## Common Task Patterns & Optimized Flows

## 🚀 CRITICAL WORKFLOWS (Use Daily)

### 1. QUICK MODEL SWITCH
**Scenario:** User wants to switch models in Telegram

**Standard Flow:**
```
User: "Switch to GLM 4.7" or just "GLM 4.7"
→ Bot interprets and switches model
→ Confirmation with model details
→ Ready for next task
```

**Optimization:**
- Use model alias shortcuts
- Default reasoning models for complex tasks
- Flash/Spark for quick responses

**Shortcut Codes:**
```
"deep"       → Zen (Kimi K2 Thinking)
"fast"       → Spark (Ministral 14B)
"balanced"   → Nova (Kimi K2.5)
"code"       → Coder (Devstral 2)
"vision"     → Vision (Llama 4 Scout)
```

---

### 2. AGENT ARMY ROUTING
**Scenario:** Complex task requiring multiple agents

**Standard Flow:**
```
User: [Complex multi-step request]
        ↓
Main Agent → Analyze & route
        ↓
Atlas (Architecture) → Plan approach
        ↓
Flash (Draft) → Quick generation
        ↓
Coder (Refine) → Code improvements
        ↓
Zen (Review) → Deep analysis & polish
        ↓
Main Agent → Deliver result
```

**Task Type → Best Agent Mapping:**
```json
{
  "architecture": ["atlas", "zen"],
  "debugging": ["orion", "coder"],
  "code_review": ["luna", "coder"],
  "generation": ["flash", "nova"],
  "documentation": ["nova", "spark"],
  "vision": ["vision"],
  "analysis": ["atlas", "zen", "luna"],
  "quick_decisions": ["spark", "flash"]
}
```

---

### 3. CODE TASK WORKFLOW
**Scenario:** User needs code written/debugged

**Optimized Flow:**
```
Step 1: Task Understanding (Atlas)
  - Clarify requirements
  - Identify edge cases
  - Plan architecture

Step 2: Code Generation (Flash or Coder)
  - Quick draft (Flash) for simple tasks
  - Expert code (Coder) for complex tasks

Step 3: Verification (Orion)
  - Debug if issues
  - Test edge cases

Step 4: Final Polish (Nova or Zen)
  - Code review
  - Documentation
  - Best practices
```

**Efficiency Tips:**
- Use Flash for first drafts (fast, low cost)
- Switch to Coder for specialized code
- Use Spark for quick fixes or small changes
- Use Zen for critical code requiring deep analysis

---

### 4. RESEARCH & ANALYSIS WORKFLOW
**Scenario:** User needs research on a topic

**Optimized Flow:**
```
Step 1: Define Scope (Nova)
  - Clarify research questions
  - Identify key areas

Step 2: Web Search (Main + Brave Search)
  - Gather information
  - Cross-reference sources

Step 3: Deep Analysis (Luna + Atlas)
  - Luna: Process large context (1M tokens)
  - Atlas: Structure findings

Step 4: Synthesis (Zen)
  - Deep analysis & synthesis
  - Key insights extraction

Step 5: Presentation (Nova)
  - Clear summary
  - Actionable recommendations
```

**Cost Optimization:**
- Use Luna only for very large documents (>200k tokens)
- Use Nova for standard research
- Use Atlas for structured analysis

---

### 5. DOCUMENTATION WORKFLOW
**Scenario:** User needs documentation written

**Optimized Flow:**
```
Step 1: Quick Draft (Spark)
  - Fast outline generation
  - Basic structure

Step 2: Content Development (Nova)
  - Flesh out sections
  - Add examples

Step 3: Quality Review (Atlas)
  - Check consistency
  - Verify completeness

Step 4: Polish (beautiful-prose skill)
  - Improve writing style
  - Final polish
```

**Shortcut:** `beautiful-prose` skill available for immediate writing improvement

---

### 6. ERROR DEBUGGING WORKFLOW
**Scenario:** User reports a bug or error

**Optimized Flow:**
```
Step 1: Error Analysis (Orion)
  - Identify root cause
  - Propose fixes

Step 2: Fix Implementation (Coder)
  - Apply the fix
  - Test locally

Step 3: Prevention (Atlas)
  - Document root cause
  - Suggest prevention strategies
```

**Error Pattern Matching:**
```
API Error → Check API keys, endpoints, authentication
Code Syntax → Syntax error detection and fix
Logic Error → Code flow analysis
Performance → Profiling and optimization
```

---

### 7. SKILL LOADING WORKFLOW
**Scenario:** User needs a specific skill

**Quick Load:**
```
User: "Use [skill-name] skill"
→ Main Agent → Load skill from inventory
→ Apply skill to task
→ Document usage pattern
```

**Skill Discovery:**
```
User: "Find skills for [task]"
→ Review SKILLS_INVENTORY.md
→ List relevant skills
→ Prioritize by category
→ Load top recommendation
```

**Common Skill Combinations:**
```json
{
  "web_dev": ["architecture", "api-design-principles", "frontend-dev-guidelines", "backend-dev-guidelines"],
  "ai_dev": ["ai-engineer", "agent-orchestration-improve-agent", "azure-ai-projects-py"],
  "testing": ["tdd-workflows-tdd-green", "playwright-skill", "production-code-audit"],
  "security": ["pentest-checklist", "api-security-best-practices", "backend-security-coder"]
}
```

---

## 🎯 HIGH-IMPACT WORKFLOWS (Use Weekly)

### 8. SYSTEM OPTIMIZATION WORKFLOW
**Scenario:** Performance improvements or cost reduction

**Flow:**
```
Step 1: Current State Analysis (Nova)
  - Analyze metrics
  - Identify bottlenecks

Step 2: Optimization Strategy (Atlas)
  - Design improvements
  - Estimate impact

Step 3: Implementation (Flash/Coder)
  - Apply changes
  - Test thoroughly

Step 4: Results Measurement (Luna)
  - Compare before/after
  - Document improvement
```

---

### 9. KNOWLEDGE SHARING WORKFLOW
**Scenario:** Sharing learnings across agent army

**Flow:**
```
Step 1: Discover New Pattern/Main Agent
  - Document discovery

Step 2: Update Agent Knowledge Bases (Automation)
  → Update AGENT_ARMY_KNOWLEDGE.md
  → Update relevant agent SKILLS.md

Step 3: Apply to Other Agents (Testing)
  → Test pattern in different contexts

Step 4: Document Best Practices → MEMORY.md
```

---

### 10. API TESTING & INTEGRATION
**Scenario:** Testing or integrating with new API

**Flow:** (Reference workspace-flash implementation)
```
Step 1: API Exploration (Flash)
  - Test endpoints
  - Document responses

Step 2: Integration Planning (Atlas)
  - Design integration
  - Identify potential issues

Step 3: Implementation (Coder)
  - Build integration
  - Add error handling

Step 4: Cost Analysis → IMPLEMENTATION.md
  - Measure API costs
  - Optimize usage

Step 5: Documentation (Nova)
  - Create API documentation
  - Document usage patterns
```

---

## 🔄 BATCH WORKFLOWS (Use Monthly)

### 11. SKILLS UPDATE WORKFLOW
**Scenario:** Refreshing skill knowledge

**Flow:**
```
Step 1: Scan for New Skills (Main)
  - Check Antigravity repo
  - Scan new additions

Step 2: Category Assessment (Atlas)
  - Categorize new skills
  - Prioritize by relevance

Step 3: Update SKILLS_INVENTORY.md (Nova)
  - Add new skills
  - Update counts

Step 4: Test High-Value Skills (Flash)
  - Quick test drive
  - Document usage patterns
```

---

### 12. PERFORMANCE AUDIT WORKFLOW
**Scenario:** Comprehensive system performance review

**Flow:**
```
Step 1: Collect Metrics (All agents contribute)
  - Response times
  - Accuracy rates
  - Cost efficiency

Step 2: Analysis (Luna + Atlas)
  - Process large dataset
  - Identify patterns

Step 3: Recommendations (Zen)
  - Deep analysis
  - Strategic improvements

Step 4: Action Plan (Nova)
  - Prioritize improvements
  - Create implementation plan
```

---

## 📋 WORKFLOW OPTIMIZATION TIPS

### SPEED OPTIMIZATIONS
1. Use **Flash/Spark** for first drafts always
2. Cache frequent responses in MEMORY.md
3. Use model alias shortcuts
4. Parallelize independent tasks across agents

### COST OPTIMIZATIONS
1. Prioritize **NVIDIA free models** (80%+ of tasks)
2. Use **Spark** for quick tasks (lower token cost)
3. Use **Luna only** when 1M context is truly needed
4. Batch similar requests together

### QUALITY OPTIMIZATIONS
1. Always use **Zen** for final review on critical tasks
2. Use **Atlas** for architecture decisions
3. Use **Coder** specialized model for code
4. Use **Vision** for any image-related tasks

### AGENT COORDINATION OPTIMIZATIONS
1. Use **handoff protocol** - pass context between agents
2. Document state in shared files
3. Use appropriate agent for task type
4. Avoid unnecessary agent switches

---

## 🎯 WORKFLOW DECISION TREE

```
New Task?
  ↓
Quick? (< 1 min)
  → YES → Spark or Flash
  → NO  → 

Complex?
  ↓
  → YES → Atlas (plan) → Flash (draft) → Coder/Specialist (refine) → Zen (review)
  → NO  →

Code-related?
  ↓
  → YES → Coder (or Flash for simple)
  → NO  → 

Requires vision?
  ↓
  → YES → Vision
  → NO  →

Large context (> 200k tokens)?
  ↓
  → YES → Luna
  → NO  → Nova or Atlas
```

---

## 📊 WORKFLOW METRICS TO TRACK

1. **Task Completion Time** - Average time per task
2. **Agent Switch Count** - How many agents per task
3. **Model Selection Accuracy** - Right model for right task
4. **Skill Usage Frequency** - Most/least used skills
5. **Cost per Task** - Total tokens used
6. **Success Rate** - Tasks completed without issues

---

## 🚀 AUTOMATION OPPORTUNITIES

### Can Be Automated:
1. **Agent Selection** - Based on task keywords
2. **Model Selection** - Based on task complexity
3. **Skill Loading** - Auto-detect need
4. **Error Pattern Detection** - Common error fixes
5. **File Organization** - Archive old files

### Needs Manual Review:
1. Complex architecture decisions
2. Security assessment
3. Critical code reviews
4. User-specific preferences

---

*Workflows Created: 2026-02-18 | Phase 2 - Workflow Automations*
