"""
Signal Explainer

生成人类可读的评分解释文本。
"""

from v2.domain.models import CanonicalEvent, Exposure, RankingFeatureSet, SignalScoreBreakdown


def _get_top_features(features: RankingFeatureSet) -> list[tuple[str, float]]:
    """获取最高的 2-3 个特征。"""
    feature_scores = [
        ("severity", features.severity_score),
        ("market_relevance", features.market_relevance_score),
        ("novelty", features.novelty_score),
        ("confidence", features.confidence_score),
        ("breadth", features.breadth_score),
        ("urgency", features.urgency_score),
    ]
    
    # 排序并取前 3
    feature_scores.sort(key=lambda x: x[1], reverse=True)
    return feature_scores[:3]


def _get_top_exposures(exposures: list[Exposure], n: int = 3) -> list[Exposure]:
    """获取分数最高的 n 个暴露。"""
    sorted_exposures = sorted(exposures, key=lambda x: x.magnitude_score, reverse=True)
    return sorted_exposures[:n]


def _format_exposure_for_summary(exposure: Exposure) -> str:
    """格式化暴露为简洁文本。"""
    return f"{exposure.target_id.replace('_', ' ').title()}"


def build_signal_summary(
    event: CanonicalEvent,
    features: RankingFeatureSet,
    breakdown: SignalScoreBreakdown,
    signal_class: str,
    top_exposures: list[Exposure],
) -> tuple[str, str]:
    """
    构建信号摘要和推理轨迹。
    
    Args:
        event: 规范化事件
        features: 特征集
        breakdown: 分数拆解
        signal_class: 信号等级
        top_exposures: 最重要的暴露
        
    Returns:
        (summary_text, reasoning_trace)
    """
    # 获取关键实体名称（用于人话描述）
    key_entities = []
    for exp in top_exposures[:2]:
        entity_name = exp.target_id.replace('_', ' ').title()
        key_entities.append(entity_name)
    
    # 如果没有暴露，使用事件标题中的关键词
    if not key_entities and event.normalized_entities:
        key_entities = [e.title() for e in event.normalized_entities[:2]]
    
    entity_str = " and ".join(key_entities) if key_entities else "key areas"
    
    # 生成简洁摘要
    urgency_desc = ""
    if features.urgency_score > 0.75:
        urgency_desc = " with high urgency"
    elif features.urgency_score > 0.60:
        urgency_desc = " with moderate urgency"
    
    breadth_desc = ""
    if features.breadth_score > 0.60:
        breadth_desc = " and broad exposure"
    elif features.breadth_score > 0.40:
        breadth_desc = " and notable exposure"
    
    # Summary text（人话版本）
    summary_text = (
        f"{event.canonical_title} affecting {entity_str}{urgency_desc}{breadth_desc}, "
        f"driving a {signal_class.replace('_', ' ')} signal."
    )
    
    # Reasoning trace（技术细节）
    top_features = _get_top_features(features)
    feature_str = ", ".join([f"{name}={score:.2f}" for name, score in top_features])
    
    exposure_details = []
    for exp in top_exposures[:3]:
        exposure_details.append(
            f"{exp.target_type}:{exp.target_id} ({exp.magnitude_score:.2f}, {exp.direction})"
        )
    exposure_str = "; ".join(exposure_details)
    
    reasoning_trace = (
        f"Ranked {signal_class} due to {feature_str}.\n"
        f"Top exposures: {exposure_str}.\n"
        f"Formula: {breakdown.formula_trace}"
    )
    
    return summary_text, reasoning_trace
