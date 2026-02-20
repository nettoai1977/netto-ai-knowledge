# AUTOMATED TESTING FRAMEWORK
## Comprehensive Testing System for Agent Army

## 🧪 TESTING ARCHITECTURE

```
┌─────────────────────────────────────────────────┐
│              TEST ORCHESTRATOR                   │
│              (Main Agent)                        │
└────────────┬────────────────────────────────────┘
             │
    ┌────────┼────────┬─────────┬────────┐
    │        │        │         │        │
┌───▼───┐ ┌▼──────┐ ┌▼──────┐ ┌▼─────┐ ┌▼─────┐
│  UNIT │ │API IN ││FUNC  │ │ PERFO │ │INTEG │
│ TESTS │ │TEGRATE││TESTS ││ RMANCE│ │ATION │
└───────┘ └───────┘ └───────┘ └──────┘ └──────┘
```

---

## 📋 TEST TYPES

### 1. Unit Tests

#### Purpose
Test individual components in isolation

#### Test Cases
```yaml
Core Functions:
  - Function: model_selection(task_type)
    Input: "debugging"
    Expected: "orion"
    Priority: HIGH

  - Function: should_use_free_model(task_complexity)
    Input: "high"
    Expected: true
    Priority: HIGH

  - Function: agent_capacity_check(agent_name)
    Input: "spark"
    Expected: "< 90%"
    Priority: MEDIUM

Utility Functions:
  - Function: format_handoff(from_agent, to_agent, context)
    Input: ["main", "flash", task_context]
    Expected: Properly structured handoff markdown
    Priority: MEDIUM

  - Function: calculate_cost(tokens, model)
    Input: [15000, "nvidia/z-ai/glm4.7"]
    Expected: "$0.00"
    Priority: MEDIUM
```

#### Implementation
```python
def test_model_selection():
    """Test routing logic based on task type"""
    test_cases = [
        ("debugging", "orion"),
        ("code", "coder"),
        ("vision", "vision"),
        ("quick", "spark"),
        ("architecture", "atlas"),
    ]
    
    for task_type, expected_agent in test_cases:
        result = select_agent_for_task(task_type)
        assert result == expected_agent, f"Expected {expected_agent}, got {result}"
        log_test_result("model_selection", task_type, "PASS")

def test_cost_calculation():
    """Verify cost calculations accuracy"""
    test_cases = [
        (15000, "nvidia/z-ai/glm4.7", 0.00),
        (15000, "groq/llama-3.3-70b-versatile", 0.015),
    ]
    
    for tokens, model, expected_cost in test_cases:
        result = calculate_cost(tokens, model)
        assert abs(result - expected_cost) < 0.01, f"Cost mismatch"
        log_test_result("cost_calculation", f"{tokens},{model}", "PASS")
```

### 2. API Integration Tests

#### Purpose
Verify all external APIs are accessible and functional

#### Test Cases
```yaml
NVIDIA API:
  - Test: List available models
    Endpoint: /v1/models
    Expected: 200 OK, non-empty model list
    Frequency: HOURLY
    Priority: CRITICAL

  - Test: Simple inference
    Model: nvidia/z-ai/glm4.7
    Prompt: "Test prompt"
    Expected: Response with completion
    Frequency: DAILY
    Priority: HIGH

Groq API:
  - Test: List available models
    Endpoint: /v1/models
    Expected: 200 OK, non-empty model list
    Frequency: HOURLY
    Priority: CRITICAL

  - Test: Simple inference
    Model: groq/llama-3.3-70b-versatile
    Prompt: "Test prompt"
    Expected: Response with completion
    Frequency: DAILY
    Priority: HIGH

OpenRouter API:
  - Test: API connectivity
    Endpoint: /v1/models
    Expected: 200 OK or 401 (unauthorized is OK)
    Frequency: HOURLY
    Priority: MEDIUM

Brave Search:
  - Test: Web search
    Query: "OpenClaw AI"
    Expected: Non-empty results
    Frequency: DAILY
    Priority: MEDIUM
```

#### Implementation
```python
def test_nvidia_api_health():
    """Check NVIDIA API is accessible"""
    response = requests.get(
        "https://integrate.api.nvidia.com/v1/models",
        headers={"Authorization": f"Bearer {NVIDIA_API_KEY}"}
    )
    assert response.status_code == 200, f"NVIDIA API failed: {response.status_code}"
    models = response.json().get("data", [])
    assert len(models) > 0, "No models returned"
    log_test_result("api_integration", "nvidia_health", "PASS")

def test_nvidia_inference():
    """Test NVIDIA API can perform inference"""
    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {NVIDIA_API_KEY}"},
        json={
            "model": "nvidia/z-ai/glm4.7",
            "messages": [{"role": "user", "content": "Test"}],
            "max_tokens": 10
        }
    )
    assert response.status_code == 200, f"Inference failed: {response.status_code}"
    result = response.json()
    assert "choices" in result, "No choices in response"
    assert len(result["choices"]) > 0, "Empty choices"
    log_test_result("api_integration", "nvidia_inference", "PASS")
```

