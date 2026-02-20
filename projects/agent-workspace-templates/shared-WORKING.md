# WORKING.md — Shared Agent State

This file is the shared memory across all agent heartbeats.
Each agent reads this on wake to understand current state.
Update it constantly so context isn't lost between sessions.

---

## Current Focus

_What the squad is working on right now._

- **Main Agent:** Coordinator and orchestrator — managing tasks across specialist agents
- **Atlas 🧠:** Deep reasoning — available for architecture and analysis tasks
- **Luna 🌙:** Creative — available for naming and content tasks
- **Orion 🔭:** Technical analysis — available for code and system tasks
- **Nova 💫:** Strategy — available for planning and strategy tasks
- **Zen 🧘:** Contemplation — available for ethical and long-term analysis
- **Flash ⚡:** Speed — available for quick code solutions
- **Titan 🏔️:** Heavy computation — available for system design and scale tasks
- **Coder 💻:** Development — available for implementation and debugging
- **Max 💪:** Heavy lifting — available for codebase analysis and profiling
- **Spark ✨:** Quick wins — available for quick productivity tips
- **Vision 👁️:** Visual analysis — available for UI/UX design and visualization

---

## The Squad

| Agent    | Role             | Session Key          |
| -------- | ---------------- | -------------------- |
| Main     | Coordinator     | agent:main:main      |
| Atlas 🧠 | Deep Reasoning  | agent:atlas:main     |
| Luna 🌙  | Creative        | agent:luna:main      |
| Orion 🔭 | Technical       | agent:orion:main     |
| Nova 💫  | Strategy        | agent:nova:main      |
| Zen 🧘   | Contemplation   | agent:zen:main       |
| Flash ⚡  | Speed           | agent:flash:main     |
| Titan 🏔️| Heavy Compute   | agent:titan:main     |
| Coder 💻 | Development     | agent:coder:main     |
| Max 💪   | Heavy Lifting   | agent:max:main       |
| Spark ✨  | Quick Wins      | agent:spark:main     |
| Vision 👁️| Visual          | agent:vision:main    |

---

## Active Tasks

_No active tasks yet._

---

## Recently Completed

_Nothing completed yet._

---

## Agent Routing

When choosing an agent for a task, use this guide:

| Task Type                                 | Assign To                    |
| ----------------------------------------- | ---------------------------- |
| Architecture decisions                    | atlas 🧠                     |
| System design, scalability                | atlas 🧠 or titan 🏔️        |
| Creative naming, branding                | luna 🌙                      |
| Database analysis, query optimization    | orion 🔭                     |
| Product/feature strategy                 | nova 💫                      |
| Ethical analysis, long-term implications | zen 🧘                       |
| Quick code solutions, algorithms         | flash ⚡                     |
| Production code implementation            | coder 💻                     |
| Codebase analysis, performance profiling  | max 💪                       |
| Quick productivity tips                   | spark ✨                     |
| UI/UX design, dashboard layout          | vision 👁️                    |

For multi-agent tasks, create subtasks and assign each specialist their portion.

---

## Communication Protocol

- **Main Agent** coordinates and delegates to specialists
- **Specialists** report back to Main with results
- **Use shared files** for cross-agent context
- **Update this file** when tasks are created or completed

---

**Last Updated:** Initial setup — 2026-02-19
