"""
Signal Bucketing

把分数映射为优先级档位。
"""

from v2.config import DEFAULT_RANKING_CONFIG, RankingConfig
from v2.domain.enums import SignalClass


def classify_signal(
    score: float,
    config: RankingConfig = DEFAULT_RANKING_CONFIG,
) -> str:
    """
    根据分数分类信号等级。
    
    规则（动态配置）：
    - >= major_shock_threshold (0.80) → major_shock
    - >= high_priority_threshold (0.65) → high_priority
    - >= watchlist_upgrade_threshold (0.50) → watchlist_upgrade
    - >= monitor_threshold (0.35) → monitor
    - < monitor_threshold → low_signal
    
    Args:
        score: 信号分数
        config: 配置
        
    Returns:
        SignalClass 字符串
    """
    if score >= config.major_shock_threshold:
        return SignalClass.MAJOR_SHOCK.value
    elif score >= config.high_priority_threshold:
        return SignalClass.HIGH_PRIORITY.value
    elif score >= config.watchlist_upgrade_threshold:
        return SignalClass.WATCHLIST_UPGRADE.value
    elif score >= config.monitor_threshold:
        return SignalClass.MONITOR.value
    else:
        return SignalClass.LOW_SIGNAL.value
