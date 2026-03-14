#!/usr/bin/env python3
"""
Geo Market Watch - Benchmark Runner

Validates scoring and trigger engines against real-world events.
"""

import json
import sys
from pathlib import Path

# Add engine directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from scoring_engine import score_event
from trigger_engine import evaluate_trigger


def load_benchmark_events() -> list:
    """Load benchmark events from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "benchmark-events.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    return data["events"]


def run_benchmark() -> dict:
    """
    Run benchmark test against all events.
    
    Returns:
        Dict with test results and statistics
    """
    events = load_benchmark_events()
    
    results = {
        "total": len(events),
        "scoring_passed": 0,
        "scoring_failed": 0,
        "trigger_passed": 0,
        "trigger_failed": 0,
        "details": []
    }
    
    print("=" * 60)
    print("Geo Market Watch v5.4 Benchmark")
    print("=" * 60)
    print()
    
    for event in events:
        event_id = event["event_id"]
        event_title = event["event_title"]
        
        print(f"Testing: {event_id} - {event_title}")
        
        # Test scoring engine
        try:
            score_result = score_event(event)
            score_correct = (
                score_result["score"] == event["expected_score"] and
                score_result["band"] == event["expected_band"]
            )
            
            if score_correct:
                results["scoring_passed"] += 1
                score_status = "✓ PASS"
            else:
                results["scoring_failed"] += 1
                score_status = "✗ FAIL"
            
            print(f"  Score: {score_result['score']} (expected {event['expected_score']}) {score_status}")
            print(f"  Band: {score_result['band']} (expected {event['expected_band']})")
            
        except Exception as e:
            results["scoring_failed"] += 1
            print(f"  Score: ERROR - {e}")
            score_correct = False
        
        # Test trigger engine
        try:
            trigger_data = {
                "event_title": event["event_title"],
                "score": event["expected_score"],
                "flags": event["flags"]
            }
            trigger_result = evaluate_trigger(trigger_data)
            trigger_correct = trigger_result["trigger_full_analysis"] == event["expected_trigger"]
            
            if trigger_correct:
                results["trigger_passed"] += 1
                trigger_status = "✓ PASS"
            else:
                results["trigger_failed"] += 1
                trigger_status = "✗ FAIL"
            
            print(f"  Trigger: {trigger_result['trigger_full_analysis']} (expected {event['expected_trigger']}) {trigger_status}")
            if trigger_result["reasons"]:
                print(f"  Reasons: {', '.join(trigger_result['reasons'])}")
            
        except Exception as e:
            results["trigger_failed"] += 1
            print(f"  Trigger: ERROR - {e}")
            trigger_correct = False
        
        results["details"].append({
            "event_id": event_id,
            "event_title": event_title,
            "score_correct": score_correct,
            "trigger_correct": trigger_correct
        })
        
        print()
    
    return results


def print_summary(results: dict):
    """Print benchmark summary."""
    print("=" * 60)
    print("Benchmark Summary")
    print("=" * 60)
    print()
    print(f"Total Events: {results['total']}")
    print()
    print("Scoring Engine:")
    print(f"  Passed: {results['scoring_passed']}/{results['total']}")
    print(f"  Failed: {results['scoring_failed']}/{results['total']}")
    print()
    print("Trigger Engine:")
    print(f"  Passed: {results['trigger_passed']}/{results['total']}")
    print(f"  Failed: {results['trigger_failed']}/{results['total']}")
    print()
    
    total_passed = results['scoring_passed'] + results['trigger_passed']
    total_tests = results['total'] * 2
    pass_rate = (total_passed / total_tests) * 100
    
    print(f"Overall Pass Rate: {pass_rate:.1f}%")
    print()
    
    if results['scoring_failed'] == 0 and results['trigger_failed'] == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


def main():
    """Main entry point."""
    results = run_benchmark()
    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
