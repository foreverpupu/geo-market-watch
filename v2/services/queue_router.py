"""
Queue Router

按分数、事件状态、冲突情况分配队列。
"""

from v2.config import DEFAULT_RANKING_CONFIG, RankingConfig
from v2.domain.enums import ExposureDirection, QueueType, SignalClass
from v2.domain.models import CanonicalEvent, Exposure, NetExposureSummary


def assign_signal_queue(
    event: CanonicalEvent,
    signal_class: str,
    exposures: list[Exposure],
    net_exposures: list[NetExposureSummary] | None = None,
    watchlist_matches: list[dict] | None = None,
    config: RankingConfig = DEFAULT_RANKING_CONFIG,
) -> str:
    """
    为信号分配队列。
    
    路由规则：
    1. Watchlist 优先：如果 watchlist_matches 非空 → watchlist
    2. 冲突队列：如果 net_direction == "mixed" 且分数差距小 → conflict
    3. 高优先事件：如果 signal_class in {major_shock, high_priority} → triage
    4. 持续事件：如果 status == active 且非低信号 → active_event
    5. 已 resolved：如果 status in {resolved, archived} → postmortem
    6. 默认：triage
    
    Args:
        event: 规范化事件
        signal_class: 信号等级
        exposures: 暴露列表
        net_exposures: 净暴露汇总（可选）
        watchlist_matches: Watchlist 匹配（可选）
        config: 配置
        
    Returns:
        QueueType 字符串
    """
    # Rule 1: Watchlist 优先
    if watchlist_matches and len(watchlist_matches) > 0:
        return QueueType.WATCHLIST.value
    
    # Rule 2: 冲突队列
    if net_exposures:
        for net in net_exposures:
            if net.net_direction == ExposureDirection.MIXED.value:
                # 检查分数差距
                gap = abs(net.positive_score - net.negative_score)
                if gap < config.mixed_exposure_threshold:
                    return QueueType.CONFLICT.value
    
    # Rule 3: 高优先事件
    if signal_class in {SignalClass.MAJOR_SHOCK.value, SignalClass.HIGH_PRIORITY.value}:
        return QueueType.TRIAGE.value
    
    # Rule 4: 持续事件
    if event.status == "active" and signal_class != SignalClass.LOW_SIGNAL.value:
        return QueueType.ACTIVE_EVENT.value
    
    # Rule 5: 已 resolved
    if event.status in {"resolved", "archived"}:
        return QueueType.POSTMORTEM.value
    
    # Rule 6: 默认
    return QueueType.TRIAGE.value
