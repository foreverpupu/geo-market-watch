"""
Signal Engine

Step 3 orchestrator，统一生成 Signal。
"""

import uuid
from datetime import datetime

from v2.config import DEFAULT_RANKING_CONFIG, RankingConfig
from v2.domain.models import (
    CanonicalEvent,
    Exposure,
    NetExposureSummary,
    Signal,
    SignalResult,
)
from v2.repositories.signal_repository import SignalRepository
from v2.services.queue_router import assign_signal_queue
from v2.services.ranking_features import build_ranking_features
from v2.services.signal_bucketing import classify_signal
from v2.services.signal_explainer import build_signal_summary
from v2.services.signal_scoring import compute_signal_score


def _generate_signal_id() -> str:
    """生成信号 ID。"""
    return f"SIG_{uuid.uuid4().hex[:12].upper()}"


def generate_signal_for_event(
    event: CanonicalEvent,
    exposures: list[Exposure],
    net_exposures: list[NetExposureSummary] | None = None,
    watchlist_matches: list[dict] | None = None,
    signal_repository: SignalRepository | None = None,
    now: datetime | None = None,
    config: RankingConfig = DEFAULT_RANKING_CONFIG,
) -> SignalResult:
    """
    为事件生成信号。
    
    流程：
    1. build_ranking_features
    2. compute_signal_score
    3. classify_signal
    4. assign_signal_queue
    5. build_signal_summary
    6. 构建 Signal
    7. 保存到 repository
    
    Args:
        event: 规范化事件
        exposures: 暴露列表
        net_exposures: 净暴露汇总（可选）
        watchlist_matches: Watchlist 匹配（可选）
        signal_repository: 信号存储（可选）
        now: 当前时间
        config: 配置
        
    Returns:
        SignalResult
    """
    if now is None:
        now = datetime.now()
    
    # Step 1: Build ranking features
    features = build_ranking_features(
        event=event,
        exposures=exposures,
        net_exposures=net_exposures,
        watchlist_matches=watchlist_matches,
        now=now,
        config=config,
    )
    
    # Step 2: Compute signal score
    breakdown = compute_signal_score(features, config)
    
    # Step 3: Classify signal
    signal_class = classify_signal(breakdown.final_score, config)
    
    # Step 4: Assign queue
    queue = assign_signal_queue(
        event=event,
        signal_class=signal_class,
        exposures=exposures,
        net_exposures=net_exposures,
        watchlist_matches=watchlist_matches,
        config=config,
    )
    
    # Step 5: Build summary
    top_exposures = sorted(exposures, key=lambda x: x.magnitude_score, reverse=True)[:3]
    summary_text, reasoning_trace = build_signal_summary(
        event=event,
        features=features,
        breakdown=breakdown,
        signal_class=signal_class,
        top_exposures=top_exposures,
    )
    
    # Step 6: Build Signal
    signal = Signal(
        signal_id=_generate_signal_id(),
        event_id=event.event_id,
        signal_class=signal_class,
        rank_score=breakdown.final_score,
        severity_score=features.severity_score,
        market_relevance_score=features.market_relevance_score,
        novelty_score=features.novelty_score,
        confidence_score=features.confidence_score,
        breadth_score=features.breadth_score,
        urgency_score=features.urgency_score,
        watchlist_match_score=features.watchlist_match_score,
        assigned_queue=queue,
        status="generated",
        summary_text=summary_text,
        reasoning_trace=reasoning_trace,
        generated_at=now,
        metadata={
            "formula_trace": breakdown.formula_trace,
            "feature_contributions": breakdown.feature_contributions,
        },
    )
    
    # Step 7: Save to repository
    if signal_repository:
        signal_repository.save_signal(signal)
    
    return SignalResult(
        event=event,
        signal=signal,
        features=features,
        breakdown=breakdown,
    )
