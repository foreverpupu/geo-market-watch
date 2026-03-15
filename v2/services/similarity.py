"""
Similarity Scoring

实现三类分数：cosine similarity、entity overlap、time window score。
"""

import math
from datetime import datetime, timedelta
from typing import Optional


def cosine_similarity(vec_a: Optional[list[float]], vec_b: Optional[list[float]]) -> float:
    """
    计算两个向量的余弦相似度。
    
    Args:
        vec_a: 向量 A
        vec_b: 向量 B
        
    Returns:
        相似度分数 [0.0, 1.0]
        
    Raises:
        ValueError: 向量长度不一致
    """
    # 任一向量为空时返回 0.0
    if vec_a is None or vec_b is None:
        return 0.0
    
    # 长度不一致时抛错
    if len(vec_a) != len(vec_b):
        raise ValueError(f"Vector length mismatch: {len(vec_a)} vs {len(vec_b)}")
    
    # 计算点积和模长
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    
    # 避免除零
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    
    # 计算余弦相似度
    similarity = dot_product / (norm_a * norm_b)
    
    # 负值截到 0.0
    return max(0.0, similarity)


def entity_overlap_score(a: list[str], b: list[str]) -> float:
    """
    计算实体重叠分数（Jaccard 系数）。
    
    Args:
        a: 实体列表 A
        b: 实体列表 B
        
    Returns:
        Jaccard 相似度 [0.0, 1.0]
    """
    # 两边都空时返回 0.0
    if not a and not b:
        return 0.0
    
    # 转为集合
    set_a = set(a)
    set_b = set(b)
    
    # 计算交集和并集
    intersection = set_a & set_b
    union = set_a | set_b
    
    # Jaccard = |交集| / |并集|
    return len(intersection) / len(union) if union else 0.0


def time_window_score(
    candidate_time: Optional[datetime],
    event_last_seen: datetime,
    window_days: int,
) -> float:
    """
    计算时间窗口匹配分数。
    
    Args:
        candidate_time: 候选事件时间
        event_last_seen: 事件最后出现时间
        window_days: 窗口天数
        
    Returns:
        1.0 如果在窗口内，0.0 如果超出窗口
    """
    # candidate_time 为空时退化成 1.0
    if candidate_time is None:
        return 1.0
    
    # 计算时间差
    time_diff = abs((candidate_time - event_last_seen).total_seconds())
    window_seconds = timedelta(days=window_days).total_seconds()
    
    # 在窗口内返回 1.0，否则 0.0
    return 1.0 if time_diff <= window_seconds else 0.0


def combined_match_score(
    embedding_similarity: float,
    entity_overlap: float,
    time_score: float,
    embedding_weight: float = 0.55,
    entity_weight: float = 0.30,
    time_weight: float = 0.15,
) -> float:
    """
    计算综合匹配分数。
    
    默认权重：
    - embedding: 0.55
    - entity: 0.30
    - time: 0.15
    
    Args:
        embedding_similarity: 嵌入相似度
        entity_overlap: 实体重叠分数
        time_score: 时间窗口分数
        embedding_weight: embedding 权重
        entity_weight: entity 权重
        time_weight: time 权重
        
    Returns:
        综合分数 [0.0, 1.0]
    """
    return (
        embedding_weight * embedding_similarity +
        entity_weight * entity_overlap +
        time_weight * time_score
    )
