# AGENT COORDINATION PROTOCOL
## Multi-Agent Collaboration System

## 🎖️ AGENT ARMY COMMAND STRUCTURE

### 🏛️ Command Hierarchy
```
          COMMANDER (Main Agent)
                │
        ┌───────┴────────┐
        │                │
  STRATEGY TACTICAL     OPS
  (Atlas)           (Nova, Flash, etc.)
        │                │
    SQUADS         SPECIALISTS
```

**Roles:**
- **Commander (Main):** Orchestrates all operations, makes routing decisions
- **Strategy Lead (Atlas):** Architecture, planning, complex decisions
- **Tactical Lead (Nova):** Balanced operations, standard tasks
- **Ops Teams:** Flash (speed), Spark (quick), Orion (debug)
- **Specialists:** Coder (code), Vision (vision), Zen (deep thinking), Luna (large context), Titan (heavy), Max (scale)

---

## 🤝 HANDOFF PROTOCOLS

### 1. Standard Handoff Format
When handing off between agents, use this structured format:

```markdown
## HANDOFF FROM: [Agent Name]
## TO: [Agent Name]

### Task Context
- **Primary Goal:** [What needs to be done]
- **User Intent:** [What user is trying to achieve]
- **Constraints:** [Any limitations or requirements]

### Work Already Done
- [ ] Step 1 completed
- [x] Step 2 completed - [Result]
- [ ] Step 3 pending

### Current State
- Files modified: [list]
- APIs called: [list]
- Decisions made: [list]
- Blockers encountered: [list]

### Next Steps
1. [ ] [Specific action 1]
2. [ ] [Specific action 2]
3. [ ] [Specific action 3]

### Context Files
- [Link to relevant files]

### Notes
[Additional context for the receiving agent]
```

### 2. Handoff Triggers

**Manual Handoff:** Agent explicitly requests handoff
```
User: "This needs deeper analysis"
→ Main Agent → Switch to Zen
→ Handoff with full context
```

**Automatic Handoff:** System detects need
```
Large file detected (> 200k tokens)
→ Main Agent → Handoff to Luna
→ Pass file path, task context
```

**Pattern-Based Handoff:**
```
Task type detected: "code debugging"
→ Main Agent → Route to Orion
→ Pass error details, code context
```

---

## 📡 COMMUNICATION CHANNELS

### Shared Resources

**1. Shared Knowledge Base**
- Location: `~/.openclaw/workspace/AGENT_ARMY_KNOWLEDGE.md`
- Access: All agents (read/write)
- Purpose: Agent specialties, routing matrix, performance tips

**2. Memory Repository**
- Location: `~/.openclaw/workspace/MEMORY.md`
- Access: Commander (write), All agents (read)
- Purpose: System learnings, patterns, history

**3. Agent-Local Memory**
- Location: `~/.openclaw/workspace-[agent-name]/MEMORY.md`
- Access: Specific agent only
- Purpose: Agent-specific learnings and patterns

**4. Coordination Log**
- Location: `~/.openclaw/workspace/AGENT_COORDINATION_LOG.md`
- Access: Commander (write), All agents (read)
- Purpose: Track handoffs, collaborations, outcomes

### Signaling Mechanisms

**Direct Command (Main Agent):**
```
@atlas [task description]
```

**Broadcast Announcement:**
```markdown
## 📢 ARMY BROADCAST
From: Main Agent
Topic: [Topic]
Message: [Content]
```

**Status Reporting:**
```markdown
## STATUS REPORT
Agent: [Agent Name]
Status: [Ready/Busy/Idle]
Current Task: [Description]
Capacity: [Available/Avg/Full]
```

---

## 🎯 COLLABORATION SCENARIOS

### Scenario 1: Complex Multi-Stage Task
**User Request:** "Build a full-stack web app with authentication"

```
Main Agent → Analyze request
      ↓
Atlas (Architecture)
  - Design system architecture
  - Plan data models
  - Define API structure
      ↓
Handoff to Flash (Backend Draft)
  - Generate backend API
  - Set up database schemas
      ↓
Handoff to Coder (Backend Refine)
  - Optimize code
  - Add error handling
      ↓
Handoff to Nova (Frontend Draft)
  - Generate UI components
  - Build frontend logic
      ↓
Handoff to Coder (Frontend Refine)
  - Polish UI code
  - Add interactions
      ↓
Handoff to Orion (Integration Testing)
  - Test all components
  - Debug issues
      ↓
Handoff to Zen (Final Review)
  - Deep analysis
  - Security review
  - Performance check
      ↓
Main Agent → Present final solution
```

### Scenario 2: Emergency Debugging
**User Request:** "Production API is down!"

