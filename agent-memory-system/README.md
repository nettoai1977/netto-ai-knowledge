# Self-Organizing Agent Memory System

A self-organizing memory system for AI agents that structures interactions into persistent, meaningful knowledge units.

---

## 📁 Files

- **memory_db.py** - SQLite database with FTS5 full-text search
- **memory_manager.py** - Memory extraction and consolidation
- **agent_memory_integration.py** - Integration layer with OpenClaw/Nanobot
- **import_historical_data.py** - Import script for MEMORY.md
- **agent_memory.db** - SQLite database (created on first run)

---

## 🚀 Quick Start

### Basic Usage

```python
from agent_memory_integration import get_agent_memory

# Initialize memory system
memory = get_agent_memory()

# Update memory with interaction
memory.update(
    user="I want to deploy cron automation",
    assistant="I'll help you set up daily and weekly cron jobs."
)

# Retrieve context
context = memory.retrieve_context("cron automation")
print(context)

# Get statistics
stats = memory.get_statistics()
print(f"Total cells: {stats['total_cells']}")
print(f"Total scenes: {stats['total_scenes']}")
```

### Import Historical Data

```bash
cd /Users/michaelnetto/.openclaw/workspace/agent-memory-system
python import_historical_data.py
```

---

## 📊 Memory Cell Types

| Type | Emoji | Description | Example |
|------|-------|-------------|---------|
| **fact** | 📌 | Facts learned | "Week 3 productivity gain: 2.5x" |
| **plan** | 📋 | Future plans | "Week 5: Deploy cron automation" |
| **preference** | ❤️ | User preferences | "User prefers Option 1 (direct action)" |
| **decision** | ✅ | Decisions made | "Skip manual cron testing, deploy direct" |
| **task** | ⏰ | Tasks pending | "Task 5: Integrate Cloudflare + Mistral" |
| **risk** | ⚠️ | Risks identified | "API rate limits limit subagent to 3-4 concurrent" |

---

## 🔍 Search & Retrieval

### Retrieve Context
```python
context = memory.retrieve_context("week 5 cron tasks", limit=6)
```

### List All Scenes
```python
scenes = memory.list_all_scenes()
print(scenes)
```

### Search by Type
```python
tasks = memory.search_by_type("task", limit=10)
print(tasks)
```

### Get Scene Details
```python
details = memory.get_scene_details("user-preferences")
print(details)
```

### Search Memory
```python
results = memory.search_memory("automation")
print(results)
```

---

## 💡 Integration with OpenClaw/Nanobot

### Step 1: Add to Your Skill Directory

```bash
cd /Users/michaelnetto/.openclaw/skills/
mkdir agent-memory-skill
cd agent-memory-skill
```

### Step 2: Create Skill File (SKILL.md)

```markdown
# Agent Memory Skill

Enhance your agent with long-term memory capabilities.

## Features

- Automated memory extraction from interactions
- Scene-based organization
- Salience scoring
- Full-text search retrieval
- Long-horizon reasoning

## Usage

### Initialize
```
import sys
sys.path.append("/Users/michaelnetto/.openclaw/workspace/agent-memory-system")
from agent_memory_integration import get_agent_memory

memory = get_agent_memory()
```

### Update Memory
```
memory.update(user_message, assistant_response)
```

### Retrieve Context
```
context = memory.retrieve_context(query)
```

## Database Location

`/Users/michaelnetto/.openclaw/workspace/agent-memory-system/agent_memory.db`
```

### Step 3: Test Integration

```bash
cd /Users/michaelnetto/.openclaw/workspace/agent-memory-system

# Test without historical import
python agent_memory_integration.py

# Import historical data
python import_historical_data.py
```

---

## 📈 Memory Cell Flow

```
1. INTERACTION
   User: "Deploy cron automation now"
   Agent: "Adding crontab entries..."

2. EXTRACT CELLS
   MemoryManager extracts from interaction:
   [
     {
       "scene": "week-5-cron-deployment",
       "cell_type": "task",
       "salience": 0.9,
       "content": "Deploy cron automation (Task 1)"
     }
   ]

3. STORE IN DATABASE
   - Insert into mem_cells (structured storage)
   - Insert into mem_cells_fts (searchable index)

4. CONSOLIDATE SCENE
   - Summarize all cells in scene
   - Scene summary: "Week 5 Task 1: Deploy cron automation to daily (8AM) and weekly (Sunday 10AM)"

5. RETRIEVAL (Future Queries)
   - Full-text search by scene/content
   - Fallback to salience-based retrieval
   - Assemble context summaries for reasoning
```

