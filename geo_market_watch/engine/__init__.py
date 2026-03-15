"""Geo Market Watch Engine - Core business logic."""

from geo_market_watch.engine.event_similarity import (
    headline_similarity,
    event_similarity_score,
    is_soft_duplicate,
)
from geo_market_watch.engine.agent_pipeline import (
    load_intake,
    normalize_events,
    dedupe_events,
    score_events,
    trigger_events,
    persist_events,
    render_notifications,
    run_pipeline,
)

__all__ = [
    # Event similarity
    "headline_similarity",
    "event_similarity_score",
    "is_soft_duplicate",
    # Pipeline steps
    "load_intake",
    "normalize_events",
    "dedupe_events",
    "score_events",
    "trigger_events",
    "persist_events",
    "render_notifications",
    "run_pipeline",
]
