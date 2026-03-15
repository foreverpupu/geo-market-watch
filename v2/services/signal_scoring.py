"""
Signal Scoring

实现线性打分公式。
"""

from v2.config import RankingConfig, DEFAULT_RANKING_CONFIG
from v2.domain.models import RankingFeatureSet, SignalScoreBreakdown


def compute_signal_score(
    features: RankingFeatureSet,
    config: RankingConfig = DEFAULT_RANKING_CONFIG,
) -> SignalScoreBreakdown:
    """
    计算信号分数。
    
    Base Score 公式：
    base = severity_weight * severity
         + market_relevance_weight * market_relevance
         + novelty_weight * novelty
         + confidence_weight * confidence
         + breadth_weight * breadth
         + urgency_weight * urgency
    
    Boosts:
    - watchlist_boost = min(watchlist_boost_max, watchlist_match * watchlist_boost_max)
    - analyst_interest_boost = min(analyst_interest_boost_max, analyst_interest_boost)
    
    Penalties:
    - duplicate_penalty
    - low_evidence_penalty
    
    Final Score = base + boosts - penalties (clamped to [0, 1])
    
    Args:
        features: 特征集
        config: 配置
        
    Returns:
        SignalScoreBreakdown
    """
    # 计算 base score
    base_score = (
        config.severity_weight * features.severity_score +
        config.market_relevance_weight * features.market_relevance_score +
        config.novelty_weight * features.novelty_score +
        config.confidence_weight * features.confidence_score +
        config.breadth_weight * features.breadth_score +
        config.urgency_weight * features.urgency_score
    )
    
    # 计算 boosts
    watchlist_boost = min(
        config.watchlist_boost_max,
        features.watchlist_match_score * config.watchlist_boost_max
    )
    analyst_boost = min(
        config.analyst_interest_boost_max,
        features.analyst_interest_boost
    )
    
    # 计算 final score
    final_score = (
        base_score +
        watchlist_boost +
        analyst_boost -
        features.duplicate_penalty -
        features.low_evidence_penalty
    )
    
    # Clamp to [0, 1]
    final_score = max(0.0, min(1.0, final_score))
    
    # 构建 formula trace
    formula_trace = (
        f"base={base_score:.2f}="
        f"{config.severity_weight}*{features.severity_score:.2f}+"
        f"{config.market_relevance_weight}*{features.market_relevance_score:.2f}+"
        f"{config.novelty_weight}*{features.novelty_score:.2f}+"
        f"{config.confidence_weight}*{features.confidence_score:.2f}+"
        f"{config.breadth_weight}*{features.breadth_score:.2f}+"
        f"{config.urgency_weight}*{features.urgency_score:.2f}\n"
        f"+ watchlist_boost={watchlist_boost:.2f}\n"
        f"+ analyst_boost={analyst_boost:.2f}\n"
        f"- duplicate_penalty={features.duplicate_penalty:.2f}\n"
        f"- low_evidence_penalty={features.low_evidence_penalty:.2f}\n"
        f"=> final={final_score:.2f}"
    )
    
    # 特征贡献
    feature_contributions = {
        "severity": config.severity_weight * features.severity_score,
        "market_relevance": config.market_relevance_weight * features.market_relevance_score,
        "novelty": config.novelty_weight * features.novelty_score,
        "confidence": config.confidence_weight * features.confidence_score,
        "breadth": config.breadth_weight * features.breadth_score,
        "urgency": config.urgency_weight * features.urgency_score,
    }
    
    return SignalScoreBreakdown(
        base_score=round(base_score, 4),
        watchlist_boost=round(watchlist_boost, 4),
        analyst_interest_boost=round(analyst_boost, 4),
        duplicate_penalty=features.duplicate_penalty,
        low_evidence_penalty=features.low_evidence_penalty,
        final_score=round(final_score, 4),
        formula_trace=formula_trace,
        feature_contributions=feature_contributions,
    )
