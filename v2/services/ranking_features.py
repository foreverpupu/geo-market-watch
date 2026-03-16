"""
Ranking Features

从 CanonicalEvent + Exposures 提取 ranking 所需特征。
"""

from datetime import datetime

from v2.config import DEFAULT_RANKING_CONFIG, RankingConfig
from v2.domain.enums import EventPhase, EventStatus, ExposureTargetType
from v2.domain.models import CanonicalEvent, Exposure, NetExposureSummary, RankingFeatureSet


def _get_severity_score(event: CanonicalEvent, config: RankingConfig) -> float:
    """
    计算严重度分数。
    
    优先使用 event.metadata["severity_score"]，否则按 event_type 给默认值。
    """
    # 优先使用已有 severity_score
    if "severity_score" in event.metadata:
        return float(event.metadata["severity_score"])
    
    # 按 event_type 给默认值
    return config.event_type_severity_defaults.get(event.event_type, 0.60)


def _get_market_relevance_score(
    exposures: list[Exposure],
    config: RankingConfig,
) -> float:
    """
    计算市场相关度分数。
    
    公式：0.5 * max_exposure_score + 0.3 * top3_avg + 0.2 * tradable_ratio
    
    对 ETF/ASSET/COMMODITY 等可交易资产增强。
    """
    if not exposures:
        return 0.0
    
    # 提取分数
    scores = [e.magnitude_score for e in exposures]
    max_score = max(scores)
    
    # Top 3 平均
    top3_scores = sorted(scores, reverse=True)[:3]
    top3_avg = sum(top3_scores) / len(top3_scores) if top3_scores else 0.0
    
    # 可交易资产比例
    tradable_types = {
        ExposureTargetType.ETF.value,
        ExposureTargetType.ASSET.value,
        ExposureTargetType.COMMODITY.value,
        ExposureTargetType.SECTOR.value,
    }
    tradable_count = sum(1 for e in exposures if e.target_type in tradable_types)
    tradable_ratio = tradable_count / len(exposures)
    
    # 基础分数
    base_score = 0.5 * max_score + 0.3 * top3_avg + 0.2 * tradable_ratio
    
    # 可交易资产增强
    if tradable_count > 0:
        base_score = min(1.0, base_score * config.tradable_asset_boost)
    
    return round(base_score, 4)


def _get_novelty_score(
    event: CanonicalEvent,
    now: datetime,
    config: RankingConfig,
) -> float:
    """
    计算新颖度分数（带时间衰减）。
    
    基于 evidence_count 和 first_seen_at / last_seen_at。
    """
    # 基础分数
    if event.evidence_count == 1:
        base_score = 0.85
    elif event.evidence_count <= 3:
        base_score = 0.75
    elif event.evidence_count <= 6:
        base_score = 0.55
    else:
        base_score = 0.35
    
    # 时间衰减
    hours_since_first = (now - event.first_seen_at).total_seconds() / 3600
    decay_factor = max(
        config.novelty_min_score,
        1.0 - (hours_since_first / config.novelty_decay_hours)
    )
    
    # 应用衰减
    novelty_score = base_score * decay_factor
    
    return round(novelty_score, 4)


def _get_confidence_score(
    event: CanonicalEvent,
    exposures: list[Exposure],
) -> float:
    """
    计算置信度分数。
    
    公式：0.6 * event_level + 0.4 * avg_top_exposure_confidence
    """
    # Event level confidence
    if "confidence_score" in event.metadata:
        event_conf = float(event.metadata["confidence_score"])
    else:
        # 基于 evidence_count
        if event.evidence_count >= 4:
            event_conf = 0.78
        elif event.evidence_count >= 2:
            event_conf = 0.65
        else:
            event_conf = 0.50
    
    # Top exposure confidence
    if exposures:
        top_confidences = sorted([e.confidence_score for e in exposures], reverse=True)[:3]
        exposure_conf = sum(top_confidences) / len(top_confidences)
    else:
        exposure_conf = 0.50
    
    confidence = 0.6 * event_conf + 0.4 * exposure_conf
    return round(confidence, 4)