---

## 🎯 Example: Memory Cells from Your System

```json
[
  {
    "scene": "week-3-productivity",
    "cell_type": "fact",
    "salience": 0.9,
    "content": "Week 3 productivity gain: 2.5x vs Week 1 baseline"
  },
  {
    "scene": "week-5-cron-deployment",
    "cell_type": "plan",
    "salience": 0.95,
    "content": "Task 1: Deploy cron automation (daily 8AM, weekly Sunday 10AM)"
  },
  {
    "scene": "user-preferences",
    "cell_type": "preference",
    "salience": 0.85,
    "content": "User prefers direct action (Option 1, 'Yes continue', 'Proceed')"
  },
  {
    "scene": "subagent-capacity",
    "cell_type": "risk",
    "salience": 0.75,
    "content": "API rate limits limit practical subagent capacity to 3-4 concurrent"
  },
  {
    "scene": "free-api-providers",
    "cell_type": "task",
    "salience": 0.8,
    "content": "Task 5: Integrate Cloudflare + Mistral La Plateforme ($550/month savings)"
  }
]
```

---

## 📊 Features

### Automated Memory Extraction
- Extracts structured cells from interactions
- 6 cell types (fact, plan, preference, decision, task, risk)
- Salience scoring (0-1 for importance)

### Scene-Based Organization
- Conversations auto-grouped into scenes/topics
- No manual topic assignment required
- Emergent organization through patterns

### Consolidated Summaries
- Automatic scene summaries for long-horizon reasoning
- Reduces token usage (summary << raw memory)
- Stable, reusable context

### Fast Retrieval
- SQLite FTS5 full-text search
- Salience-based fallback
- Semantic+structured retrieval

### Long-Horizon Reasoning
- Stable scene summaries persist across sessions
- Context maintained without re-reading logs
- Improved consistency and groundedness

---

## 🔧 Configuration

### Database Path
Default: `/Users/michaelnetto/.openclaw/workspace/agent-memory-system/agent_memory.db`

Change by passing `db_path`:
```python
from memory_db import get_memory_db
db = get_memory_db("/custom/path/to/memory.db")
```

### LLM Provider (Optional)
For better extraction/consolidation, provide an LLM function:

```python
def my_llm(prompt, temperature=0.1, max_tokens=500):
    # Use your GLM-4.7 model
    return llm_call(prompt)

from agent_memory_integration import get_agent_memory
memory = get_agent_memory(llm_provider=my_llm)
```

---

## 📚 How It Works

### MemoryDB Class
- **Three tables:**
  - `mem_cells` - Atomic memory units
  - `mem_scenes` - Scene summaries
  - `mem_cells_fts` - Full-text search index

### MemoryManager Class
- **Extraction:** Converts interactions into structured cells
  - LLM-based (if provider provided)
  - Rule-based fallback (if no LLM)
- **Consolidation:** Summarizes cells into stable scene summaries

### AgentMemoryIntegration Class
- **Integration layer** between memory system and OpenClaw/Nanobot
- **Methods:** update(), retrieve_context(), list_all_scenes(), search_by_type(), etc.

---

## 🚀 Next Steps

### With LLM Provider
1. Implement LLM function using NVIDIA GLM-4.7
2. Pass to `get_agent_memory(llm_provider=my_llm)`
3. Better extraction/consolidation quality

### Without LLM Provider (Current)
- Uses rule-based extraction (simpler, faster)
- Works immediately, no additional setup
- Can upgrade to LLM later

---

## 📊 Statistics

After importing historical data:

```python
from agent_memory_integration import get_agent_memory

memory = get_agent_memory()
stats = memory.get_statistics()

print(f"Total cells: {stats['total_cells']}")
print(f"Total scenes: {stats['total_scenes']}")
print(f"Cells by type:")
for cell_type, count in stats['cells_by_type'].items():
    print(f"  {cell_type}: {count}")
```

---

## 🔍 Testing

```bash
# Test without historical import
python agent_memory_integration.py

# Test with historical import
python import_historical_data.py

# View database statistics
python -c "
from agent_memory_integration import get_agent_memory
memory = get_agent_memory()
print(memory.get_statistics())
"
```

---

## 📄 License

Open-source, for use with your agent army system.

---

**Last Updated:** February 18, 2026

---

*Self-Organizing Agent Memory System - Integration Complete* ✅
