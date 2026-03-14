"""
Geo Market Watch v5.5 — Intake Normalizer

Converts raw intake items into normalized Event Card format.
"""

import hashlib
import json
from typing import Dict, Any, List
from datetime import datetime


def generate_event_key(item: Dict[str, Any]) -> str:
    """
    Generate a unique key for deduplication.
    
    Uses headline + date for stable identification.
    """
    headline = item.get("headline", "")
    date = item.get("published_at", "")
    key_string = f"{headline}|{date}"
    return hashlib.md5(key_string.encode()).hexdigest()[:12]


def normalize_intake_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw intake item into normalized Event Card format.
    
    Args:
        item: Raw intake item with fields like headline, source, indicators, etc.
        
    Returns:
        Normalized event dict with standard Event Card structure
    """
    # Generate unique key for this event
    event_key = generate_event_key(item)
    
    # Extract or default required fields
    normalized = {
        "event_key": event_key,
        "event_title": item.get("headline", "Unknown Event"),
        "date_detected": item.get("published_at", datetime.now().isoformat()),
        "region": item.get("region", "Unknown"),
        "category": item.get("category", "Unclassified"),
        "source_name": item.get("source_name", "Unknown"),
        "source_url": item.get("source_url", ""),
        "summary": item.get("summary", ""),
        
        # Indicators for scoring (use provided or default to 0)
        "indicators": item.get("indicators", {
            "physical_disruption": 0,
            "transport_impact": 0,
            "policy_sanctions": 0,
            "market_transmission": 0,
            "escalation_risk": 0
        }),
        
        # Flags for trigger engine (use provided or default to False)
        "flags": item.get("flags", {
            "confirmed_supply_disruption": False,
            "strategic_transport_disruption": False,
            "major_sanctions_escalation": False,
            "military_escalation": False
        }),
        
        # Processing metadata
        "normalized_at": datetime.now().isoformat(),
        "version": "5.5"
    }
    
    return normalized


def normalize_intake_batch(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize a batch of intake items.
    
    Args:
        items: List of raw intake items
        
    Returns:
        List of normalized event dicts
    """
    return [normalize_intake_item(item) for item in items]


def load_intake_file(path: str) -> List[Dict[str, Any]]:
    """
    Load intake items from JSON file.
    
    Args:
        path: Path to JSON file containing intake items
        
    Returns:
        List of raw intake items
    """
    with open(path, 'r') as f:
        data = json.load(f)
        # Support both { "items": [...] } and [...] formats
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Intake file must contain a list or {items: [...]} structure")


if __name__ == "__main__":
    # Example usage
    example_item = {
        "source_name": "Reuters",
        "source_url": "https://example.com/red-sea",
        "published_at": "2024-01-12",
        "headline": "Red Sea shipping disruption",
        "region": "Middle East",
        "category": "Maritime disruption",
        "summary": "Major container lines reroute vessels due to security risks.",
        "indicators": {
            "physical_disruption": 1,
            "transport_impact": 2,
            "policy_sanctions": 0,
            "market_transmission": 1,
            "escalation_risk": 1
        },
        "flags": {
            "confirmed_supply_disruption": False,
            "strategic_transport_disruption": True,
            "major_sanctions_escalation": False,
            "military_escalation": False
        }
    }
    
    normalized = normalize_intake_item(example_item)
    print(f"Event Key: {normalized['event_key']}")
    print(f"Title: {normalized['event_title']}")
    print(f"Region: {normalized['region']}")
