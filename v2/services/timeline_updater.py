"""
Timeline Updater

负责新建事件和更新已有事件的时间线字段。
"""

import uuid
from datetime import datetime

from v2.domain.enums import EventPhase, EventStatus
from v2.domain.models import CanonicalEvent, EventCandidate


def _generate_event_id() -> str:
    """生成新的事件 ID。"""
    return f"EVT_{uuid.uuid4().hex[:12].upper()}"


def _generate_cluster_id() -> str:
    """生成新的 cluster ID。"""
    return f"CLUSTER_{uuid.uuid4().hex[:12].upper()}"


def _detect_phase_from_content(title: str, summary: str) -> str:
    """
    从标题和摘要中检测事件阶段。
    
    MVP 简单规则：
    - 含 "escalat" / "expand" / "widen" -> escalation
    - 含 "implement" / "begin" / "start" -> implementation
    - 否则 -> warning
    """
    text = (title + " " + summary).lower()
    
    if any(word in text for word in ["escalat", "expand", "widen", "intensif"]):
        return EventPhase.ESCALATION.value
    elif any(word in text for word in ["implement", "begin", "start", "launch"]):
        return EventPhase.IMPLEMENTATION.value
    else:
        return EventPhase.WARNING.value


def create_new_event_from_candidate(
    candidate: EventCandidate,
    now: datetime,
    cluster_id: str | None = None,
) -> CanonicalEvent:
    """
    从候选事件创建新的规范化事件。
    
    Args:
        candidate: 候选事件
        now: 当前时间
        cluster_id: 可选的 cluster ID，不传则生成新的
        
    Returns:
        新创建的规范化事件
    """
    event_id = _generate_event_id()
    final_cluster_id = cluster_id if cluster_id else _generate_cluster_id()
    
    # 检测 phase
    phase = _detect_phase_from_content(candidate.title, candidate.summary)
    
    return CanonicalEvent(
        event_id=event_id,
        cluster_id=final_cluster_id,
        canonical_title=candidate.title,
        event_type=candidate.event_type,
        region=candidate.region,
        country_codes=list(candidate.country_codes),
        normalized_entities=list(candidate.normalized_entities),
        first_seen_at=candidate.detected_at,
        last_seen_at=candidate.detected_at,
        occurred_at_start=candidate.occurred_at,
        occurred_at_end=candidate.occurred_at,
        status=EventStatus.DETECTED.value,
        phase=phase,
        evidence_count=1,
        embedding=candidate.embedding,
        metadata=dict(candidate.metadata),
    )


def update_existing_event_from_candidate(
    event: CanonicalEvent,
    candidate: EventCandidate,
    now: datetime,
) -> CanonicalEvent:
    """
    用候选事件更新已有事件。
    
    Args:
        event: 已有事件
        candidate: 候选事件
        now: 当前时间
        
    Returns:
        更新后的事件
    """
    # 更新 last_seen_at
    last_seen_at = max(event.last_seen_at, candidate.detected_at)
    
    # 更新 occurred_at_end（如果候选时间更晚）
    occurred_at_end = event.occurred_at_end
    if candidate.occurred_at is not None:
        if occurred_at_end is None or candidate.occurred_at > occurred_at_end:
            occurred_at_end = candidate.occurred_at
    
    # 合并 country_codes
    country_codes = list(set(event.country_codes + candidate.country_codes))
    
    # 合并 normalized_entities
    normalized_entities = list(set(event.normalized_entities + candidate.normalized_entities))
    normalized_entities.sort()
    
    # 更新 phase（如果检测到升级）
    new_phase = _detect_phase_from_content(candidate.title, candidate.summary)
    # escalation > implementation > warning
    phase_priority = {
        EventPhase.WARNING.value: 1,
        EventPhase.IMPLEMENTATION.value: 2,
        EventPhase.ESCALATION.value: 3,
    }
    phase = new_phase if phase_priority.get(new_phase, 0) > phase_priority.get(event.phase, 0) else event.phase
    
    # 更新 status
    status = EventStatus.ACTIVE.value if event.status == EventStatus.DETECTED.value else event.status
    
    return CanonicalEvent(
        event_id=event.event_id,
        cluster_id=event.cluster_id,
        canonical_title=event.canonical_title,
        event_type=event.event_type,
        region=event.region,
        country_codes=country_codes,
        normalized_entities=normalized_entities,
        first_seen_at=event.first_seen_at,
        last_seen_at=last_seen_at,
        occurred_at_start=event.occurred_at_start,
        occurred_at_end=occurred_at_end,
        status=status,
        phase=phase,
        evidence_count=event.evidence_count + 1,
        embedding=event.embedding,
        metadata=event.metadata,
    )
