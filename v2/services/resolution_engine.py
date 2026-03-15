"""
Resolution Engine

核心决策模块。
"""

from datetime import datetime
from typing import Optional
from v2.config import ResolutionConfig
from v2.domain.models import EventCandidate, CanonicalEvent, ResolutionDecision, ResolutionResult
from v2.domain.enums import ResolutionDecisionType
from v2.repositories.event_repository import EventRepository
from v2.services.event_search import find_candidate_matches
from v2.services.timeline_updater import create_new_event_from_candidate, update_existing_event_from_candidate


def _should_reject_candidate(candidate: EventCandidate, config: ResolutionConfig) -> Optional[ResolutionDecision]:
    """
    检查是否应该拒绝候选事件。
    
    拒绝条件：
    - title 太短
    - event_type 为空
    - normalized_entities 为空且 region 为空
    """
    reasons = []
    
    if len(candidate.title) < config.min_meaningful_title_length:
        reasons.append("title too short")
    
    if not candidate.event_type:
        reasons.append("event_type is empty")
    
    if not candidate.normalized_entities and not candidate.region:
        reasons.append("missing both entities and region")
    
    if reasons:
        return ResolutionDecision(
            decision_type=ResolutionDecisionType.REJECT_CANDIDATE.value,
            matched_event_id=None,
            matched_cluster_id=None,
            similarity_score=0.0,
            entity_overlap_score=0.0,
            time_score=0.0,
            reason=f"missing key fields for event resolution: {'; '.join(reasons)}"
        )
    
    return None


def resolve_candidate(
    candidate: EventCandidate,
    repository: EventRepository,
    now: datetime,
    config: ResolutionConfig,
) -> ResolutionDecision:
    """
    为候选事件做出 resolution 决策。
    
    决策规则：
    - Rule A: Reject（字段缺失）
    - Rule B: Update Existing Event（高相似度）
    - Rule C: New Event in Existing Cluster（中等相似度）
    - Rule D: New Event（无匹配）
    
    Args:
        candidate: 候选事件
        repository: 事件存储
        now: 当前时间
        config: 配置
        
    Returns:
        Resolution 决策
    """
    # Rule A: Reject
    reject_decision = _should_reject_candidate(candidate, config)
    if reject_decision:
        return reject_decision
    
    # 查找候选匹配
    matches = find_candidate_matches(candidate, repository, now, config)
    
    # 无匹配 -> Rule D: New Event
    if not matches:
        return ResolutionDecision(
            decision_type=ResolutionDecisionType.NEW_EVENT.value,
            matched_event_id=None,
            matched_cluster_id=None,
            similarity_score=0.0,
            entity_overlap_score=0.0,
            time_score=0.0,
            reason="no sufficiently similar recent event found"
        )
    
    # 取 top match
    top_match = matches[0]
    
    # Rule B: Update Existing Event
    if (top_match.embedding_similarity >= config.same_event_embedding_threshold and
        top_match.entity_overlap_score >= config.same_event_entity_overlap_threshold and
        top_match.time_score == 1.0):
        return ResolutionDecision(
            decision_type=ResolutionDecisionType.UPDATE_EVENT.value,
            matched_event_id=top_match.event.event_id,
            matched_cluster_id=top_match.event.cluster_id,
            similarity_score=top_match.embedding_similarity,
            entity_overlap_score=top_match.entity_overlap_score,
            time_score=top_match.time_score,
            reason="high semantic similarity, entity overlap, and matching time window"
        )
    
    # Rule C: New Event in Existing Cluster
    if (top_match.embedding_similarity >= config.same_cluster_embedding_threshold and
        top_match.entity_overlap_score >= config.same_cluster_entity_overlap_threshold and
        top_match.time_score == 1.0):
        return ResolutionDecision(
            decision_type=ResolutionDecisionType.NEW_EVENT_IN_EXISTING_CLUSTER.value,
            matched_event_id=top_match.event.event_id,
            matched_cluster_id=top_match.event.cluster_id,
            similarity_score=top_match.embedding_similarity,
            entity_overlap_score=top_match.entity_overlap_score,
            time_score=top_match.time_score,
            reason="related to existing cluster but distinct enough to create a new canonical event"
        )
    
    # Rule D: New Event
    return ResolutionDecision(
        decision_type=ResolutionDecisionType.NEW_EVENT.value,
        matched_event_id=None,
        matched_cluster_id=None,
        similarity_score=top_match.embedding_similarity if matches else 0.0,
        entity_overlap_score=top_match.entity_overlap_score if matches else 0.0,
        time_score=top_match.time_score if matches else 0.0,
        reason="no sufficiently similar recent event found"
    )


def apply_resolution(
    candidate: EventCandidate,
    decision: ResolutionDecision,
    repository: EventRepository,
    now: datetime,
) -> ResolutionResult:
    """
    应用 resolution 决策，创建或更新事件。
    
    Args:
        candidate: 候选事件
        decision: 决策
        repository: 事件存储
        now: 当前时间
        
    Returns:
        Resolution 结果
    """
    decision_type = decision.decision_type
    
    # Reject
    if decision_type == ResolutionDecisionType.REJECT_CANDIDATE.value:
        # 返回一个空结果，不创建事件
        dummy_event = create_new_event_from_candidate(candidate, now)
        return ResolutionResult(
            candidate=candidate,
            decision=decision,
            event=dummy_event,
            created_new_event=False,
            updated_existing_event=False,
        )
    
    # Update Existing Event
    if decision_type == ResolutionDecisionType.UPDATE_EVENT.value:
        existing_event = repository.get_event(decision.matched_event_id)
        if existing_event is None:
            raise ValueError(f"Event {decision.matched_event_id} not found")
        
        updated_event = update_existing_event_from_candidate(existing_event, candidate, now)
        repository.update_event(updated_event)
        
        return ResolutionResult(
            candidate=candidate,
            decision=decision,
            event=updated_event,
            created_new_event=False,
            updated_existing_event=True,
        )
    
    # New Event in Existing Cluster
    if decision_type == ResolutionDecisionType.NEW_EVENT_IN_EXISTING_CLUSTER.value:
        new_event = create_new_event_from_candidate(
            candidate, now, cluster_id=decision.matched_cluster_id
        )
        repository.create_event(new_event)
        
        return ResolutionResult(
            candidate=candidate,
            decision=decision,
            event=new_event,
            created_new_event=True,
            updated_existing_event=False,
        )
    
    # New Event (default)
    new_event = create_new_event_from_candidate(candidate, now)
    repository.create_event(new_event)
    
    return ResolutionResult(
        candidate=candidate,
        decision=decision,
        event=new_event,
        created_new_event=True,
        updated_existing_event=False,
    )