def _get_breadth_score(exposures: list[Exposure]) -> float:
    """
    计算广度分数。
    
    公式：0.5 * min(unique_targets / 8, 1.0) + 0.3 * min(unique_types / 4, 1.0) + 0.2 * multi_region
    """
    if not exposures:
        return 0.0
    
    # Unique targets
    unique_targets = len(set(e.target_id for e in exposures))
    target_ratio = min(unique_targets / 8.0, 1.0)
    
    # Unique target types
    unique_types = len(set(e.target_type for e in exposures))
    type_ratio = min(unique_types / 4.0, 1.0)
    
    # Multi-region indicator (simplified)
    multi_region = 1.0 if unique_targets >= 3 else 0.0
    
    breadth = 0.5 * target_ratio + 0.3 * type_ratio + 0.2 * multi_region
    return round(breadth, 4)


def _get_urgency_score(
    event: CanonicalEvent,
    now: datetime,
) -> float:
    """
    计算紧急度分数。
    
    基于 phase、status、freshness、event_type。
    """
    # Phase component
    phase_scores = {
        EventPhase.ESCALATION.value: 0.20,
        EventPhase.IMPLEMENTATION.value: 0.12,
        EventPhase.WARNING.value: 0.05,
    }
    phase_component = phase_scores.get(event.phase, 0.0)
    
    # Freshness component
    hours_since_last = (now - event.last_seen_at).total_seconds() / 3600
    if hours_since_last < 1:
        freshness = 0.15
    elif hours_since_last < 6:
        freshness = 0.10
    elif hours_since_last < 24:
        freshness = 0.05
    else:
        freshness = 0.0
    
    # Event type component
    urgent_types = {"military_strike", "infrastructure_outage", "shipping_disruption"}
    type_component = 0.10 if event.event_type in urgent_types else 0.0
    
    # Status component
    status_component = 0.05 if event.status == EventStatus.ACTIVE.value else 0.0
    
    urgency = min(1.0, phase_component + freshness + type_component + status_component + 0.50)
    return round(urgency, 4)


def _get_penalties(
    event: CanonicalEvent,
    config: RankingConfig,
) -> tuple[float, float]:
    """
    计算 penalties。
    
    Returns: (duplicate_penalty, low_evidence_penalty)
    """
    duplicate_penalty = 0.0
    low_evidence_penalty = 0.0
    
    # Duplicate penalty
    if event.metadata.get("is_duplicate_heavy", False):
        duplicate_penalty = config.duplicate_penalty
    elif event.metadata.get("duplicate_like_update_count", 0) > 5:
        duplicate_penalty = config.duplicate_penalty * 0.5
    
    # Low evidence penalty
    if event.evidence_count == 1:
        low_evidence_penalty = config.low_evidence_penalty
    
    return duplicate_penalty, low_evidence_penalty


def build_ranking_features(
    event: CanonicalEvent,
    exposures: list[Exposure],
    net_exposures: list[NetExposureSummary] | None = None,
    watchlist_matches: list[dict] | None = None,
    now: datetime | None = None,
    config: RankingConfig = DEFAULT_RANKING_CONFIG,
) -> RankingFeatureSet:
    """
    构建 Ranking 特征集。
    
    Args:
        event: 规范化事件
        exposures: 暴露列表
        net_exposures: 净暴露汇总（可选）
        watchlist_matches: Watchlist 匹配（可选）
        now: 当前时间
        config: 配置
        
    Returns:
        RankingFeatureSet
    """
    if now is None:
        now = datetime.now()
    
    # 计算各项特征
    severity = _get_severity_score(event, config)
    market_relevance = _get_market_relevance_score(exposures, config)
    novelty = _get_novelty_score(event, now, config)
    confidence = _get_confidence_score(event, exposures)
    breadth = _get_breadth_score(exposures)
    urgency = _get_urgency_score(event, now)
    
    # Watchlist match
    watchlist_match = 0.0
    if watchlist_matches:
        watchlist_match = min(1.0, sum(m.get("weight", 0.0) for m in watchlist_matches))
    
    # Penalties
    duplicate_penalty, low_evidence_penalty = _get_penalties(event, config)
    
    return RankingFeatureSet(
        severity_score=severity,
        market_relevance_score=market_relevance,
        novelty_score=novelty,
        confidence_score=confidence,
        breadth_score=breadth,
        urgency_score=urgency,
        watchlist_match_score=watchlist_match,
        duplicate_penalty=duplicate_penalty,
        low_evidence_penalty=low_evidence_penalty,
    )
