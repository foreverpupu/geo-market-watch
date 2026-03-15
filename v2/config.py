"""
V2 Resolution Configuration

集中管理所有阈值与默认窗口，禁止魔法数字散落。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResolutionConfig:
    """Resolution 配置类，所有阈值的唯一来源。"""
    
    # 同一事件判定阈值
    same_event_embedding_threshold: float = 0.82
    same_event_entity_overlap_threshold: float = 0.40
    
    # 同一 cluster 判定阈值
    same_cluster_embedding_threshold: float = 0.65
    same_cluster_entity_overlap_threshold: float = 0.25
    
    # 时间窗口
    default_time_window_days: int = 30
    
    # 输入验证
    min_meaningful_title_length: int = 8
    
    # 搜索参数
    top_k_candidates: int = 10
    
    # 相似度权重
    embedding_weight: float = 0.55
    entity_weight: float = 0.30
    time_weight: float = 0.15


# 默认配置实例
DEFAULT_RESOLUTION_CONFIG = ResolutionConfig()

# 事件类型特定时间窗口（天）
EVENT_TYPE_TIME_WINDOWS = {
    "shipping_disruption": 30,
    "sanction": 60,
    "export_control": 60,
    "military_strike": 14,
    "labor_strike": 21,
    "infrastructure_outage": 21,
}


def get_time_window_for_event_type(event_type: str) -> int:
    """获取特定事件类型的时间窗口。"""
    return EVENT_TYPE_TIME_WINDOWS.get(event_type, DEFAULT_RESOLUTION_CONFIG.default_time_window_days)


@dataclass(frozen=True)
class ExposureConfig:
    """Exposure 配置类。"""
    
    # 图传播参数
    max_graph_hops: int = 2
    propagation_decay_factor: float = 0.70
    min_propagated_exposure_score: float = 0.15
    graph_confidence_decay_per_hop: float = 0.75
    
    # 基础分数
    direct_exposure_base_score: float = 0.75
    template_exposure_base_score: float = 0.60
    graph_exposure_base_score: float = 0.45
    
    # 聚合参数
    aggregation_cap: float = 0.95
    
    # 图传播限制
    max_propagation_nodes_per_seed: int = 10


# 默认 exposure 配置
DEFAULT_EXPOSURE_CONFIG = ExposureConfig()


@dataclass(frozen=True)
class RankingConfig:
    """Ranking 配置类。"""
    
    # 特征权重
    severity_weight: float = 0.22
    market_relevance_weight: float = 0.20
    novelty_weight: float = 0.16
    confidence_weight: float = 0.14
    breadth_weight: float = 0.14
    urgency_weight: float = 0.14
    
    # Boost 和 Penalty
    watchlist_boost_max: float = 0.10
    analyst_interest_boost_max: float = 0.08
    duplicate_penalty: float = 0.10
    low_evidence_penalty: float = 0.15
    
    # 优先级阈值（动态配置）
    major_shock_threshold: float = 0.80
    high_priority_threshold: float = 0.65
    watchlist_upgrade_threshold: float = 0.50
    monitor_threshold: float = 0.35
    low_signal_threshold: float = 0.10
    
    # 冲突路由配置
    conflict_confidence_gap_threshold: float = 0.15
    mixed_exposure_threshold: float = 0.15
    
    # Novelty 时间衰减
    novelty_decay_hours: float = 24.0
    novelty_min_score: float = 0.20
    
    # Market Relevance 资产增强
    tradable_asset_boost: float = 1.2
    
    # 事件类型默认严重度
    event_type_severity_defaults: dict = None
    
    def __post_init__(self):
        if self.event_type_severity_defaults is None:
            object.__setattr__(
                self,
                'event_type_severity_defaults',
                {
                    "shipping_disruption": 0.70,
                    "port_closure": 0.62,
                    "sanction": 0.68,
                    "export_control": 0.66,
                    "military_strike": 0.85,
                    "labor_strike": 0.55,
                    "infrastructure_outage": 0.60,
                    "commodity_supply_shock": 0.78,
                }
            )


# 默认 ranking 配置
DEFAULT_RANKING_CONFIG = RankingConfig()


@dataclass(frozen=True)
class AnalystWorkflowConfig:
    """Analyst Workflow 配置类。"""
    
    # Triage 队列阈值
    triage_priority_threshold: float = 0.80
    
    # Watchlist 阈值
    watchlist_boost_threshold: float = 0.65
    
    # 分析师处理超时（小时）
    review_action_timeout: int = 48
    
    # 是否启用审计轨迹
    audit_trail_enabled: bool = True
    
    # 每个分析师最大 watchlist 数量
    max_watchlist_size: int = 50


# 默认 analyst workflow 配置
DEFAULT_ANALYST_WORKFLOW_CONFIG = AnalystWorkflowConfig()


@dataclass(frozen=True)
class ReplayConfig:
    """Replay 配置类。"""
    
    # 价格数据时间窗口（分钟）
    price_window_before: int = 60
    price_window_after: int = 240
    
    # 市场反应检测阈值
    market_move_threshold: float = 0.02  # 2% 价格变动
    volatility_spike_threshold: float = 1.5  # 波动率倍数
    
    # Lead time 计算参数
    max_lead_time_minutes: int = 1440  # 24小时
    
    # 信号效用评估阈值
    usefulness_threshold: float = 0.60
    false_alarm_threshold: float = 0.20
    
    # 逻辑版本
    prompt_version: str = "v1.0"
    model_config_id: str = "default"


# 默认 replay 配置
DEFAULT_REPLAY_CONFIG = ReplayConfig()
