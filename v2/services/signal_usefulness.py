"""
Signal Usefulness Metrics

信号效用度评估。
"""

from v2.config import DEFAULT_REPLAY_CONFIG, ReplayConfig
from v2.domain.enums import EventTypeCategory, SignalUsefulnessRating
from v2.domain.models import EventTimeline, Signal, SignalUsefulnessMetrics


def classify_event_category(event_type: str) -> str:
    """
    分类事件类型。
    
    Directionality 事件：关税、制裁、出口管制等
    Volatility 事件：军事演习、基础设施 outage 等
    """
    directionality_types = {
        "tariff", "sanction", "export_control", "trade_war",
        "currency_devaluation", "interest_rate_hike",
    }
    
    volatility_types = {
        "military_strike", "military_exercise", "infrastructure_outage",
        "cyber_attack", "political_crisis", "election_uncertainty",
    }
    
    if event_type.lower() in directionality_types:
        return EventTypeCategory.DIRECTIONALITY.value
    elif event_type.lower() in volatility_types:
        return EventTypeCategory.VOLATILITY.value
    else:
        # 默认根据关键词判断
        if any(kw in event_type.lower() for kw in ["price", "tariff", "tax", "rate"]):
            return EventTypeCategory.DIRECTIONALITY.value
        return EventTypeCategory.VOLATILITY.value


def calculate_usefulness_score(
    lead_time: int | None,
    prediction_error: float | None,
    is_false_alarm: bool,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
) -> float:
    """
    计算效用度分数。
    
    评分标准：
    - Lead time 越短越好（但要有提前量）
    - Prediction error 越小越好
    - False alarm 直接 0 分
    
    Args:
        lead_time: 领先时间（分钟）
        prediction_error: 预测误差
        is_false_alarm: 是否误报
        config: 配置
        
    Returns:
        效用度分数 0-1
    """
    if is_false_alarm:
        return 0.0
    
    score = 0.5  # 基础分
    
    # Lead time 加分（理想：15-60 分钟）
    if lead_time is not None:
        if 15 <= lead_time <= 60:
            score += 0.3
        elif 5 <= lead_time < 15:
            score += 0.2
        elif 60 < lead_time <= 120:
            score += 0.1
    
    # Prediction error 减分
    if prediction_error is not None:
        if prediction_error < 0.01:  # < 1%
            score += 0.2
        elif prediction_error < 0.03:  # < 3%
            score += 0.1
        elif prediction_error > 0.10:  # > 10%
            score -= 0.2
    
    return max(0.0, min(1.0, score))


def determine_usefulness_rating(score: float) -> str:
    """
    确定效用评级。
    
    Args:
        score: 效用度分数
        
    Returns:
        评级字符串
    """
    if score >= 0.70:
        return SignalUsefulnessRating.HIGH.value
    elif score >= 0.50:
        return SignalUsefulnessRating.MEDIUM.value
    elif score >= 0.30:
        return SignalUsefulnessRating.LOW.value
    else:
        return SignalUsefulnessRating.FALSE_ALARM.value


def evaluate_signal_usefulness(
    signal: Signal,
    timeline: EventTimeline,
    lead_time: int | None,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
) -> SignalUsefulnessMetrics:
    """
    评估信号效用度。
    
    Args:
        signal: 信号
        timeline: 事件时间线
        lead_time: 领先时间
        config: 配置
        
    Returns:
        SignalUsefulnessMetrics
    """
    # 分类事件
    event_type = signal.event_id.split("_")[0] if hasattr(signal, 'event_id') else "unknown"
    event_category = classify_event_category(event_type)
    
    # 判断是否误报
    is_false_alarm = timeline.market_reaction_detected_at is None
    
    # 计算预测误差（简化版）
    prediction_error = None
    if timeline.market_move_magnitude is not None:
        # 假设信号预测了 5% 的变动
        predicted_move = 0.05
        prediction_error = abs(predicted_move - timeline.market_move_magnitude)
    
    # 计算效用度分数
    usefulness_score = calculate_usefulness_score(
        lead_time, prediction_error, is_false_alarm, config
    )
    
    # 确定评级
    usefulness_rating = determine_usefulness_rating(usefulness_score)
    
    # 波动率预警匹配（简化）
    volatility_spike_match = False
    if event_category == EventTypeCategory.VOLATILITY.value:
        # 检查是否有波动率增加
        if timeline.price_points_after:
            avg_vol_before = sum(p.volatility or 0 for p in timeline.price_points_before[-20:]) / 20
            avg_vol_after = sum(p.volatility or 0 for p in timeline.price_points_after[:20]) / 20
            volatility_spike_match = avg_vol_after > avg_vol_before * config.volatility_spike_threshold
    
    # 获取检测方法（从 timeline 的 metadata 或通过其他方式传递）
    # 这里简化处理，根据 is_false_alarm 推断
    detection_method = "neutral" if is_false_alarm else "2sigma"
    
    return SignalUsefulnessMetrics(
        signal_id=signal.signal_id if hasattr(signal, 'signal_id') else "unknown",
        usefulness_score=round(usefulness_score, 4),
        usefulness_rating=usefulness_rating,
        lead_time_minutes=lead_time,
        prediction_error=round(prediction_error, 4) if prediction_error else None,
        is_false_alarm=is_false_alarm,
        volatility_spike_match=volatility_spike_match,
        market_move=timeline.market_move_magnitude,
        signal_move=0.05,  # 假设预测
        event_category=event_category,
        detection_method=detection_method,
    )
