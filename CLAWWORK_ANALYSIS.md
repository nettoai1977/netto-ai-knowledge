# ClawWork Analysis - AI Coworker Economic Framework
## Source: https://github.com/HKUDS/ClawWork
**Date:** February 18, 2026

---

## 🎯 What is ClawWork?

**ClawWork** transforms AI assistants into economically-accountable AI coworkers that must earn income by completing real professional tasks while paying for their own token usage.

---

## 💰 Key Concept: AI Economic Accountability

**The Challenge:**
- Most AI agents are cost centers (they consume tokens without generating revenue)
- No pressure to be cost-effective or productive
- Hard to quantify "real world" productivity

**The ClawWork Solution:**
- Agents pay for every token they generate
- Income only comes from completing quality professional work
- Must earn more than they spend to survive
- Economic metrics measure true productivity

---

## 📊 Economics System

### Starting Conditions
- **Initial Balance:** $10.00 (tight by design)
- **Token Costs:** Deducted automatically after each LLM call
- **API Costs:** Web search $0.0008/call (Tavily), code execution via E2B sandbox

### Payment System
```
Payment = quality_score × (estimated_hours × BLS_hourly_wage)
```

**Payment Range:**
- Task range: $82.78 – $5,004.00
- Average task value: $259.45
- Quality score range: 0.0 – 1.0

### Cost Tracking (per task)
- Input tokens: $2.50/1M tokens
- Output tokens: $10.00/1M tokens
- All costs tracked in `token_costs.jsonl`

**Example:**
```json
{
  "task_id": "abc-123",
  "llm_usage": {
    "total_input_tokens": 4500,
    "total_output_tokens": 900,
    "total_cost": 0.02025
  },
  "api_usage": {
    "search_api_cost": 0.0016
  },
  "cost_summary": {
    "total_cost": 0.02185
  },
  "balance_after": 1198.41
}
```

---

## 🏆 Live Economic Benchmark: GDPVal Dataset

**220 professional tasks** spanning **44 occupations** from the GDPVal dataset

### Occupations (4 Domains)

**1. Technology & Engineering**
- Computer & Information Systems Managers
- Software Developers

**2. Business & Finance**
- Financial Analysts
- Compliance Officers
- Financial Managers
- Auditors

**3. Healthcare & Social Services**
- Social Workers
- Health Administrators

**4. Legal & Government**
- Police Supervisors
- Administrative Managers

**5. Retail & Wholesale**
- Customer Service Representatives
- Sales Supervisors
- Purchasing Agents

**6. Real Estate**
- Property Managers
- Appraisers

### Task Types
- Word documents
- Excel spreadsheets
- PDFs
- Data analysis
- Project plans
- Technical specs
- Research reports
- Process designs

### Top Performance
- **Top agents achieve $1,500+/hr equivalent earnings**
- Exceeds typical human white-collar productivity
- Measured on 3 dimensions: work quality, cost efficiency, economic sustainability

---

## 🤖 Features & Capabilities

### 1. Live React Dashboard
**Real-time visualization at http://localhost:3000:**
- Balance chart (real-time line graph)
- Activity distribution (work vs learn)
- Economic metrics: income, costs, net worth, survival status
- Work tasks tab (all assigned tasks, payment amounts, quality scores)
- Learning tab (knowledge entries, timeline, searchable knowledge base)

### 2. Agent Tools (8 Tools Available)

**Economic Tools (4):**
- `decide_activity(activity, reasoning)` — Choose "work" or "learn"
- `submit_work(work_output, artifact_file_paths)` — Submit work for evaluation + payment
- `learn(topic, knowledge)` — Save knowledge to persistent memory (min 200 chars)
- `get_status()` — Check balance, costs, survival tier

**Productivity Tools (4):**
- `search_web(query, max_results)` — Web search (Tavily or Jina AI)
- `create_file(filename, content, file_type)` — Create documents (.txt, .xlsx, .docx, .pdf)
- `execute_code(code, language)` — Run Python in isolated E2B sandbox
- `create_video(slides_json, output_filename)` — Generate MP4 from text/image slides

### 3. Multi-Model Competition Arena
- **Supports different AI models:** GLM, Kimi, Qwen, and others
- **Head-to-head competition** to determine the "AI worker champion"
- **Real work performance** determines winner (not just benchmarks)

### 4. Drop-in OpenClaw/Nanobot Integration (ClawMode)

**What It Does:**
- Transforms any live Nanobot gateway into a money-earning coworker
- Every conversation costs tokens
- Income comes from completing real professional tasks
- Self-sustaining operation must earn more than it spends to survive

**What You Get:**
- All 9 nanobot channels (Telegram, Discord, Slack, WhatsApp, Email, Feishu, DingTalk, MoChat, QQ)
- All nanobot tools (read_file, write_file, exec, web_search, spawn, etc.)
- Plus 4 economic tools (decide_activity, submit_work, learn, get_status)
- Cost footer on every response: `Cost: $0.0075 | Balance: $999.99 | Status: thriving`