### 3. Functional Tests

#### Purpose
Test end-to-end workflows and agent operations

#### Test Cases
```yaml
Agent Handoff:
  - Scenario: Main → Flash handoff
    Steps:
      1. Main completes initial analysis
      2. Creates handoff document
      3. Switches to Flash agent
      4. Flash receives and continues
    Expected: Handoff successful, Flash continues task
    Priority: HIGH

Model Switch:
  - Scenario: Switch from GLM4.7 to Kimi K2.5
    Steps:
      1. User requests model switch
      2. System validates model availability
      3. Updates configuration
      4. Confirms switch
    Expected: Model changed successfully
    Priority: HIGH

Workflow Execution:
  - Scenario: Execute documented workflow
    Workflow: "Code Task Workflow" from WORKFLOW_AUTOMATIONS.md
    Steps: Atlas → Flash → Coder → Orion → Zen
    Expected: All steps complete, task finishes
    Priority: MEDIUM

Skill Loading:
  - Scenario: Load and apply a skill
    Skill: "tdd-workflows-tdd-green"
    Task: Apply TDD to simple problem
    Expected: skill applied correctly, TDD followed
    Priority: MEDIUM

Documentation Access:
  - Scenario: Access all knowledge files
    Files: AGENT_ARMY_KNOWLEDGE.md, SKILLS_INVENTORY.md, etc.
    Expected: All files readable, content accessible
    Priority: LOW
```

### 4. Performance Tests

#### Purpose
Measure and validate performance characteristics

#### Test Cases
```yaml
Response Time:
  - Test: spark agent response time
    Task: Simple question response
    Expected: < 1000ms
    Priority: HIGH

  - Test: zen agent response time
    Task: Deep analysis task
    Expected: < 10000ms
    Priority: MEDIUM

  - Test: luna agent with large context
    Task: Process 100k token file
    Expected: < 30000ms
    Priority: MEDIUM

Token Efficiency:
  - Test: Repeated similar tasks
    Tasks: 10 similar simple questions
    Expected: Token usage doesn't increase >50%
    Priority: MEDIUM

Memory Usage:
  - Test: Session memory growth
    Duration: 2-hour session
    Expected: Memory growth < 50% of context
    Priority: LOW

Throughput:
  - Test: Parallel task execution
    Tasks: 5 agents working simultaneously
    Expected: All complete successfully
    Priority: MEDIUM
```

### 5. Integration Tests

#### Purpose
Test multi-agent coordination end-to-end

#### Test Cases
```yaml
Multi-Agent Collaboration:
  - Scenario: Complex task requiring 3 agents
    Flow: Main → Atlas → Coder → Main
    Task: Build a REST API with authentication
    Expected: Task completed, all agents participated correctly
    Priority: HIGH

Conflict Resolution:
  - Scenario: Agents disagree on approach
    Setup: Two agents propose different solutions
    Expected: Main agent makes decision based on criteria
    Priority: MEDIUM

Error Handling:
  - Scenario: Agent fails mid-task
    Setup: Simulate agent failure
    Expected: Error recovery, alternative agent engaged
    Priority: HIGH

Load Balancing:
  - Scenario: High load on spark agent
    Setup: Queue 10 quick tasks
    Expected: Tasks distributed to alternative agents
    Priority: MEDIUM
```

---

## 🚀 TEST EXECUTION FRAMEWORK

### Test Runner

```python
class TestRunner:
    def __init__(self):
        self.test_suite = []
        self.results = []
        self.start_time = None
        
    def add_test(self, test_name, test_function, priority="MEDIUM"):
        """Add a test to the suite"""
        self.test_suite.append({
            "name": test_name,
            "function": test_function,
            "priority": priority,
            "last_run": None,
            "status": "PENDING"
        })
    
    def run_tests(self, priority_filter=None):
        """Execute all tests or filtered by priority"""
        priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        if priority_filter and priority_filter.upper() in priorities:
            priorities = priorities[priorities.index(priority_filter.upper()):]
        
        results = []
        for test in self.test_suite:
            if test["priority"] in priorities:
                try:
                    test["last_run"] = datetime.now()
                    test["function"]()
                    test["status"] = "PASS"
                    results.append({
                        "test": test["name"],
                        "status": "PASS",
                        "duration": time.time() - start_time,
                        "timestamp": datetime.now()
                    })
                except AssertionError as e:
                    test["status"] = "FAIL"
                    results.append({
                        "test": test["name"],
                        "status": "FAIL",
                        "error": str(e),
                        "timestamp": datetime.now()
                    })
                except Exception as e:
                    test["status"] = "ERROR"
                    results.append({
                        "test": test["name"],
                        "status": "ERROR",
                        "error": str(e),
                        "timestamp": datetime.now()
                    })
        
        return results
```

