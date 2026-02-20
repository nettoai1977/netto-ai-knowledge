# ClawWork Configuration Template
## For Future Use - Task #6 (TODO.md)

**Created:** February 18, 2026
**Purpose:** ClawWork Competition Arena setup guide

---

## 📁 Repository Location

```
/Users/michaelnetto/.openclaw/workspace/ClawWork/
```

**Status:** ✅ cloned successfully (2,049 files)

---

## 🔑 Required API Keys

| Key | Purpose | Source | Free Tier? |
|-----|---------|--------|-----------|
| `OPENAI_API_KEY` | Agent model (GLM-4.7) | OpenRouter / SiliconFlow / OpenAI | ✅ Yes |
| `EVALUATION_API_KEY` | LLM evaluation (GPT-4o) | OpenAI (recommended) | ⚠️ No |
| `E2B_API_KEY` | Code execution sandbox | E2B.dev | ⚠️ No |
| `WEB_SEARCH_API_KEY` | Web search | Tavily / Jina | ✅ Yes |

---

## 🐍 Environment Setup Commands

```bash
cd /Users/michaelnetto/.openclaw/workspace/ClawWork

# Create Python 3.10+ environment
conda create -n clawwork python=3.10
conda activate clawwork

# Install dependencies
pip install -r requirements.txt
```

---

## 🔧 .env Configuration Template

```bash
# Copy the example
cp .env.example .env

# Edit .env with your keys:
OPENAI_API_KEY=your-key-here
OPENAI_API_BASE=https://openrouter.ai/api/v1  # For OpenRouter
EVALUATION_API_KEY=your-openai-key-here
EVALUATION_API_BASE=https://api.openai.com/v1
WEB_SEARCH_PROVIDER=tavily
WEB_SEARCH_API_KEY=your-tavily-key-here
E2B_API_KEY=your-e2b-key-here
```

---

## 🤖 Agent Configuration Template

**File:** `/Users/michaelnetto/.openclaw/workspace/ClawWork/livebench/configs/agent_army_config.json`

```json
{
  "livebench": {
    "date_range": {
      "init_date": "2026-02-18",
      "end_date": "2026-02-25"
    },
    "economic": {
      "initial_balance": 1000.0,
      "task_values_path": "./scripts/task_value_estimates/task_values.jsonl",
      "token_pricing": {
        "input_per_1m": 0.4,
        "output_per_1m": 1.5
      }
    },
    "agents": [
      {
        "signature": "atlas-glm47",
        "basemodel": "z-ai/glm-4.7",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "flash-glm5",
        "basemodel": "z-ai/glm5",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "vision-groq",
        "basemodel": "llama-4-scout-17b-16e-instruct",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": true
      },
      {
        "signature": "orion-deepseek",
        "basemodel": "deepseek/deepseek-v3.2",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "zen-kimi",
        "basemodel": "kimi-k2-thinking",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "titan-nemotron",
        "basemodel": "nvidia/nemotron-30b",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "coder-devstral",
        "basemodel": "mistralai/devstral-2-123b-instruct",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "max-mistral",
        "basemodel": "mistralai/mistral-large-3",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      },
      {
        "signature": "spark-ministral",
        "basemodel": "mistralai/ministral-14b-instruct",
        "enabled": true,
        "tasks_per_day": 1,
        "supports_multimodal": false
      }
    ],
    "agent_params": {
      "max_steps": 15,
      "max_retries": 3,
      "base_delay": 0.5,
      "tasks_per_day": 1
    },
    "evaluation": {
      "use_llm_evaluation": true,
      "meta_prompts_dir": "./eval/meta_prompts"
    },
    "data_path": "./livebench/data/agent_data",
    "gdpval_path": "./gdpval"
  }
}
```

---

## 🚀 Quick Start Commands

```bash
# Terminal 1: Start dashboard
./start_dashboard.sh

# Terminal 2: Run test agent
./run_test_agent.sh

# Browser: http://localhost:3000
```

---

## 📊 Competition Commands

```bash
# Run multi-agent competition
python -m livebench.agent.run_competition \
  --config livebench/configs/agent_army_config.json \
  --output results/agent_army_results.json

# View results
python -m livebench.analyze_leaderboard \
  --results results/agent_army_results.json
```

---

## 💰 Expected Results

**Metrics Measured:**
- **Survival days**: How long each agent stays solvent
- **Final balance**: Net economic result
- **Total work income**: Gross earnings from completed tasks
- **Profit margin**: (income - costs) / costs
- **Work quality**: Average quality score (0–1)
- **Token efficiency**: Income earned per dollar spent on tokens
- **Task completion rate**: Tasks completed / tasks assigned

**Expected Benchmark:**
- Top agents demonstrate $1,500+/hr equivalent earnings
- Compare GLM vs Kimi vs Qwen head-to-head
- Identify most productive agents in your army

---

## ⚙️ Troubleshooting

**Dashboard not updating:**
```bash
# Hard refresh browser
Ctrl+Shift+R
```

**Port conflicts:**
```bash
# Kill processes on ports 8000 and 3000
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Module errors:**
```bash
# Set Python path
export PYTHONPATH="/Users/michaelnetto/.openclaw/workspace/ClawWork:$PYTHONPATH"
```

---

## 📋 Setup Checklist

- [ ] Clone ClawWork ✅ COMPLETE
- [ ] Create Python 3.10+ env
- [ ] Install dependencies (pip install -r requirements.txt)
- [ ] Create .env file with API keys
- [ ] Create agent_army_config.json
- [ ] Configure 9 agents (use template above)
- [ ] Load GDPVal tasks (220 professional tasks)
- [ ] Start dashboard (http://localhost:3000)
- [ ] Run multi-agent competition
- [ ] Analyze leaderboard results
- [ ] Document findings

**Estimated Time:** 4 hours total (when ready)

---

## 🎯 Value Proposition

**Why Option C (Competition Arena):**
- Benchmarks all 11 agents head-to-head
- Identifies most productive agents for your use cases
- Provides scientific ROI data (earnings / token cost)
- Low risk: Isolated simulation, no production impact

**Alternatives:**
- **Option A** (Standalone simulation): 1-2 hours, test framework first
- **Option B** (ClawMode production): 2-3 hours, adds economic tracking

---

## 📚 Documentation References

**ClawWork README:** `/Users/michaelnetto/.openclaw/workspace/ClawWork/README.md`  
**ClawMode Integration:** `/Users/michaelnetto/.openclaw/workspace/ClawWork/clawmode_integration/README.md`  
**Configuration Examples:** `/Users/michaelnetto/.openclaw/workspace/ClawWork/livebench/configs/test_*.json`  
**Task #6:** See TODO.md (line 121-141)

---

## 🔄 When Ready to Proceed

1. Acquire required API keys (OPENAI_API_KEY, EVALUATION_API_KEY, E2B_API_KEY, WEB_SEARCH_API_KEY)
2. Follow "Setup Checklist" above
3. Report results on agent productivity
4. Update AGENT_ARMY_KNOWLEDGE.md with findings

---

**Status:** Setup template complete ✅  
**Next Action:** Wait until API keys acquired → return to complete setup

---

*Template Created: February 18, 2026*  
*Task #6 Status: PENDING - Ready when you are*

---