---

## 🏗️ Architecture

### System Components
```
ClawWork/
├── livebench/                          # Core simulation system
│   ├── agent/
│   │   ├── live_agent.py              # Main agent orchestrator
│   │   └── economic_tracker.py         # Balance, costs, income tracking
│   ├── work/
│   │   ├── task_manager.py             # GDPVal task loading
│   │   └── evaluator.py                # LLM-based work evaluation
│   ├── tools/
│   │   ├── direct_tools.py             # Core economic tools
│   │   └── productivity/               # Productivity tools
│   ├── api/
│   │   └── server.py                   # FastAPI backend + WebSocket
│   ├── prompts/
│   │   └── live_agent_prompt.py        # System prompts
│   └── configs/                        # Agent configuration files
├── clawmode_integration/               # OpenClaw/Nanobot integration
│   ├── agent_loop.py                   # ClawWorkAgentLoop + /clawwork command
│   ├── task_classifier.py              # Occupation classifier (40 categories)
│   ├── config.py                       # Plugin config
│   ├── provider_wrapper.py             # TrackedProvider (cost interception)
│   ├── cli.py                          # CLI commands
│   └── skill/
│       └── SKILL.md                    # Economic protocol skill
├── eval/
│   ├── meta_prompts/                   # Category-specific evaluation rubrics
│   └── generate_meta_prompts.py        # Meta-prompt generator
├── frontend/
│   └── src/                            # React dashboard
├── start_dashboard.sh                  # Launch backend + frontend
└── run_test_agent.sh                   # Run test agent
```

### Configuration
```json
{
  "livebench": {
    "date_range": {
      "init_date": "2025-01-20",
      "end_date": "2025-01-31"
    },
    "economic": {
      "initial_balance": 10.0,
      "token_pricing": {
        "input_per_1m": 2.5,
        "output_per_1m": 10.0
      }
    },
    "agents": [
      {
        "signature": "gpt-4o-agent",
        "basemodel": "gpt-4o",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": true
      }
    ],
    "evaluation": {
      "use_llm_evaluation": true,
      "meta_prompts_dir": "./eval/meta_prompts"
    }
  }
}
```

---

## 🚀 Quick Start

### Mode 1: Standalone Simulation
```bash
# Clone
git clone https://github.com/HKUDS/ClawWork.git
cd ClawWork

# Setup
conda create -n clawwork python=3.10
conda activate clawwork
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Configure
cp .env.example .env
# Edit .env with your keys: OPENAI_API_KEY, E2B_API_KEY, WEB_SEARCH_API_KEY

# Run (3 terminals)
./start_dashboard.sh           # Terminal 1 - dashboard
./run_test_agent.sh            # Terminal 2 - agent
# Browser → http://localhost:3000
```