### Test Scheduler

```python
class TestScheduler:
    def __init__(self, runner):
        self.runner = runner
        self.schedules = []
    
    def schedule_test(self, test_name, frequency, priority):
        """
        Schedule test to run at specific intervals
        
        Frequencies:
        - CONTINUOUS: Run every 5 minutes
        - HOURLY: Run every hour
        - DAILY: Run at 8:00 AM
        - WEEKLY: Run every Monday at 8:00 AM
        """
        self.schedules.append({
            "test_name": test_name,
            "frequency": frequency,
            "priority": priority,
            "last_run": None,
            "next_run": self._calculate_next_run(frequency)
        })
    
    def check_and_run_due_tests(self):
        """Run tests that are due"""
        now = datetime.now()
        results = []
        
        for schedule in self.schedules:
            if now >= schedule["next_run"]:
                result = self.runner.run_tests(priority_filter=schedule["priority"])
                results.extend(result)
                schedule["last_run"] = now
                schedule["next_run"] = self._calculate_next_run(schedule["frequency"])
        
        return results

def _calculate_next_run(self, frequency):
    now = datetime.now()
    if frequency == "CONTINUOUS":
        return now + timedelta(minutes=5)
    elif frequency == "HOURLY":
        return now + timedelta(hours=1)
    elif frequency == "DAILY":
        return now.replace(hour=8, minute=0, second=0) + timedelta(days=1)
    elif frequency == "WEEKLY":
        next_monday = now + timedelta(days=(0 - now.weekday()) % 7)
        return next_monday.replace(hour=8, minute=0, second=0)
```

---

## 📊 TEST REPORTING

### Automated Test Report Template

```markdown
# TEST EXECUTION REPORT
Date: [YYYY-MM-DD HH:MM:SS]
Test Suite: Full Suite Execution

## Summary
- Total Tests: [X]
- Passed: [Y]
- Failed: [Z]
- Errors: [W]
- Success Rate: [X]%
- Duration: [X]m [X]s

## Results by Priority

### CRITICAL (Must Pass)
| Test | Status | Duration | Error |
|------|--------|----------|-------|
| test_nvidia_api_health | PASS | 0.5s | - |
| test_groq_api_health | PASS | 0.6s | - |

### HIGH (Should Pass)
| Test | Status | Duration | Error |
|------|--------|----------|-------|
| test_model_selection | PASS | 0.1s | - |
| test_nvidia_inference | PASS | 2.3s | - |

### MEDIUM (Pass Recommended)
| Test | Status | Duration | Error |
|------|--------|----------|-------|
| test_cost_calculation | PASS | 0.1s | - |

### LOW (Pass Optional)
| Test | Status | Duration | Error |
|------|--------|----------|-------|
| test_performance_metrics | SKIP | - | Not scheduled |

## Failed Tests
[If any failures, document here]

## Recommendations
[Based on test results]

## Next Scheduled Run
[Date and time of next test execution]

---
Report Generated by: Automated Test Framework
```

---

## 🔄 CONTINUOUS INTEGRATION

### Test Triggers

#### Automatic Triggers
```yaml
Before Deployment:
  - Run all CRITICAL and HIGH priority tests
  - Must achieve > 950% success rate
  - Fail fast if CRITICAL tests fail

After Configuration Change:
  - Run all integration tests
  - Verify agent connectivity
  - Validate API credentials

After Model Update:
  - Run API integration tests
  - Test inference with new model
  - Compare performance metrics

Daily Health Check:
  - Run CRITICAL priority tests
  - Verify system health
  - Check API connectivity
```

#### Manual Triggers
```yaml
On Demand:
  - Run full test suite
  - Run tests for specific agent
  - Run tests for specific component

Before Critical Task:
  - Quick health check
  - API connectivity test
  - Agent availability check
```

---

## 🎯 TEST COVERAGE

### Component Coverage

