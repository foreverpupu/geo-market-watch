"""
Agent Pipeline - Discrete pipeline steps for agent loop.

Separates concerns into individual steps that can be tested
and composed independently.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from geo_market_watch.dedupe_memory import DedupeMemory
from geo_market_watch.intake_normalizer import IntakeNormalizer
from geo_market_watch.models import (
    AgentRunSummary,
    NormalizedEvent,
    ScoreResult,
    TriggerResult,
)
from geo_market_watch.scoring_engine import ScoringEngine
from geo_market_watch.trigger_engine import TriggerEngine


def load_intake(intake_path: str) -> list[dict[str, Any]]:
    """
    Load raw intake items from JSON file.
    
    Args:
        intake_path: Path to intake JSON file
        
    Returns:
        List of raw intake dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    with open(intake_path, encoding='utf-8') as f:
        data = json.load(f)
    
    # Support both {items: [...]} and [...] formats
    if isinstance(data, dict) and 'items' in data:
        return data['items']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(f"Unexpected intake format: {type(data)}")


def normalize_events(
    raw_items: list[dict[str, Any]],
    normalizer: IntakeNormalizer
) -> tuple[list[NormalizedEvent], list[str]]:
    """
    Normalize raw intake items into structured events.
    
    Args:
        raw_items: List of raw intake dictionaries
        normalizer: IntakeNormalizer instance
        
    Returns:
        Tuple of (normalized_events, errors)
    """
    normalized = []
    errors = []
    
    for raw in raw_items:
        try:
            event = normalizer.normalize(raw)
            normalized.append(event)
        except Exception as e:
            errors.append(f"Failed to normalize item: {e}")
    
    return normalized, errors


def dedupe_events(
    events: list[NormalizedEvent],
    dedupe_memory: DedupeMemory,
    current_time: datetime | None = None
) -> tuple[list[NormalizedEvent], int, list[str]]:
    """
    Filter out duplicate events.
    
    Args:
        events: List of normalized events
        dedupe_memory: DedupeMemory instance
        current_time: Optional time reference
        
    Returns:
        Tuple of (new_events, duplicate_count, reasons)
    """
    new_events = []
    duplicate_count = 0
    reasons = []
    
    for event in events:
        is_dup, reason = dedupe_memory.check_duplicate(event, current_time)
        if is_dup:
            duplicate_count += 1
            reasons.append(f"{event.event_id}: {reason}")
        else:
            new_events.append(event)
    
    return new_events, duplicate_count, reasons


def score_events(
    events: list[NormalizedEvent],
    scoring_engine: ScoringEngine
) -> list[tuple[NormalizedEvent, ScoreResult]]:
    """
    Score all events.
    
    Args:
        events: List of normalized events
        scoring_engine: ScoringEngine instance
        
    Returns:
        List of (event, score_result) tuples
    """
    scored = []
    
    for event in events:
        score_result = scoring_engine.compute_score(event)
        scored.append((event, score_result))
    
    return scored


def trigger_events(
    scored_events: list[tuple[NormalizedEvent, ScoreResult]],
    trigger_engine: TriggerEngine
) -> list[tuple[NormalizedEvent, ScoreResult, TriggerResult]]:
    """
    Evaluate triggers for scored events.
    
    Args:
        scored_events: List of (event, score_result) tuples
        trigger_engine: TriggerEngine instance
        
    Returns:
        List of (event, score_result, trigger_result) tuples
    """
    triggered = []
    
    for event, score_result in scored_events:
        context = {
            "category": event.category,
            "severity": event.severity,
        }
        trigger_result = trigger_engine.should_escalate(score_result, context)
        triggered.append((event, score_result, trigger_result))
    
    return triggered


