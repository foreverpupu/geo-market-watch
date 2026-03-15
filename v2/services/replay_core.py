"""
Replay Core

信号回放核心功能。
"""

import uuid
from datetime import datetime, timedelta
from v2.config import ReplayConfig, DEFAULT_REPLAY_CONFIG
from v2.domain.models import Signal, EventTimeline, PricePoint, PricePoint
from v2.repositories.price_repository import PriceRepository, MockPriceRepository


def _generate_replay_id() -> str:
    """生成回放 ID。"""
    return f"REPLAY_{uuid.uuid4().hex[:12].upper()}"


def build_event_timeline(
    signal,
    symbols: list[str],
    price_repository: PriceRepository,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
    now: datetime | None = None,
) -> EventTimeline:
    """
    构建事件时间线。
    
    Args:
        signal: 信号
        symbols: 相关资产代码列表
        price_repository: 价格数据存储
        config: 配置
        now: 当前时间（用于模拟）
        
    Returns:
        EventTimeline
    """
    if now is None:
        now = datetime.now()
    
    # 使用信号生成时间作为基准
    signal_time = signal.generated_at if hasattr(signal, 'generated_at') else now
    
    # 计算时间窗口
    window_before = timedelta(minutes=config.price_window_before)
    window_after = timedelta(minutes=config.price_window_after)
    
    start_time = signal_time - window_before
    end_time = signal_time + window_after
    
    # 获取价格数据
    all_points_before = []
    all_points_after = []
    
    for symbol in symbols:
        points = price_repository.get_price_data(symbol, start_time, end_time)
        
        for point in points:
            if point.timestamp <= signal_time:
                all_points_before.append(point)
            else:
                all_points_after.append(point)
    
    # 排序
    all_points_before.sort(key=lambda x: x.timestamp)
    all_points_after.sort(key=lambda x: x.timestamp)
    
    # 检测市场反应
    market_reaction = _detect_market_reaction(
        all_points_before, all_points_after, config
    )
    
    return EventTimeline(
        event_id=signal.event_id if hasattr(signal, 'event_id') else "unknown",
        signal_generated_at=signal_time,
        price_points_before=all_points_before,
        price_points_after=all_points_after,
        market_reaction_detected_at=market_reaction.get("detected_at"),
        market_move_direction=market_reaction.get("direction"),
        market_move_magnitude=market_reaction.get("magnitude"),
    )


def _detect_market_reaction(
    points_before: list[PricePoint],
    points_after: list[PricePoint],
    config: ReplayConfig,
) -> dict:
    """
    检测市场反应。
    
    Returns:
        {
            "detected_at": datetime | None,
            "direction": "up" | "down" | "neutral" | None,
            "magnitude": float | None,
        }
    """
    if not points_before or not points_after:
        return {"detected_at": None, "direction": None, "magnitude": None}
    
    # 计算信号前的平均价格
    baseline_price = sum(p.price for p in points_before[-20:]) / min(len(points_before), 20)
    
    # 在信号后查找第一个显著变动
    for point in points_after:
        move = (point.price - baseline_price) / baseline_price
        
        if abs(move) >= config.market_move_threshold:
            direction = "up" if move > 0 else "down"
            return {
                "detected_at": point.timestamp,
                "direction": direction,
                "magnitude": round(abs(move), 4),
            }
    
    return {"detected_at": None, "direction": "neutral", "magnitude": 0.0}


def calculate_lead_time(
    signal,
    timeline: EventTimeline,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
) -> int | None:
    """
    计算信息领先时间（分钟）。
    
    Lead Time = T_market_move - T_signal_generated
    
    Args:
        signal: 信号
        timeline: 事件时间线
        config: 配置
        
    Returns:
        领先时间（分钟），如果市场未反应则返回 None
    """
    if timeline.market_reaction_detected_at is None:
        return None
    
    signal_time = signal.generated_at if hasattr(signal, 'generated_at') else datetime.now()
    reaction_time = timeline.market_reaction_detected_at
    
    lead_time = (reaction_time - signal_time).total_seconds() / 60
    
    # 限制最大领先时间
    if lead_time > config.max_lead_time_minutes:
        return None
    
    return int(lead_time)
