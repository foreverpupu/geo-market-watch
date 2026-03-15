"""
V2 Domain Models

定义 dataclass 模型。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class EventCandidate:
    """事件候选对象。"""
    candidate_id: str
    source_id: str
    title: str
    summary: str
    event_type: str
    region: Optional[str]
    country_codes: list[str]
    entity_names: list[str]
    normalized_entities: list[str]
    occurred_at: Optional[datetime]
    detected_at: datetime
    embedding: Optional[list[float]] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class CanonicalEvent:
    """规范化事件对象。"""
    event_id: str
    cluster_id: str
    canonical_title: str
    event_type: str
    region: Optional[str]
    country_codes: list[str]
    normalized_entities: list[str]
    first_seen_at: datetime
    last_seen_at: datetime
    occurred_at_start: Optional[datetime]
    occurred_at_end: Optional[datetime]
    status: str
    phase: str
    evidence_count: int
    embedding: Optional[list[float]] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ScoredEventMatch:
    """带分数的事件匹配结果。"""
    event: CanonicalEvent
    embedding_similarity: float
    entity_overlap_score: float
    time_score: float
    total_score: float
    reason: str


@dataclass
class ResolutionDecision:
    """Resolution 决策结果。"""
    decision_type: str
    matched_event_id: Optional[str]
    matched_cluster_id: Optional[str]
    similarity_score: float
    entity_overlap_score: float
    time_score: float
    reason: str


@dataclass
class ResolutionResult:
    """Resolution 完整结果。"""
    candidate: EventCandidate
    decision: ResolutionDecision
    event: CanonicalEvent
    created_new_event: bool
    updated_existing_event: bool
