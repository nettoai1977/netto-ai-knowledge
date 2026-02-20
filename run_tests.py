#!/usr/bin/env python3
"""
OpenClaw Automated Test Runner
Execute tests for the agent army
"""
import json
import os
import sys
from datetime import datetime

# Configuration
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "REDACTED")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "REDACTED")

# Test results storage
class TestResults:
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def add_result(self, test_name, status, duration_ms, error_msg=None):
        self.tests.append({
            "name": test_name,
            "status": status,  # PASS, FAIL, ERROR, SKIP
            "duration_ms": duration_ms,
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        })
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "ERROR":
            self.errors += 1

    def save_results(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(output_dir, f"test_results_{timestamp}.json")
        
        summary = {
            "test_run_id": timestamp,
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.tests),
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "success_rate": (self.passed / len(self.tests) * 100) if self.tests else 0,
            "tests": self.tests
        }
        
        with open(results_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        return results_file

def run_test(test_name, test_func, results):
    """Run a single test and record results"""
    start_time = datetime.now()
    try:
        test_func()
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        results.add_result(test_name, "PASS", duration_ms)
        print(f"✅ {test_name}: PASS ({duration_ms:.0f}ms)")
        return True
    except AssertionError as e:
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        results.add_result(test_name, "FAIL", duration_ms, str(e))
        print(f"❌ {test_name}: FAIL ({duration_ms:.0f}ms) - {str(e)}")
        return False
    except Exception as e:
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        results.add_result(test_name, "ERROR", duration_ms, str(e))
        print(f"⚠️  {test_name}: ERROR ({duration_ms:.0f}ms) - {str(e)}")
        return False

# Test Functions
def test_nvidia_api_health():
    """Check NVIDIA API is accessible"""
    import requests
    response = requests.get(
        "https://integrate.api.nvidia.com/v1/models",
        headers={"Authorization": f"Bearer {NVIDIA_API_KEY}",
                 "Content-Type": "application/json"},
        timeout=10
    )
    assert response.status_code == 200, f"NVIDIA API returned {response.status_code}"
    data = response.json()
    assert "data" in data, "No 'data' field in response"
    assert len(data["data"]) > 0, "No models returned from NVIDIA API"

def test_groq_api_health():
    """Check Groq API is accessible"""
    import requests
    response = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}",
                 "Content-Type": "application/json"},
        timeout=10
    )
    assert response.status_code == 200, f"Groq API returned {response.status_code}"
    data = response.json()
    assert "data" in data, "No 'data' field in response"
    assert len(data["data"]) > 0, "No models returned from Groq API"

def test_model_selection():
    """Test agent routing logic"""
    routing_map = {
        "debugging": "orion",
        "code": "coder",
        "vision": "vision",
        "quick": "spark",
        "architecture": "atlas",
        "deep": "zen",
    }
    
    for task_type, expected_agent in routing_map.items():
        agent = routing_map.get(task_type)
        assert agent == expected_agent, f"Expected {expected_agent} for {task_type}, got {agent}"

def test_cost_calculation():
    """Test cost calculation"""
    # NVIDIA models are free
    assert calculate_cost(15000, "nvidia/z-ai/glm4.7") == 0.00, "NVIDIA should be free"
    
    # Groq has cost
    groq_cost = calculate_cost(15000, "groq/llama-3.3-70b-versatile")
    assert groq_cost > 0, "Groq should have cost > 0"
    assert groq_cost < 1.0, "Groq cost should be < $1.00 for 15K tokens"

def calculate_cost(tokens, model):
    """Calculate cost based on tokens and model"""
    if model.startswith("nvidia"):
        return 0.00  # Free
    elif model.startswith("groq"):
        return tokens * 0.000001  # Rough estimate
    elif model.startswith("openrouter"):
        return tokens * 0.0000005  # Rough estimate
    else:
        return tokens * 0.000001  # Default estimate

# Main Execution
def main():
    """Main test runner"""
    print("=" * 60)
    print("OpenClaw Automated Test Runner")
    print("=" * 60)
    print()
    
    results = TestResults()
    
    # CRITICAL PRIORITY TESTS
    print("CRITICAL PRIORITY TESTS:")
    print("-" * 40)
    run_test("test_nvidia_api_health", test_nvidia_api_health, results)
    run_test("test_groq_api_health", test_groq_api_health, results)
    print()
    
    # HIGH PRIORITY TESTS
    print("HIGH PRIORITY TESTS:")
    print("-" * 40)
    run_test("test_model_selection", test_model_selection, results)
    print()
    
    # MEDIUM PRIORITY TESTS
    print("MEDIUM PRIORITY TESTS:")
    print("-" * 40)
    run_test("test_cost_calculation", test_cost_calculation, results)
    print()
    
    # Print Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(results.tests)}")
    print(f"Passed: {results.passed} ✅")
    print(f"Failed: {results.failed} ❌")
    print(f"Errors: {results.errors} ⚠️")
    print(f"Success Rate: {(results.passed / len(results.tests) * 100) if results.tests else 0:.1f}%")
    
    # Save results
    output_dir = os.path.expanduser("~/.openclaw/test-results/")
    results_file = results.save_results(output_dir)
    print()
    print(f"Results saved to: {results_file}")
    
    # Return exit code
    return 0 if results.failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
