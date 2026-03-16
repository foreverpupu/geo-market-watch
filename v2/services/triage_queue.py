"""
Triage Queue

Triage 队列管理。
"""

import uuid
from datetime import datetime, timedelta

from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG, AnalystWorkflowConfig
from v2.domain.enums import TriageStatus
from v2.domain.models import Signal, TriageQueueItem
from v2.repositories.triage_queue_repository import (
    TriageQueueRepository,
)


def _generate_item_id() -> str:
    """生成队列项 ID。"""
    return f"TRIAGE_{uuid.uuid4().hex[:12].upper()}"


def add_to_triage_queue(
    signal: Signal,
    config: AnalystWorkflowConfig = DEFAULT_ANALYST_WORKFLOW_CONFIG,
    repository: TriageQueueRepository | None = None,
    now: datetime | None = None,
) -> TriageQueueItem:
    """
    将信号添加到 Triage 队列。
    
    如果信号分数高于 triage_priority_threshold，则添加到队列。
    
    Args:
        signal: 信号
        config: 配置
        repository: 存储（可选）
        now: 当前时间
        
    Returns:
        TriageQueueItem
    """
    if now is None:
        now = datetime.now()
    
    # 检查是否满足阈值
    if signal.rank_score < config.triage_priority_threshold:
        raise ValueError(f"Signal rank_score {signal.rank_score} below threshold {config.triage_priority_threshold}")
    
    # 计算截止时间
    due_by = now + timedelta(hours=config.review_action_timeout)
    
    item = TriageQueueItem(
        signal_id=signal.signal_id,
        event_id=signal.event_id,
        rank_score=signal.rank_score,
        assigned_to=None,  # 初始未分配
        added_at=now,
        due_by=due_by,
        status=TriageStatus.PENDING.value,
    )
    
    if repository:
        repository.add_item(item)
    
    return item


def claim_signal(
    signal_id: str,
    analyst_id: str,
    repository: TriageQueueRepository,
    now: datetime | None = None,
) -> TriageQueueItem:
    """
    分析师申领信号。
    
    Args:
        signal_id: 信号 ID
        analyst_id: 分析师 ID
        repository: 存储
        now: 当前时间
        
    Returns:
        更新后的 TriageQueueItem
    """
    if now is None:
        now = datetime.now()
    
    item = repository.get_item(signal_id)
    if item is None:
        raise ValueError(f"Signal {signal_id} not found in triage queue")
    
    if item.assigned_to is not None:
        raise ValueError(f"Signal {signal_id} already claimed by {item.assigned_to}")
    
    # 更新分配
    updated_item = TriageQueueItem(
        signal_id=item.signal_id,
        event_id=item.event_id,
        rank_score=item.rank_score,
        assigned_to=analyst_id,
        added_at=item.added_at,
        due_by=item.due_by,
        status=TriageStatus.IN_REVIEW.value,
        metadata=item.metadata,
    )
    
    repository.update_item(updated_item)
    return updated_item


def check_expired_items(
    repository: TriageQueueRepository,
    now: datetime | None = None,
) -> list[TriageQueueItem]:
    """
    检查并返回已过期的队列项。
    
    Args:
        repository: 存储
        now: 当前时间
        
    Returns:
        已过期的队列项列表
    """
    if now is None:
        now = datetime.now()
    
    expired_items = []
    for item in repository.list_items():
        if item.status in {TriageStatus.PENDING.value, TriageStatus.IN_REVIEW.value}:
            if now > item.due_by:
                # 标记为过期
                expired_item = TriageQueueItem(
                    signal_id=item.signal_id,
                    event_id=item.event_id,
                    rank_score=item.rank_score,
                    assigned_to=item.assigned_to,
                    added_at=item.added_at,
                    due_by=item.due_by,
                    status=TriageStatus.EXPIRED.value,
                    metadata=item.metadata,
                )
                repository.update_item(expired_item)
                expired_items.append(expired_item)
    
    return expired_items
