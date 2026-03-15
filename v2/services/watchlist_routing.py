"""
Watchlist Routing

信号路由到分析师 Watchlist。
"""

from datetime import datetime
from v2.config import AnalystWorkflowConfig, DEFAULT_ANALYST_WORKFLOW_CONFIG
from v2.domain.models import Signal, WatchlistEntry
from v2.domain.enums import WatchlistStatus
from v2.repositories.watchlist_repository import WatchlistRepository, InMemoryWatchlistRepository


def route_signal_to_watchlist(
    signal: Signal,
    analyst_id: str,
    reason: str,
    config: AnalystWorkflowConfig = DEFAULT_ANALYST_WORKFLOW_CONFIG,
    watchlist_repository: WatchlistRepository | None = None,
    now: datetime | None = None,
) -> WatchlistEntry | None:
    """
    将信号路由到分析师 Watchlist。
    
    如果信号分数大于 watchlist_boost_threshold，则添加到 Watchlist。
    
    Args:
        signal: 信号
        analyst_id: 分析师 ID
        reason: 添加原因
        config: 配置
        watchlist_repository: Watchlist 存储（可选）
        now: 当前时间
        
    Returns:
        WatchlistEntry（如果满足阈值）
    """
    if now is None:
        now = datetime.now()
    
    # 检查阈值
    if signal.rank_score < config.watchlist_boost_threshold:
        return None
    
    # 检查 watchlist 大小限制
    if watchlist_repository:
        current_count = watchlist_repository.count(assigned_to=analyst_id)
        if current_count >= config.max_watchlist_size:
            raise ValueError(f"Watchlist size limit reached for analyst {analyst_id}")
    
    entry = WatchlistEntry(
        signal_id=signal.signal_id,
        added_at=now,
        assigned_to=analyst_id,
        status=WatchlistStatus.ACTIVE.value,
        reason_for_watchlist=reason,
    )
    
    if watchlist_repository:
        watchlist_repository.add_entry(entry)
    
    return entry


def auto_route_high_priority_signals(
    signal: Signal,
    analyst_ids: list[str],
    config: AnalystWorkflowConfig = DEFAULT_ANALYST_WORKFLOW_CONFIG,
    watchlist_repository: WatchlistRepository | None = None,
    now: datetime | None = None,
) -> list[WatchlistEntry]:
    """
    自动路由高优先级信号到多个分析师。
    
    Args:
        signal: 信号
        analyst_ids: 分析师 ID 列表
        config: 配置
        watchlist_repository: Watchlist 存储（可选）
        now: 当前时间
        
    Returns:
        创建的 WatchlistEntry 列表
    """
    entries = []
    
    for analyst_id in analyst_ids:
        try:
            entry = route_signal_to_watchlist(
                signal=signal,
                analyst_id=analyst_id,
                reason=f"Auto-routed: high priority signal ({signal.signal_class})",
                config=config,
                watchlist_repository=watchlist_repository,
                now=now,
            )
            if entry:
                entries.append(entry)
        except ValueError:
            # Watchlist 已满，跳过
            pass
    
    return entries
