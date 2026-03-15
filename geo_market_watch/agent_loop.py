"""
Geo Market Watch v5.5 — Agent Loop

Runs the full 4-node processing pipeline in a single process.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from geo_market_watch.intake_normalizer import IntakeNormalizer
from geo_market_watch.dedupe_memory import DedupeMemory
from geo_market_watch.scoring_engine import ScoringEngine
from geo_market_watch.trigger_engine import TriggerEngine
from geo_market_watch.models import (
    NormalizedEvent,
    ScoreResult,
    TriggerResult,
    AgentRunSummary,
)


def load_intake_file(intake_path: str) -> List[Dict[str, Any]]:
    """Load intake items from JSON file."""
    with open(intake_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Support both {items: [...]} and [...] formats
    if isinstance(data, dict) and 'items' in data:
        return data['items']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(f"Unexpected intake format: {type(data)}")


def ensure_directories(intake_path: str, dedupe_memory_path: str, output_dir: Optional[str] = None):
    """
    Ensure all required directories exist.
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
    output_dir: Optional[str] = None,
    current_time: Optional[datetime] = None
) -> AgentRunSummary:
    """
    Run the full agent loop.

    Processing flow:
    1. Ensure required directories exist
    2. Load raw intake file
    3. Normalize intake items
    4. Load dedupe memory
    5. Check for duplicates
    6. For each new event: compute score, trigger
    7. Update dedupe memory
    8. Return run summary

    Args:
        intake_path: Path to intake JSON file
        dedupe_memory_path: Path to dedupe memory JSON file
        output_dir: Optional directory to write notification files
        current_time: Optional time reference for reproducibility

    Returns:
        AgentRunSummary with full execution details
    """
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    started_at = current_time or datetime.now()
    
    summary = AgentRunSummary(
        run_id=run_id,
        started_at=started_at
    )
    
    try:
        # Step 0: Ensure directories exist
        ensure_directories(intake_path, dedupe_memory_path, output_dir)

        # Step 1: Load intake file
        raw_items = load_intake_file(intake_path)
        summary.items_processed = len(raw_items)
        
        # Step 2: Initialize engines
        normalizer = IntakeNormalizer(current_time=started_at)
        dedupe_memory = DedupeMemory(dedupe_memory_path)
        scoring_engine = ScoringEngine()
        trigger_engine = TriggerEngine()
        
        # Step 3: Normalize events
        normalized_events: List[NormalizedEvent] = []
        for raw in raw_items:
            try:
                event = normalizer.normalize(raw)
                normalized_events.append(event)
            except Exception as e:
                summary.errors.append(f"Failed to normalize item: {e}")
        
        summary.items_normalized = len(normalized_events)
        
        # Step 4 & 5: Check duplicates and process new events
        new_events = []
        duplicate_count = 0
        
        for event in normalized_events:
            is_dup, reason = dedupe_memory.check_duplicate(event, current_time=started_at)
            if is_dup:
                duplicate_count += 1
            else:
                new_events.append(event)
        
        summary.items_deduped = duplicate_count
        
        # Step 6: Score and trigger new events
        monitor_count = 0
        full_analysis_count = 0
        
        for event in new_events:
            try:
                # Score event
                score_result = scoring_engine.compute_score(event)
                summary.items_scored += 1
                
                # Check trigger
                context = {
                    "category": event.category,
                    "severity": event.severity,
                }
                trigger_result = trigger_engine.should_escalate(score_result, context)
                
                if trigger_result.trigger_full_analysis:
                    full_analysis_count += 1
                else:
                    monitor_count += 1
                
                summary.items_triggered += 1
                
            except Exception as e:
                summary.errors.append(f"Failed to process event {event.event_id}: {e}")
        
        summary.notifications_generated = full_analysis_count
        summary.completed_at = datetime.now()
        
        return summary
        
    except Exception as e:
        summary.errors.append(f"Agent loop failed: {e}")
        summary.completed_at = datetime.now()
        return summary


def print_summary(summary: AgentRunSummary):
    """Print run summary to stdout."""
    print("=" * 60)
    print("Geo Market Watch v5.5 — Agent Loop Summary")
    print("=" * 60)
    print()
    print(f"Run ID: {summary.run_id}")
    print(f"Started: {summary.started_at}")
    if summary.completed_at:
        print(f"Completed: {summary.completed_at}")
        print(f"Duration: {summary.duration_seconds:.2f}s")
    print()
    print(f"Items processed: {summary.items_processed}")
    print(f"Items normalized: {summary.items_normalized}")
    print(f"Items deduped: {summary.items_deduped}")
    print(f"Items scored: {summary.items_scored}")
    print(f"Items triggered: {summary.items_triggered}")
    print()
    print(f"Notifications generated: {summary.notifications_generated}")
    print(f"Success: {summary.success}")
    
    if summary.errors:
        print()
        print("Errors:")
        for error in summary.errors:
            print(f"  - {error}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    # Example usage
    import tempfile
    
    # Create sample intake file
    sample_intake = {
        "items": [
            {
                "source_name": "Reuters",
                "source_url": "https://example.com/red-sea",
                "published_at": "2024-01-12",
                "headline": "Red Sea shipping disruption escalates as Houthis target more vessels",
                "region": "Middle East",
                "category": "shipping",
                "summary": "Major container lines reroute vessels.",
            },
            {
                "source_name": "Bloomberg",
                "source_url": "https://example.com/russia-oil",
                "published_at": "2023-12-15",
                "headline": "Russia expands oil export restrictions amid sanctions",
                "region": "Eastern Europe",
                "category": "energy",
                "summary": "Russia expands restrictions affecting energy exports.",
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
        
        print(f"\nOutput directory: {output_path}")
