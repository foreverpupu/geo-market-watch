"""
Event Search

从 repository 中找到最近可能相关的 canonical events，并排序返回。
"""

from datetime import datetime, timedelta

from v2.config import ResolutionConfig, get_time_window_for_event_type
from v2.domain.models import EventCandidate, ScoredEventMatch
from v2.repositories.event_repository import EventRepository
from v2.services.similarity import (
    combined_match_score,
    cosine_similarity,
    entity_overlap_score,
    time_window_score,
)


def find_candidate_matches(
    candidate: EventCandidate,
    repository: EventRepository,
    now: datetime,
    config: ResolutionConfig,
) -> list[ScoredEventMatch]:
    """
    为候选事件找到可能匹配的事件列表。
    
    处理流程：
    1. 根据 event_type 和 region 过滤最近事件
    2. 对每个 event 计算：embedding similarity、entity overlap、time score、total score
    3. 降序排序返回 top_k
    
    Args:
        candidate: 候选事件
        repository: 事件存储
        now: 当前时间
        config: 配置
        
    Returns:
        排序后的匹配事件列表
    """
    # 确定时间窗口
    window_days = get_time_window_for_event_type(candidate.event_type)
    since = now - timedelta(days=window_days)
    
    # 从 repository 获取候选事件
    # 优先筛选相同 region，如果没有则放宽
    candidate_events = repository.list_recent_events(
        event_type=candidate.event_type,
        region=candidate.region,
        since=since,
    )
    
    # 如果相同 region 没有结果，尝试放宽 region 限制
    if not candidate_events and candidate.region is not None:
        candidate_events = repository.list_recent_events(
            event_type=candidate.event_type,
            region=None,
            since=since,
        )
    
    # 计算分数
    scored_matches = []
    for event in candidate_events:
        # 计算各项分数
        embedding_sim = cosine_similarity(candidate.embedding, event.embedding)
        entity_overlap = entity_overlap_score(candidate.normalized_entities, event.normalized_entities)
        time_score = time_window_score(candidate.occurred_at, event.last_seen_at, window_days)
        
        # 计算综合分数
        total_score = combined_match_score(
            embedding_similarity=embedding_sim,
            entity_overlap=entity_overlap,
            time_score=time_score,
            embedding_weight=config.embedding_weight,
            entity_weight=config.entity_weight,
            time_weight=config.time_weight,
        )
        
        # 构建原因说明
        reasons = []
        if embedding_sim >= config.same_cluster_embedding_threshold:
            reasons.append(f"embedding_sim={embedding_sim:.2f}")
        if entity_overlap >= config.same_cluster_entity_overlap_threshold:
            reasons.append(f"entity_overlap={entity_overlap:.2f}")
        if time_score == 1.0:
            reasons.append("within_time_window")
        
        reason = ", ".join(reasons) if reasons else "low similarity"
        
        scored_matches.append(ScoredEventMatch(
            event=event,
            embedding_similarity=embedding_sim,
            entity_overlap_score=entity_overlap,
            time_score=time_score,
            total_score=total_score,
            reason=reason,
        ))
    
    # 按总分降序排序
    scored_matches.sort(key=lambda x: x.total_score, reverse=True)
    
    # 返回 top_k
    return scored_matches[:config.top_k_candidates]