### Mode 2: OpenClaw/Nanobot Integration (ClawMode)
See [clawmode_integration/README.md](https://github.com/HKUDS/ClawWork/blob/main/clawmode_integration/README.md) for full setup.

---

## 📈 Benchmark Metrics

**ClawWork Measures AI Coworker Performance Across:**

| Metric | Description |
|--------|-------------|
| **Survival days** | How long the agent stays solvent |
| **Final balance** | Net economic result |
| **Total work income** | Gross earnings from completed tasks |
| **Profit margin** | (income - costs) / costs |
| **Work quality** | Average quality score (0–1) across tasks |
| **Token efficiency** | Income earned per dollar spent on tokens |
| **Activity mix** | % work vs % learn decisions |
| **Task completion rate** | Tasks completed / tasks assigned |

---

## 💼 Productivity Outcomes (Example)

**Example Console Output:**
```
============================================================
📅 ClawWork Daily Session: 2025-01-20
============================================================

📋 Task: Buyers and Purchasing Agents — Manufacturing
 Task ID: 1b1ade2d-f9f6-4a04-baa5-aa15012b53be
 Max payment: $247.30

🔄 Iteration 1/15
 📞 decide_activity → work
 📞 submit_work → Earned: $198.44

============================================================
📊 Daily Summary - 2025-01-20
 Balance: $11.98 | Income: $198.44 | Cost: $0.03
 Status: 🟢 thriving
============================================================
```

---

## 🎯 Relevant to Agent Army?

**YES — Highly Relevant!** Reasons:

### 1. **OpenClaw Integration**
- ClawWork integrates directly with OpenClaw/Nanobot (same framework you're using!)
- ClawMode wrapper transforms any Nanobot gateway into economically-accountable agent
- Drop-in installation to your existing setup

### 2. **Productivity Benchmarking**
- Real-world work validation (220 professional tasks)
- Economic metrics measure true productivity (not just token counts)
- $1,500+/hr equivalent earnings benchmark for top agents

### 3. **Cost Optimization Pressure**
- Forces agents to be token-efficient (they pay for their own tokens)
- Economic accountability drives optimization
- Work vs learn decisions mimic real resource allocation

### 4. **Multi-Agent Competition**
- Models compete head-to-head on actual work performance
- Determine "AI worker champion" across GLM, Kimi, Qwen, etc.
- Could benchmark your 11-agent army!

---

## 🛠️ Integration Options

### Option 1: Run Standalone Simulation (RECOMMENDED - Start Here)
- Quick test environment with GDPVal tasks
- Learn the framework before full integration
- No risk to production system

**Estimated Time:** 1-2 hours setup + testing

### Option 2: Add ClawMode to Your OpenClaw Gateway
- Transform your agents into economically-accountable coworkers
- Every response shows cost footer (balance, income, spending)
- Agents must earn income from tasks to survive

**Estimated Time:** 2-3 hours integration
**Prerequisite:** OpenClaw/Nanobot instance running

### Option 3: Run Competition Arena (Benchmark Phase)
- Run multiple models (GLM, Kimi, Qwen) head-to-head
- Benchmark your 11 agent army performance
- Identify most productive agents

**Estimated Time:** 3-4 hours setup + run
**Value:** Scientific benchmark data on agent effectiveness

---

## 📊 Comparison: Your System vs ClawWork

| Aspect | Your Current System | ClawWork Framework |
|--------|------------------|-------------------|
| **Productivity Metric** | Token efficiency (8.5/10) | Economic efficiency ($ earned/$ spent) |
| **Task Validation** | 3 workflows (custom) | 220 professional tasks (GDPVal) |
| **Work Pressure** | Optimization-driven | Economic survival (must earn to survive) |
| **Benchmark** | 2.5-3x productivity gain | $1,500+/hr equiv earnings |
| **Integration** | OpenClaw/Nanobot | OpenClaw/Nanobot (same framework!) |
| **Dashboard** | HEARTBEAT checks (manual) | Live React dashboard (real-time) |
| **Multi-Model Support** | 11 agents configured | Multi-model competition arena |

---

## 🎯 Recommended Next Steps

### Immediate (This Week):
1. **Document ClawWork findings** ✅ (this file)
2. **Add to TODO.md** 🆕 (task below)
3. **Decide on integration approach** (Option 1/2/3)

### Medium (Next Week):
4. Run standalone simulation (test environment)
5. Assess framework value for your system

### Optional (Future):
6. Full ClawMode integration to production
7. Benchmark your 11-agent army in competition arena

---

## 📋 Task to Add to TODO.md

**Task #6:** Evaluate/Integrate ClawWork AI Coworker Framework

**Status:** NEW (priority: MEDIUM-LOW)

**Checklist:**
- [ ] Review ClawWork documentation
- [ ] Decide integration option:
  - Option 1: Run standalone simulation
  - Option 2: Add ClawMode to OpenClaw gateway
  - Option 3: Run competition arena benchmark
  - Option 4: Skip (not relevant now)
- [ ] [If Option 1] Clone and setup ClawWork locally
- [ ] [If Option 2] Integrate ClawMode with existing gateway
- [ ] [If Option 3] Set up multi-agent competition

**Priority:** MEDIUM-LOW (optimization, optional)
**Estimated Time:** 1-4 hours (depending on option)
**Value:** Economic accountability framework + productivity benchmarking

---

## 💡 Key Insights

1. **Economic Pressure Drives Quality** — Agents must earn to survive, forcing optimization
2. **Real-World Tasks Validate Capability** — 220 professional tasks (not artificial benchmarks)
3. **OpenClaw/Nanobot Native** — Same framework you're using, drop-in integration
4. **Multi-Model Competition** — Scientific benchmarking for agent selection

---

## ⚠️ Considerations

**Requirements:**
- Python 3.10+
- OPENAI_API_KEY (required for GPT-4o agent + LLM evaluation)
- E2B_API_KEY (required for code execution sandbox)
- Optional web search key (Tavily default)

**Trade-offs:**
- Economic pressure may reduce responsiveness (agents consider costs before acting)
- Requires new API keys (cost factor if not free tier)
- Learning curve (new framework semantics)

---

**Analysis Complete: February 18, 2026**

---

*Next Step: Decide on ClawWork integration approach*

---

## 🤔 What Would You Like to Do?

1. **Add ClawWork task to TODO (medium-low priority)** — evaluate later
2. **Integrate ClawMode now** — add economic accountability to production agents
3. **Run standalone simulation** — test framework before full integration
4. **Run competition arena** — benchmark your 11-agent army
5. **Skip** — not valuable for current needs
6. **Something else** (specify)

Which option would you like? 🎯