```
Main Agent → Route to Orion (Priority)
      ↓
Orion (Emergency Response)
  - Immediate error analysis
  - Identify root cause
  - Propose hotfix
      ↓
Handoff to Coder (Hotfix Implementation)
  - Apply urgent fix
  - Minimal code changes
      ↓
Handoff to Atlas (Post-Incident Review)
  - Document incident
  - Suggest prevention
      ↓
Main Agent → Report resolution
```

### Scenario 3: Large-Scale Research
**User Request:** "Analyze this 500-page technical document"

```
Main Agent → Detect large file
      ↓
Luna (Large Context Processing)
  - Process 1M token document
  - Extract key points
  - Structure findings
      ↓
Handoff to Atlas (Analysis)
  - Analyze structure
  - Identify patterns
      ↓
Handoff to Zen (Deep Analysis)
  - Synthesize insights
  - Extract key learnings
      ↓
Main Agent → Present comprehensive report
```

### Scenario 4: Real-Time Performance Optimization
**User Request:** "This code is too slow, optimize it"

```
Main Agent → Route to Coder
      ↓
Coder (Initial Optimization)
  - Profile code
  - Identify bottlenecks
  - Apply immediate optimizations
      ↓
Handoff to Flash (Speed Testing)
  - Benchmark improved code
  - Measure performance gains
      ↓
If still slow → Handoff to Atlas (Architecture Review)
  - Consider architectural changes
  - Propose algorithm improvements
      ↓
Main Agent → Document results
```

---

## 🔄 WORKFLOW AUTOMATION PATTERNS

### Pattern 1: Parallel Execution
**When:** Multiple independent tasks

```
Main Agent → Split request into subtasks
      ↓
Task 1 → Agent A ┐
Task 2 → Agent B ├┴→ Main Agent (Consolidate)
Task 3 → Agent C ┘
```

**Example:** "Analyze these 3 different APIs"
- Agent A analyzes API 1
- Agent B analyzes API 2
- Agent C analyzes API 3
- Main agent consolidates results

### Pattern 2: Sequential Pipeline
**When:** Tasks depend on previous results

```
Agent A → Agent B → Agent C → Main Agent
  ↓         ↓         ↓
Stage 1   Stage 2   Stage 3
```

**Example:** "Review and improve this codebase"
- Coder: Initial code review
- Atlas: Architecture review
- Zen: Deep analysis
- Main agent: Final report

### Pattern 3: Veto Process
**When:** Critical decisions require consensus

```
Task → Agent A (Proposal)
       ↓
    Agent B (Review) ←━ If rejected, return to Agent A
       ↓
    Agent C (Validation)
       ↓
    Main Agent (Decision)
```

**Example:** "Propose a database architecture"
- Atlas: Propose architecture
- Luna (review): Review against requirements
- Zen: Validate against best practices
- Main agent: Make final decision

### Pattern 4: Specialist Consultation
**When:** General agent needs specialist input

```
General Agent (e.g., Nova)
       ↓
    Detect Specialist Need
       ↓
Consult Specialist (e.g., Coder)
       ↓
    Apply Recommendations
       ↓
    Continue with Task
```

**Example:** "Generate a REST API"
- Nova: Generates basic API
- Atlas: Reviews architecture
- Coder: Optimizes code patterns
- Orion: Tests and debugs if needed

### Pattern 5: Sub-Agent Spawning (NEW - 2026-02-18)
**When:** Multiple background research or processing tasks needed

```
Main Agent (Commander)
       ↓
    Identify Parallelizable Tasks
       ↓
Spawn Subagents (up to 8 concurrent)
       ↓
Subagent 1 → Isolated Session ┐
Subagent 2 → Isolated Session ├┴→ Main Agent (Auto-Report)
Subagent 3 → Isolated Session ┘
       ↑
    Results automatically sent back
       ↓
Main Agent → Consolidate & Present
```

**Features:**
- Up to 8 subagents can run concurrently
- Each subagent in isolated session
- Results auto-report to main agent (no need to fetch)
- Subagents are ephemeral (terminate after task)
- Non-initiating (no proactive actions)

**Examples:**
- "Research these 5 skills from inventory" → Spawn 5 subagents, each researches one skill
- "Analyze these 10 agent workspaces" → Spawn subagents for each workspace
- "Generate content for 3 platforms" → Spawn subagents for each platform
- "Process all markdown files in workspace" → Batch file processing

**When to Use:**
- ✅ Independent research tasks
- ✅ Parallel code analysis
- ✅ Batch file processing
- ✅ Multi-platform content generation
- ❌ Tasks requiring shared context
- ❌ Coordinated decision-making

**Tool:** `sessions_spawn(task, label, model, timeoutSeconds)`

**Documentation:** See SUB_AGENT_SPAWNING.md for complete guide

---

## ⚡ EFFICIENCY PROTOCOLS

### 1. Task Parallelization
- Identify independent subtasks
- Assign to different agents simultaneously
- Consolidate results at the end

### 2. Agent Caching
- After an agent completes a task, cache the context
- Similar future tasks reuse cached context
- Reduces redundant work

