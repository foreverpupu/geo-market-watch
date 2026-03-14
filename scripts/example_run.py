#!/usr/bin/env python3
"""
Geo Market Watch - Example Run

Demonstrates basic usage of scoring and trigger engines.
"""

import sys
from pathlib import Path

# Add engine directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from scoring_engine import score_event
from trigger_engine import evaluate_trigger


def main():
    """Run example event through engines."""
    
    # Example event: Red Sea shipping disruption
    event = {
        "event_title": "Red Sea shipping disruption",
        "date_detected": "2024-01-12",
        "region": "Middle East",
        "category": "Maritime disruption",
        "indicators": {
            "physical_disruption": 1,
            "transport_impact": 2,
            "policy_sanctions": 0,
            "market_transmission": 1,
            "escalation_risk": 1
        }
    }
    
    print("=" * 60)
    print("Geo Market Watch - Example Run")
    print("=" * 60)
    print()
    
    print(f"Event: {event['event_title']}")
    print(f"Date: {event['date_detected']}")
    print(f"Region: {event['region']}")
    print()
    
    # Run scoring engine
    print("Running Scoring Engine...")
    score_result = score_event(event)
    print(f"  Score: {score_result['score']}")
    print(f"  Band: {score_result['band']}")
    print()
    
    # Run trigger engine
    print("Running Trigger Engine...")
    trigger_data = {
        "event_title": event["event_title"],
        "score": score_result["score"],
        "flags": {
            "confirmed_supply_disruption": False,
            "strategic_transport_disruption": False,
            "major_sanctions_escalation": False,
            "military_escalation": False
        }
    }
    trigger_result = evaluate_trigger(trigger_data)
    print(f"  Trigger Full Analysis: {trigger_result['trigger_full_analysis']}")
    if trigger_result["reasons"]:
        print(f"  Reasons: {', '.join(trigger_result['reasons'])}")
    else:
        print("  Reasons: None (score below threshold, no escalation flags)")
    print()
    
    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