def persist_events(
    triggered_events: list[tuple[NormalizedEvent, ScoreResult, TriggerResult]],
    dedupe_memory: DedupeMemory
) -> int:
    """
    Persist events to storage (dedupe memory already updated during dedupe step).
    
    Args:
        triggered_events: List of processed events
        dedupe_memory: DedupeMemory instance
        
    Returns:
        Number of events persisted
    """
    # Dedupe memory is already updated during check_duplicate
    # This step is a placeholder for future persistence logic
    # (e.g., database, notification queue)
    return len(triggered_events)


def render_notifications(
    triggered_events: list[tuple[NormalizedEvent, ScoreResult, TriggerResult]],
    output_dir: str | None = None
) -> list[dict[str, Any]]:
    """
    Render notification artifacts for triggered events.
    
    Args:
        triggered_events: List of (event, score, trigger) tuples
        output_dir: Optional directory to write notifications
        
    Returns:
        List of notification dictionaries
    """
    notifications = []
    
    for event, score_result, trigger_result in triggered_events:
        if not trigger_result.trigger_full_analysis:
            continue
        
        notification = {
            "event_id": event.event_id,
            "headline": event.headline,
            "region": event.region,
            "category": event.category,
            "score": score_result.value,
            "band": score_result.band.value,
            "trigger_class": trigger_result.trigger_class,
            "priority": trigger_result.escalation_priority.value,
            "reasons": trigger_result.trigger_reasons,
            "created_at": datetime.now().isoformat(),
        }
        
        # Optionally write to file
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            filename = f"notification_{event.event_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(notification, f, indent=2, ensure_ascii=False)
            
            notification["output_path"] = str(filepath)
        
        notifications.append(notification)
    
    return notifications


def run_pipeline(
    intake_path: str,
    dedupe_memory_path: str,
    output_dir: str | None = None,
    current_time: datetime | None = None
) -> AgentRunSummary:
    """
    Run the full agent pipeline.
    
    Orchestrates all pipeline steps:
    1. load_intake
    2. normalize_events
    3. dedupe_events
    4. score_events
    5. trigger_events
    6. persist_events
    7. render_notifications
    
    Args:
        intake_path: Path to intake JSON file
        dedupe_memory_path: Path to dedupe memory JSON file
        output_dir: Optional directory for notification files
        current_time: Optional time reference for reproducibility
        
    Returns:
        AgentRunSummary with execution results
    """
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    started_at = current_time or datetime.now()
    
    summary = AgentRunSummary(
        run_id=run_id,
        started_at=started_at
    )
    
    try:
        # Initialize engines
        normalizer = IntakeNormalizer(current_time=started_at)
        dedupe_memory = DedupeMemory(dedupe_memory_path)
        scoring_engine = ScoringEngine()
        trigger_engine = TriggerEngine()
        
        # Step 1: Load intake
        raw_items = load_intake(intake_path)
        summary.items_processed = len(raw_items)
        
        # Step 2: Normalize events
        normalized_events, norm_errors = normalize_events(raw_items, normalizer)
        summary.errors.extend(norm_errors)
        summary.items_normalized = len(normalized_events)
        
        # Step 3: Deduplicate events
        new_events, dup_count, dup_reasons = dedupe_events(
            normalized_events, dedupe_memory, started_at
        )
        summary.items_deduped = dup_count
        
        # Step 4: Score events
        scored_events = score_events(new_events, scoring_engine)
        summary.items_scored = len(scored_events)
        
        # Step 5: Evaluate triggers
        triggered_events = trigger_events(scored_events, trigger_engine)
        summary.items_triggered = len(triggered_events)
        
        # Step 6: Persist events
        persist_events(triggered_events, dedupe_memory)
        summary.items_persisted = len(triggered_events)
        
        # Step 7: Render notifications
        notifications = render_notifications(triggered_events, output_dir)
        summary.notifications_generated = len(notifications)
        
        summary.completed_at = datetime.now()
        return summary
        
    except Exception as e:
        summary.errors.append(f"Pipeline failed: {e}")
        summary.completed_at = datetime.now()
        return summary
