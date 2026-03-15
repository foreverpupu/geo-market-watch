"""
Review Actions

分析师操作记录和事件状态更新。
"""

import uuid
from datetime import datetime
from v2.domain.models import ReviewAction, Signal, CanonicalEvent
from v2.domain.enums import ReviewActionType, EventStatus
from v2.repositories.review_actions_repository import ReviewActionsRepository, InMemoryReviewActionsRepository
from v2.repositories.event_repository import EventRepository


def _generate_action_id() -> str:
    """生成操作 ID。"""
    return f"ACTION_{uuid.uuid4().hex[:12].upper()}"


def _update_event_status(
    action_type: str,
    event: CanonicalEvent,
    event_repository: EventRepository | None,
) -> CanonicalEvent | None:
    """
    根据操作类型更新事件状态。
    
    映射规则：
    - MARK_AS_RELEVANT: detected -> confirmed
    - MARK_AS_IRRELEVANT: detected -> monitoring (或保持)
    - ARCHIVE: any -> resolved
    - ESCALATE: any -> active
    
    Args:
        action_type: 操作类型
        event: 事件
        event_repository: 事件存储
        
    Returns:
        更新后的事件（如果有更新）
    """
    new_status = None
    
    if action_type == ReviewActionType.MARK_AS_RELEVANT.value:
        if event.status == EventStatus.DETECTED.value:
            new_status = EventStatus.CONFIRMED.value
    elif action_type == ReviewActionType.ARCHIVE.value:
        new_status = EventStatus.RESOLVED.value
    elif action_type == ReviewActionType.ESCALATE.value:
        new_status = EventStatus.ACTIVE.value
    
    if new_status and event_repository:
        # 创建更新后的事件
        updated_event = CanonicalEvent(
            event_id=event.event_id,
            cluster_id=event.cluster_id,
            canonical_title=event.canonical_title,
            event_type=event.event_type,
            region=event.region,
            country_codes=event.country_codes,
            normalized_entities=event.normalized_entities,
            first_seen_at=event.first_seen_at,
            last_seen_at=event.last_seen_at,
            occurred_at_start=event.occurred_at_start,
            occurred_at_end=event.occurred_at_end,
            status=new_status,
            phase=event.phase,
            evidence_count=event.evidence_count,
            embedding=event.embedding,
            metadata=event.metadata,
        )
        event_repository.update_event(updated_event)
        return updated_event
    
    return None


def log_review_action(
    signal: Signal,
    action_type: str,
    analyst_id: str,
    event: CanonicalEvent | None = None,
    event_repository: EventRepository | None = None,
    review_repository: ReviewActionsRepository | None = None,
    comment: str | None = None,
    exposure_override: dict | None = None,
    severity_override: float | None = None,
    agreement_with_ai: bool | None = None,
    now: datetime | None = None,
) -> ReviewAction:
    """
    记录分析师操作。
    
    Args:
        signal: 信号
        action_type: 操作类型
        analyst_id: 分析师 ID
        event: 事件（可选，用于状态更新）
        event_repository: 事件存储（可选）
        review_repository: 操作记录存储（可选）
        comment: 评论
        exposure_override: 暴露修正
        severity_override: 严重度修正
        agreement_with_ai: 是否认同 AI
        now: 当前时间
        
    Returns:
        ReviewAction
    """
    if now is None:
        now = datetime.now()
    
    # 创建操作记录
    action = ReviewAction(
        action_id=_generate_action_id(),
        signal_id=signal.signal_id,
        action_type=action_type,
        action_taken_by=analyst_id,
        action_timestamp=now,
        comment=comment,
        exposure_override=exposure_override,
        severity_override=severity_override,
        agreement_with_ai=agreement_with_ai,
    )
    
    # 保存操作记录
    if review_repository:
        review_repository.save_action(action)
    
    # 更新事件状态
    if event and event_repository:
        _update_event_status(action_type, event, event_repository)
    
    return action
