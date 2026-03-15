"""
Geo Market Watch v5.5 — Agent Loop

Runs the full 4-node processing pipeline in a single process.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add engine directory to path
sys.path.insert(0, str(Path(__file__).parent))

from intake_normalizer import load_intake_file, normalize_intake_batch
from dedupe_memory import load_dedupe_memory
from scoring_engine import score_event
from trigger_engine import evaluate_trigger
from notifier import render_notification, write_notification


def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single event through scoring and trigger engines.
    
    Args:
        event: Normalized event dict
        
    Returns:
        Enriched event dict with score, band, and trigger info
    """
    # Run scoring engine
    score_result = score_event(event)
    event['score'] = score_result['score']
    event['band'] = score_result['band']
    
    # Run trigger engine
    trigger_data = {
        "event_title": event['event_title'],
        "score": event['score'],
        "flags": event.get('flags', {})
    }
    trigger_result = evaluate_trigger(trigger_data)
    event['trigger_full_analysis'] = trigger_result['trigger_full_analysis']
    event['trigger_reasons'] = trigger_result['reasons']
    
    return event


def ensure_directories(intake_path: str, dedupe_memory_path: str, output_dir: str = None):
    """
    Ensure all required directories exist.
    
    Creates parent directories for:
    - intake file (if path provided)
    - dedupe memory file
    - output directory (if provided)
    """
    # Ensure intake file parent directory exists
    if intake_path:
        intake_parent = Path(intake_path).parent
        if intake_parent:
            intake_parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure dedupe memory parent directory exists
    if dedupe_memory_path:
        dedupe_parent = Path(dedupe_memory_path).parent
        if dedupe_parent:
            dedupe_parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure output directory exists
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)


def run_agent_loop(
    intake_path: str,
    dedupe_memory_path: str,
    output_dir: str = None
) -> Dict[str, Any]:
    """
    Run the full agent loop.

    Processing flow:
    1. Ensure required directories exist
    2. Load raw intake file
    3. Normalize intake items
    4. Load dedupe memory
    5. Split new vs duplicate events
    6. For each new event: compute score, trigger, render notification
    7. Update dedupe memory
    8. Return run summary

    Args:
        intake_path: Path to intake JSON file
        dedupe_memory_path: Path to dedupe memory JSON file
        output_dir: Optional directory to write notification files

    Returns:
        Run summary dict
    """
    # Step 0: Ensure directories exist
    ensure_directories(intake_path, dedupe_memory_path, output_dir)

    # Step 1 & 2: Load and normalize intake
    raw_items = load_intake_file(intake_path)
    normalized_events = normalize_intake_batch(raw_items)
    
    # Step 3: Load dedupe memory
    memory = load_dedupe_memory(dedupe_memory_path)
    
    # Step 4: Split new vs duplicate
    new_events, duplicate_events = memory.split_events(normalized_events)
    
    # Step 5: Process new events
    monitor_count = 0
    full_analysis_count = 0
    processed_events = []
    
    for event in new_events:
        # Compute score and trigger
        enriched_event = process_event(event)
        processed_events.append(enriched_event)
        
        # Count outcomes
        if enriched_event['trigger_full_analysis']:
            full_analysis_count += 1
        else:
            monitor_count += 1
        
        # Render and optionally write notification
        if output_dir:
            filepath = write_notification(enriched_event, output_dir)
            enriched_event['notification_path'] = filepath
    
    # Step 6: Update dedupe memory
    memory.save()
    
    # Step 7: Return summary
    summary = {
        "intake_count": len(raw_items),
        "normalized_count": len(normalized_events),
        "new_event_count": len(new_events),
        "duplicate_event_count": len(duplicate_events),
        "monitor_count": monitor_count,
        "full_analysis_count": full_analysis_count,
        "processed_events": processed_events
    }
    
    return summary


def print_summary(summary: Dict[str, Any]):
    """Print run summary to stdout."""
    print("=" * 60)
    print("Geo Market Watch v5.5 — Agent Loop Summary")
    print("=" * 60)
    print()
    print(f"Intake items: {summary['intake_count']}")
    print(f"Normalized events: {summary['normalized_count']}")
    print()
    print(f"New events: {summary['new_event_count']}")
    print(f"Duplicate events: {summary['duplicate_event_count']}")
    print()
    print(f"Monitor outcomes: {summary['monitor_count']}")
    print(f"Full Analysis outcomes: {summary['full_analysis_count']}")
    print()
    
    if summary['processed_events']:
        print("Processed Events:")
        for event in summary['processed_events']:
            trigger_status = "→ Full Analysis" if event['trigger_full_analysis'] else "→ Monitor"
            print(f"  • {event['event_title'][:50]}... (Score: {event['score']}) {trigger_status}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    # Example usage
    import tempfile
    import json
    
    # Create sample intake file
    sample_intake = {
        "items": [
            {
                "source_name": "Reuters",
                "source_url": "https://example.com/red-sea",
                "published_at": "2024-01-12",
                "headline": "Red Sea shipping disruption",
                "region": "Middle East",
                "category": "Maritime disruption",
                "summary": "Major container lines reroute vessels.",
                "indicators": {"physical_disruption": 1, "transport_impact": 2, "policy_sanctions": 0, "market_transmission": 1, "escalation_risk": 1},
                "flags": {"confirmed_supply_disruption": False, "strategic_transport_disruption": True, "major_sanctions_escalation": False, "military_escalation": False}
            },
            {
                "source_name": "Bloomberg",
                "source_url": "https://example.com/russia-oil",
                "published_at": "2023-12-15",
                "headline": "Russia expands oil export restrictions",
                "region": "Eastern Europe",
                "category": "Energy policy",
                "summary": "Russia expands restrictions affecting energy exports.",
                "indicators": {"physical_disruption": 2, "transport_impact": 1, "policy_sanctions": 2, "market_transmission": 2, "escalation_risk": 1},
                "flags": {"confirmed_supply_disruption": True, "strategic_transport_disruption": False, "major_sanctions_escalation": True, "military_escalation": False}
            }
        ]
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        intake_path = os.path.join(tmpdir, "intake.json")
        memory_path = os.path.join(tmpdir, "memory.json")
        output_path = os.path.join(tmpdir, "outputs")
        
        with open(intake_path, 'w') as f:
            json.dump(sample_intake, f)
        
        # Run agent loop
        summary = run_agent_loop(intake_path, memory_path, output_path)
        print_summary(summary)
        
        print(f"\nOutput files written to: {output_path}")
        if os.path.exists(output_path):
            for f in os.listdir(output_path):
                print(f"  - {f}")
