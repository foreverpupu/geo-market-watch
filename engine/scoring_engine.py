"""
Geo Market Watch - Minimal Scoring Engine

Converts Event Card indicators into a deterministic signal score (0-10).
"""

from typing import Dict, Any, Tuple

# Band definitions: (min_score, max_score, band_name)
BANDS = [
    (0, 3, "noise"),
    (4, 6, "monitor"),
    (7, 8, "full_analysis"),
    (9, 10, "major_shock"),
]

# Maximum scores per dimension
DIMENSION_MAX = {
    "physical_disruption": 3,
    "transport_impact": 2,
    "policy_sanctions": 2,
    "market_transmission": 2,
    "escalation_risk": 1,
}


def validate_indicators(indicators: Dict[str, int]) -> None:
    """
    Validate that indicators don't exceed their maximum values.
    
    Raises:
        ValueError: If any indicator is out of range or missing required keys.
    """
    for dimension, max_score in DIMENSION_MAX.items():
        if dimension not in indicators:
            raise ValueError(f"Missing required indicator: {dimension}")
        
        score = indicators[dimension]
        if not isinstance(score, int):
            raise ValueError(f"Indicator {dimension} must be an integer, got {type(score)}")
        
        if score < 0:
            raise ValueError(f"Indicator {dimension} cannot be negative: {score}")
        
        if score > max_score:
            raise ValueError(
                f"Indicator {dimension} exceeds maximum ({max_score}): {score}"
            )


def calculate_score(indicators: Dict[str, int]) -> int:
    """
    Calculate total signal score from indicators.
    
    Args:
        indicators: Dict with keys matching DIMENSION_MAX
        
    Returns:
        Total score (0-10)
    """
    validate_indicators(indicators)
    return sum(indicators.values())


def get_band(score: int) -> str:
    """
    Map score to signal band.
    
    Args:
        score: Signal score (0-10)
        
    Returns:
        Band name: "noise", "monitor", "full_analysis", or "major_shock"
    """
    for min_score, max_score, band in BANDS:
        if min_score <= score <= max_score:
            return band
    
    # Should never reach here if validation is correct
    raise ValueError(f"Score out of range: {score}")


def score_event(event_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point: score an Event Card and return result.
    
    Args:
        event_card: Dict with structure:
            {
                "event_title": str,
                "date_detected": str,
                "region": str,
                "category": str,
                "indicators": {
                    "physical_disruption": int (0-3),
                    "transport_impact": int (0-2),
                    "policy_sanctions": int (0-2),
                    "market_transmission": int (0-2),
                    "escalation_risk": int (0-1)
                }
            }
    
    Returns:
        Dict with:
            {
                "event_title": str,
                "score": int,
                "band": str
            }
    """
    if "indicators" not in event_card:
        raise ValueError("Event card must contain 'indicators' key")
    
    indicators = event_card["indicators"]
    score = calculate_score(indicators)
    band = get_band(score)
    
    return {
        "event_title": event_card.get("event_title", "Unknown"),
        "score": score,
        "band": band
    }


if __name__ == "__main__":
    # Example usage
    example_event = {
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
    
    result = score_event(example_event)
    print(f"Event: {result['event_title']}")
    print(f"Score: {result['score']}")
    print(f"Band: {result['band']}")
