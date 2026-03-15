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


@dataclass
class ExposureTraceStep:
    """暴露追踪步骤（结构化来源）。"""
    step_type: str  # direct_rule, template, graph_propagation
    step_ref: str  # 规则ID、模板ID、图边等
    source_target: str  # 来源target
    target: str  # 当前target
    score_contribution: float  # 该步骤的分数贡献
    hop_count: int = 0  # 传播跳数（0表示直接）
    metadata: dict = field(default_factory=dict)


@dataclass
class ExposureCandidate:
    """暴露候选（内部中间对象）。"""
    target_type: str
    target_id: str
    target_name: str
    exposure_channel: str
    direction: str
    score: float
    confidence: float
    horizon: str
    source_type: str
    source_ref: str
    reasoning_trace: str
    trace_steps: list[ExposureTraceStep] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class Exposure:
    """最终暴露对象。"""
    exposure_id: str
    event_id: str
    target_type: str
    target_id: str
    target_name: str
    exposure_channel: str
    direction: str
    magnitude_score: float
    confidence_score: float
    horizon: str
    source_type: str
    source_ref: str
    reasoning_trace: str
    trace_steps: list[ExposureTraceStep] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class GraphEdge:
    """图边对象。"""
    src_id: str
    src_type: str
    relation_type: str
    dst_id: str
    dst_type: str
    weight: float
    metadata: dict = field(default_factory=dict)


@dataclass
class ExposureTemplate:
    """暴露模板。"""
    template_id: str
    event_type: str
    template_name: str
    steps: list[dict]
    metadata: dict = field(default_factory=dict)


@dataclass
class NetExposureSummary:
    """净暴露汇总。"""
    target_type: str
    target_id: str
    target_name: str
    net_direction: str  # positive, negative, mixed, uncertain
    net_score: float
    positive_score: float
    negative_score: float
    confidence: float
    contributing_sources: list[str]
    reasoning_summary: str


@dataclass
class ExposureResult:
    """Exposure 完整结果。"""
    event: CanonicalEvent
    direct_exposures: list[Exposure]
    template_exposures: list[Exposure]
    graph_exposures: list[Exposure]
    aggregated_exposures: list[Exposure]
    net_exposure_summaries: list[NetExposureSummary]


@dataclass
class RankingFeatureSet:
    """Ranking 特征集。"""
    severity_score: float
    market_relevance_score: float
    novelty_score: float
    confidence_score: float
    breadth_score: float
    urgency_score: float
    watchlist_match_score: float = 0.0
    analyst_interest_boost: float = 0.0
    duplicate_penalty: float = 0.0
    low_evidence_penalty: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class SignalScoreBreakdown:
    """信号分数拆解。"""
    base_score: float
    watchlist_boost: float
    analyst_interest_boost: float
    duplicate_penalty: float
    low_evidence_penalty: float
    final_score: float
    formula_trace: str
    feature_contributions: dict = field(default_factory=dict)
    exposure_contributions: dict = field(default_factory=dict)


@dataclass
class Signal:
    """信号对象。"""
    signal_id: str
    event_id: str
    signal_class: str
    rank_score: float
    severity_score: float
    market_relevance_score: float
    novelty_score: float
    confidence_score: float
    breadth_score: float
    urgency_score: float
    watchlist_match_score: float
    assigned_queue: str
    status: str
    summary_text: str
    reasoning_trace: str
    generated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class SignalResult:
    """Signal 完整结果。"""
    event: CanonicalEvent
    signal: Signal
    features: RankingFeatureSet
    breakdown: SignalScoreBreakdown


@dataclass
class TriageQueueItem:
    """Triage 队列项。"""
    signal_id: str
    event_id: str
    rank_score: float
    assigned_to: str | None
    added_at: datetime
    due_by: datetime
    status: str
    metadata: dict = field(default_factory=dict)


@dataclass
class ReviewAction:
    """分析师操作记录。"""
    action_id: str
    signal_id: str
    action_type: str
    action_taken_by: str
    action_timestamp: datetime
    comment: str | None = None
    # 修正覆盖字段
    exposure_override: dict | None = None
    severity_override: float | None = None
    # AI 认同度
    agreement_with_ai: bool | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class AuditTrailEntry:
    """审计轨迹条目。"""
    entry_id: str
    signal_id: str
    action_type: str
    action_taken_by: str
    timestamp: datetime
    action_detail: str
    metadata: dict = field(default_factory=dict)


@dataclass
class WatchlistEntry:
    """Watchlist 条目。"""
    signal_id: str
    added_at: datetime
    assigned_to: str
    status: str
    reason_for_watchlist: str
    metadata: dict = field(default_factory=dict)


@dataclass
class PricePoint:
    """价格数据点（模拟数据）。"""
    timestamp: datetime
    symbol: str
    price: float
    volume: int
    volatility: float | None = None  # 波动率


@dataclass
class EventTimeline:
    """事件时间线。"""
    event_id: str
    signal_generated_at: datetime
    price_points_before: list[PricePoint]
    price_points_after: list[PricePoint]
    market_reaction_detected_at: datetime | None
    market_move_direction: str | None  # "up", "down", "neutral"
    market_move_magnitude: float | None


@dataclass
class SignalUsefulnessMetrics:
    """信号效用度指标。"""
    signal_id: str
    usefulness_score: float  # 0-1
    usefulness_rating: str  # high, medium, low, false_alarm
    lead_time_minutes: int | None  # T_market_move - T_signal_generated
    prediction_error: float | None  # |predicted - actual|
    is_false_alarm: bool
    volatility_spike_match: bool  # 波动率预警是否匹配
    market_move: float | None  # 实际市场变动
    signal_move: float | None  # 信号预测变动
    event_category: str  # directionality, volatility
    detection_method: str = "2sigma"  # 2sigma, fixed_threshold, neutral


@dataclass
class ReplayResult:
    """回放结果。"""
    replay_id: str
    signal_id: str
    event_id: str
    prompt_version: str
    model_config_id: str
    timeline: EventTimeline
    metrics: SignalUsefulnessMetrics
    generated_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """评估结果汇总。"""
    total_signals: int
    high_usefulness_count: int
    medium_usefulness_count: int
    low_usefulness_count: int
    false_alarm_count: int
    avg_lead_time_minutes: float | None
    avg_prediction_error: float | None
    volatility_accuracy: float  # 波动率预警准确率
    directionality_accuracy: float  # 方向性预测准确率