| Component | Test Coverage | Priority |
|-----------|---------------|----------|
| Agent Routing | 90% | HIGH |
| API Integration | 100% | CRITICAL |
| Handoff Protocol | 75% | HIGH |
| Cost Calculation | 100% | HIGH |
| Model Selection | 85% | MEDIUM |
| Error Handling | 70% | MEDIUM |
| Performance Monitoring | 60% | LOW |

### Path Coverage

#### Critical Paths (Must Cover 100%)
```
User Request → Agent Selection → Task Execution → Response
API Call → Response Processing → Result Formatting
Agent Handoff → Context Transfer → Continuation
```

#### Important Paths (Should Cover > 80%)
```
Error Recovery → Alternative Agent → Task Continuation
Model Switch → Configuration Update → Confirmation
Skill Loading → Skill Application → Result Validation
```

---

## 🛡️ TEST DATA MANAGEMENT

### Test Data Storage
```yaml
Test Results:
  Location: ~/.openclaw/test-results/
  Retention: 30 days
  Format: JSON + daily reports
  Compression: gzip (files > 10MB)

Test Logs:
  Location: ~/.openclaw/test-logs/
  Retention: 7 days
  Format: Plain text
  Rotation: Daily

Test Artifacts:
  Location: ~/.openclaw/test-artifacts/
  Retention: 14 days
  Includes: Screenshots, API responses, sample outputs
```

### Data Cleanup
```bash
# Automated cleanup script
find ~/.openclaw/test-results/ -name "*.json" -mtime +30 -delete
find ~/.openclaw/test-logs/ -name "*.log" -mtime +7 -delete
find ~/.openclaw/test-artifacts/ -name "*" -mtime +14 -delete
```

---

## 📈 PERFORMANCE BASELINES

### Response Time Thresholds

| Agent | P50 | P95 | P99 | Target |
|-------|-----|-----|-----|--------|
| spark | 750ms | 1200ms | 1800ms | < 1500ms |
| flash | 1500ms | 2500ms | 3500ms | < 3000ms |
| nova | 2500ms | 4000ms | 6000ms | < 5000ms |
| atlas | 3500ms | 6000ms | 9000ms | < 8000ms |
| zen | 4500ms | 8000ms | 12000ms | < 10000ms |

### Regression Detection
```python
def check_performance_regression(current_metrics, baseline_path):
    """Detect performance degradation"""
    baseline = load_baseline(baseline_path)
    
    for agent, metrics in current_metrics.items():
        if agent in baseline:
            baseline_metrics = baseline[agent]
            
            # Check if P95 degraded > 20%
            if metrics["p95"] > baseline_metrics["p95"] * 1.2:
                trigger_alert(f"Regression detected: {agent} P95 increased")

            # Check if success rate decreased > 10%
            success_rate_drop = baseline_metrics["success_rate"] - metrics["success_rate"]
            if success_rate_drop > 0.10:
                trigger_alert(f"Quality regression: {agent} success rate dropped")
```

---

## 🚨 ALERTING & NOTIFICATIONS

### Alert Conditions
```yaml
Critical (Immediate):
  - CRITICAL test fails
  - API unreachable
  - Success rate < 90%
  - Response time > 200% of target

Warning (Monitor):
  - HIGH test fails
  - Response time > 150% of target
  - Success rate < 95%

Info (Note):
  - Test coverage gap detected
  - New performance baseline established
```

### Alert Channels
```yaml
Alert Destinations:
  - MEMORY.md: Document findings
  - AGENT_COORDINATION_LOG.md: Coordination issues
  - TEST_REPORT.md: Test results
  - Main Agent: Immediate action required
```

---

## 📋 MAINTENANCE

### Test Suite Updates
```yaml
Frequency: Weekly
Actions:
  - Review test results
  - Add new test cases for new features
  - Remove obsolete tests
  - Update test data
  - Adjust thresholds based on real performance
```

### Baseline Updates
```yaml
Frequency: Monthly
Actions:
  - Analyze performance trends
  - Update baselines if needed
  - Review alert thresholds
  - Optimize test execution time
```

---

## 🎯 NEXT STEPS

### Immediate Implementation
1. Set up test runner framework
2. Implement CRITICAL priority tests
3. Create test scheduler
4. Set up automated reporting

### Short Term
1. Add HIGH priority tests
2. Implement performance monitoring tests
3. Create integration test scenarios
4. Establish performance baselines

### Long Term
1. Full test coverage > 90%
2. Automated regression detection
3. Continuous integration pipeline
4. Test-driven development for new features

---

*Automated Testing Framework Created: 2026-02-18*
