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
