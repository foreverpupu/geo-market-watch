"""
Unified data models for Geo Market Watch.

Replaces loose Dict[str, Any] passing with explicit, type-safe models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ScoreBand(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriggerDecision(Enum):
    MONITOR = "monitor"
    FULL_ANALYSIS = "full_analysis"


class EscalationPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class RawIntakeItem:
    """Raw input from news source or manual entry."""
    
    headline: str
    timestamp: datetime
    source: str | None = None
    summary: str | None = None
    region: str | None = None
    category: str | None = None
    urls: list[str] = field(default_factory=list)
    raw_metadata: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.headline:
            raise ValueError("headline is required")
        if not self.timestamp:
            raise ValueError("timestamp is required")


@dataclass
class NormalizedEvent:
    """Structured event after normalization."""
    
    event_id: str
    headline: str
    timestamp: datetime
    region: str
    category: str
    severity: str
    summary: str | None = None
    source: str | None = None
    urls: list[str] = field(default_factory=list)
    
    # Dedupe tracking
    canonical_key: str | None = None
    source_url_hash: str | None = None
    
    def __post_init__(self):
        if not self.event_id:
            raise ValueError("event_id is required")
        if not self.headline:
            raise ValueError("headline is required")


@dataclass
class ScoreResult:
    """Score output from scoring engine."""
    
    value: float  # 0-10
    band: ScoreBand
    breakdown: dict[str, float] = field(default_factory=dict)
    reasoning: str = ""
    
    def __post_init__(self):
        if not 0 <= self.value <= 10:
            raise ValueError(f"score must be 0-10, got {self.value}")


@dataclass
class TriggerResult:
    """Trigger decision from trigger engine."""
    
    trigger_full_analysis: bool
    trigger_reasons: list[str] = field(default_factory=list)
    trigger_class: str = ""
    escalation_priority: EscalationPriority = EscalationPriority.LOW
    
    @property
    def decision(self) -> TriggerDecision:
        return TriggerDecision.FULL_ANALYSIS if self.trigger_full_analysis else TriggerDecision.MONITOR


@dataclass
class NotificationArtifact:
    """Output artifact for analyst notification."""
    
    artifact_id: str
    event_id: str
    notification_type: str  # "monitor" or "full_analysis"
    headline: str
    content: str
    sectors: list[str] = field(default_factory=list)
    trade_ideas: list[dict[str, Any]] = field(default_factory=list)
    watchlist_items: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    output_path: str | None = None


@dataclass
class DedupeRecord:
    """Record for deduplication tracking."""
    
    canonical_key: str
    first_seen_at: datetime
    last_seen_at: datetime
    occurrence_count: int = 1
    headline_variants: list[str] = field(default_factory=list)
    source_urls: list[str] = field(default_factory=list)
    
    def add_occurrence(self, headline: str, timestamp: datetime, source_url: str | None = None):
        self.last_seen_at = timestamp
        self.occurrence_count += 1
        if headline not in self.headline_variants:
            self.headline_variants.append(headline)
        if source_url and source_url not in self.source_urls:
            self.source_urls.append(source_url)


@dataclass
class AgentRunSummary:
    """Summary of agent loop execution."""
    
    run_id: str
    started_at: datetime
    completed_at: datetime | None = None
    items_processed: int = 0
    items_normalized: int = 0
    items_deduped: int = 0
    items_scored: int = 0
    items_triggered: int = 0
    items_persisted: int = 0
    notifications_generated: int = 0
    errors: list[str] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        return len(self.errors) == 0
    
    @property
    def duration_seconds(self) -> float | None:
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