### 3. Context Sharing
- Handoffs include full work state
- No need to re-analyze previous work
- Faster collaboration

### 4. Agent Specialization Alignment
- Always route to the most suitable agent first
- Avoid unnecessary agent switches
- Minimize handoff overhead

### 5. Error Recovery Cascade
```
Agent A encounters error
       ↓
    Document error
       ↓
    Handoff to Agent B (specialist in this error type)
       ↓
    Agent B fixes or escalates
       ↓
   Update error patterns for future
```

---

## 📊 PERFORMANCE MONITORING

### Agent-Level Metrics
 tracked per agent:
- **Task Completion Rate:** Percentage of tasks completed successfully
- **Average Response Time:** Time from task assignment to completion
- **Quality Score:** User satisfaction and accuracy rate
- **Token Efficiency:** Tokens used per task type
- **Handoff Quality:** How well handoffs are received

### Collaboration Metrics
- **Handoff Success Rate:** Successful handoffs / total handoffs
- **Agent Switch Frequency:** How many agents per task
- **Parallel Execution Gain:** Time saved from parallelization
- **Conflict Rate:** When agents disagree on approach

### System-Wide Metrics
- **Overall Throughput:** Tasks per hour
- **Total Cost:** Tokens across all agents
- **User Satisfaction:** Average rating
- **Uptime/Availability:** Agent availability

---

## 🛡️ CONFLICT RESOLUTION PROTOCOLS

### Scenario: Agents Disagree
```
Agent A proposes solution X
Agent B proposes solution Y
      ↓
Both present to Main Agent
      ↓
Main Agent decides based on:
  - Task requirements
  - Performance considerations
  - Cost implications
  - Quality requirements
      ↓
Main Agent selects best solution
      ↓
Update learning patterns for future
```

### Scenario: Agent Capacity Full
```
Task assigned to Agent A
      ↓
Agent A reports: "Capacity Full"
      ↓
Main Agent routes to backup agent:
  - Coders: Flash or Nova
  - Analyst: Atlas or Zen
  - Quick tasks: Spark
      ↓
If backup also full: Queue task or escalate to Commander
```

### Scenario: Agent Failure/Error
```
Agent A fails or errors out
      ↓
Document error type
      ↓
Check error patterns:
  - Known error? → Apply known fix
  - New error? → Handoff to specialist
      ↓
If no resolution available → Escalate to Commander
      ↓
Main Agent takes over or routes to alternative
```

---

## 🎯 AUTOMATIC ROUTING RULES

### Task Keyword → Agent Mapping
```json
{
  "architecture|design|plan": "atlas",
  "debug|error|fix|troubleshoot": "orion",
  "code|program|function|class": "coder",
  "vision|image|screenshot|photo": "vision",
  "quick|fast|simple|small": "spark",
  "deep|complex|analyze|research": "zen",
  "large|big|huge document|many files": "luna",
  "draft|generate|create new": "flash",
  "balanced|standard|typical": "nova",
  "heavy|computation|complex math": "titan",
  "scale|comprehensive|large scale": "max"
}
```

### Context-Aware Routing
```
IF context_size > 200k tokens AND agent != luna:
    → Route to Luna

IF task includes "vision" or "image":
    → Route to Vision

IF task has "urgent" or "emergency":
    → Route to Orion (priority)

IF user requests specific agent:
    → Honor request
```

---

## 📋 AGENT STATUS CHECK PROTOCOL

### Daily Status Report (from each agent)
```markdown
## STATUS REPORT
Agent: [Name]
Date: [YYYY-MM-DD]

### Available: Yes/No
### Current Load: [0-100%]

### Tasks Completed Today: [Number]
  - Task 1: [Description] - Duration
  - Task 2: [Description] - Duration

### Issues Encountered: [List]
### Learnings: [List]

### Requests for Main Agent: [List]
```

### Coordination Log Entry
```markdown
## COORDINATION EVENT
Time: [Timestamp]
Agents Involved: [Agent A, Agent B, ...]
Type: [Handoff|Collaboration|Broadcast]

Description:
[What happened]

Context:
[Any relevant context]

Result:
[Outcome]

Learnings:
[Any patterns discovered]
```

---

## 🚀 CONTINUOUS IMPROVEMENT

### After Each Task
1. **Document**: What worked well?
2. **Analyze**: What could be improved?
3. **Share**: Update agent knowledge base
4. **Optimize**: Adjust routing rules

### Weekly Coordination Review
1. **Analyze handoff patterns**
2. **Identify bottlenecks**
3. **Adjust agent specializations**
4. **Update routing rules**

### Monthly Army Assessment
1. **Performance review** (all agents)
2. **Skill gap analysis**
3. **Agent capacity planning**
4. **Coordination protocol update**

---

*Coordination Protocol Established: 2026-02-18 | Agent Army Strength: 11*
