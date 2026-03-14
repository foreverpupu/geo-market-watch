"""
Geo Market Watch - Minimal Trigger Engine

Decides whether Full Analysis Mode should be triggered based on signal score and flags.
"""

from typing import Dict, Any, List, Tuple


def check_trigger_conditions(
    score: int,
    flags: Dict[str, bool]
) -> Tuple[bool, List[str]]:
    """
    Check if any trigger conditions are met.
    
    Trigger conditions (from docs/full-analysis-trigger.md):
    1. score >= 7
    2. confirmed supply disruption
    3. strategic transport disruption
    4. major sanctions escalation
    5. military escalation
    
    Args:
        score: Signal score (0-10)
        flags: Dict with boolean trigger flags
        
    Returns:
        Tuple of (should_trigger, list_of_reasons)
    """
    reasons = []
    
    # Condition 1: Score threshold
    if score >= 7:
        reasons.append("score_threshold")
    
    # Condition 2: Confirmed supply disruption
    if flags.get("confirmed_supply_disruption", False):
        reasons.append("confirmed_supply_disruption")
    
    # Condition 3: Strategic transport disruption
    if flags.get("strategic_transport_disruption", False):
        reasons.append("strategic_transport_disruption")
    
    # Condition 4: Major sanctions escalation
    if flags.get("major_sanctions_escalation", False):
        reasons.append("major_sanctions_escalation")
    
    # Condition 5: Military escalation
    if flags.get("military_escalation", False):
        reasons.append("military_escalation")
    
    should_trigger = len(reasons) > 0
    return should_trigger, reasons


def evaluate_trigger(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point: evaluate whether to trigger Full Analysis Mode.
    
    Args:
        event_data: Dict with structure:
            {
                "event_title": str,
                "score": int,
                "flags": {
                    "confirmed_supply_disruption": bool,
                    "strategic_transport_disruption": bool,
                    "major_sanctions_escalation": bool,
                    "military_escalation": bool
                }
            }
    
    Returns:
        Dict with:
            {
                "event_title": str,
                "trigger_full_analysis": bool,
                "reasons": List[str]
            }
    """
    if "score" not in event_data:
        raise ValueError("Event data must contain 'score' key")
    
    if "flags" not in event_data:
        raise ValueError("Event data must contain 'flags' key")
    
    score = event_data["score"]
    flags = event_data["flags"]
    
    # Validate score range
    if not isinstance(score, int) or score < 0 or score > 10:
        raise ValueError(f"Score must be an integer between 0 and 10: {score}")
    
    should_trigger, reasons = check_trigger_conditions(score, flags)
    
    return {
        "event_title": event_data.get("event_title", "Unknown"),
        "trigger_full_analysis": should_trigger,
        "reasons": reasons
    }


if __name__ == "__main__":
    # Example usage
    example_event = {
        "event_title": "Russia expands oil export restrictions",
        "score": 7,
        "flags": {
            "confirmed_supply_disruption": False,
            "strategic_transport_disruption": False,
            "major_sanctions_escalation": True,
            "military_escalation": False
        }
    }
    
    result = evaluate_trigger(example_event)
    print(f"Event: {result['event_title']}")
    print(f"Trigger Full Analysis: {result['trigger_full_analysis']}")
    print(f"Reasons: {result['reasons']}")
