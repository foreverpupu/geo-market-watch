"""
Replay Core (Optimized)

信号回放核心功能 - 优化版本。

优化点：
1. 2-Sigma 冷启动处理（数据不足时使用固定百分比阈值）
2. 动态观察窗口（只使用信号发出前的数据）
3. 虚假信号检测（24小时无反应标记为 Neutral）
4. Pandas rolling 提升计算效率
"""

import uuid
from datetime import datetime, timedelta

import pandas as pd

from v2.config import DEFAULT_REPLAY_CONFIG, ReplayConfig
from v2.domain.models import EventTimeline, Signal
from v2.repositories.price_repository import PriceRepository


def _generate_replay_id() -> str:
    """生成回放 ID。"""
    return f"REPLAY_{uuid.uuid4().hex[:12].upper()}"


def _detect_market_move_optimized(
    price_series: pd.Series,
    timestamp_series: pd.Series,
    signal_time: datetime,
    price_at_signal: float,
    config: ReplayConfig,
) -> dict:
    """
    优化版市场反应检测。
    
    优化点：
    - 使用 Pandas rolling 计算标准差
    - 动态观察窗口（只使用信号前数据）
    - 冷启动处理（数据不足时使用固定阈值）
    
    Args:
        price_series: 价格序列
        timestamp_series: 时间戳序列
        signal_time: 信号时间
        price_at_signal: 信号时价格
        config: 配置
        
    Returns:
        {
            "detected_at": datetime | None,
            "direction": "up" | "down" | "neutral" | None,
            "magnitude": float | None,
            "method": "2sigma" | "fixed_threshold" | "neutral",
        }
    """
    # 分离信号前后的数据
    mask_before = timestamp_series < signal_time
    mask_after = timestamp_series >= signal_time
    
    prices_before = price_series[mask_before]
    prices_after = price_series[mask_after]
    timestamps_after = timestamp_series[mask_after]
    
    if len(prices_before) == 0 or len(prices_after) == 0:
        return {"detected_at": None, "direction": None, "magnitude": None, "method": "neutral"}
    
    # 检查 24 小时内是否有反应（虚假信号检测）
    max_check_time = signal_time + timedelta(hours=24)
    mask_24h = timestamps_after <= max_check_time
    prices_24h = prices_after[mask_24h]
    
    if len(prices_24h) == 0:
        return {"detected_at": None, "direction": "neutral", "magnitude": 0.0, "method": "neutral"}
    
    # 冷启动处理：数据不足时使用固定百分比阈值
    window_size = config.price_window_before  # 默认 60 分钟
    
    if len(prices_before) < window_size:
        # 使用固定百分比阈值（如 1%）
        fixed_threshold = price_at_signal * config.market_move_threshold
        
        for i, (price, ts) in enumerate(zip(prices_after, timestamps_after)):
            if ts > max_check_time:
                break
            
            move = abs(price - price_at_signal)
            if move >= fixed_threshold:
                direction = "up" if price > price_at_signal else "down"
                return {
                    "detected_at": ts,
                    "direction": direction,
                    "magnitude": round(move / price_at_signal, 4),
                    "method": "fixed_threshold",
                }
        
        # 24 小时内无反应 -> 虚假信号
        return {"detected_at": None, "direction": "neutral", "magnitude": 0.0, "method": "neutral"}
    
    # 正常情况：使用 Pandas rolling 计算 2-Sigma
    # 只使用信号前的数据计算滚动统计
    rolling_mean = prices_before.rolling(window=window_size, min_periods=10).mean()
    rolling_std = prices_before.rolling(window=window_size, min_periods=10).std()
    
    # 获取信号时的基准值
    baseline_mean = rolling_mean.iloc[-1]
    baseline_std = rolling_std.iloc[-1]
    
    if pd.isna(baseline_mean) or pd.isna(baseline_std):
        # 滚动计算失败，回退到固定阈值
        fixed_threshold = price_at_signal * config.market_move_threshold
        
        for i, (price, ts) in enumerate(zip(prices_after, timestamps_after)):
            if ts > max_check_time:
                break
            
            move = abs(price - price_at_signal)
            if move >= fixed_threshold:
                direction = "up" if price > price_at_signal else "down"
                return {
                    "detected_at": ts,
                    "direction": direction,
                    "magnitude": round(move / price_at_signal, 4),
                    "method": "fixed_threshold",
                }
        
        return {"detected_at": None, "direction": "neutral", "magnitude": 0.0, "method": "neutral"}
    
    # 2-Sigma 阈值
    upper_bound = baseline_mean + 2 * baseline_std
    lower_bound = baseline_mean - 2 * baseline_std
    
    # 检测突破
    for i, (price, ts) in enumerate(zip(prices_after, timestamps_after)):
        if ts > max_check_time:
            break
        
        if price >= upper_bound:
            return {
                "detected_at": ts,
                "direction": "up",
                "magnitude": round((price - price_at_signal) / price_at_signal, 4),
                "method": "2sigma",
            }
        elif price <= lower_bound:
            return {
                "detected_at": ts,
                "direction": "down",
                "magnitude": round((price_at_signal - price) / price_at_signal, 4),
                "method": "2sigma",
            }
    
    # 24 小时内无突破 -> 虚假信号
    return {"detected_at": None, "direction": "neutral", "magnitude": 0.0, "method": "neutral"}


def build_event_timeline_optimized(
    signal: Signal,
    symbols: list[str],
    price_repository: PriceRepository,
    config: ReplayConfig = DEFAULT_REPLAY_CONFIG,
    now: datetime | None = None,
) -> EventTimeline:
    """
    优化版事件时间线构建。
    
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
    
    # 转换为 Pandas Series 进行优化计算
    if all_points_before and all_points_after:
        timestamps = pd.Series([p.timestamp for p in all_points_before + all_points_after])
        prices = pd.Series([p.price for p in all_points_before + all_points_after])
        
        # 获取信号时的价格
        price_at_signal = all_points_before[-1].price if all_points_before else all_points_after[0].price
        
        # 检测市场反应
        market_reaction = _detect_market_move_optimized(
            prices, timestamps, signal_time, price_at_signal, config
        )
    else:
        market_reaction = {
            "detected_at": None,
            "direction": None,
            "magnitude": None,
            "method": "neutral",
        }
    
    return EventTimeline(
        event_id=signal.event_id if hasattr(signal, 'event_id') else "unknown",
        signal_generated_at=signal_time,
        price_points_before=all_points_before,
        price_points_after=all_points_after,
        market_reaction_detected_at=market_reaction.get("detected_at"),
        market_move_direction=market_reaction.get("direction"),
        market_move_magnitude=market_reaction.get("magnitude"),
    )


def calculate_lead_time(
    signal: Signal,
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
