"""
Analyst Workflow

Step 4 orchestrator，管理整个分析师工作流。
"""

from datetime import datetime

from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG, AnalystWorkflowConfig
from v2.domain.enums import ReviewActionType
from v2.domain.models import CanonicalEvent, Signal
from v2.repositories.audit_trail_repository import AuditTrailRepository
from v2.repositories.event_repository import EventRepository
from v2.repositories.review_actions_repository import ReviewActionsRepository
from v2.repositories.triage_queue_repository import TriageQueueRepository
from v2.repositories.watchlist_repository import WatchlistRepository
from v2.services.audit_trail import log_audit_trail
from v2.services.review_actions import log_review_action
from v2.services.triage_queue import add_to_triage_queue, claim_signal
from v2.services.watchlist_routing import route_signal_to_watchlist


def manage_analyst_workflow(
    signal: Signal,
    event: CanonicalEvent,
    analyst_id: str | None = None,
    action_type: str | None = None,
    comment: str | None = None,
    exposure_override: dict | None = None,
    severity_override: float | None = None,
    agreement_with_ai: bool | None = None,
    triage_repository: TriageQueueRepository | None = None,
    review_repository: ReviewActionsRepository | None = None,
    audit_repository: AuditTrailRepository | None = None,
    watchlist_repository: WatchlistRepository | None = None,
    event_repository: EventRepository | None = None,
    config: AnalystWorkflowConfig = DEFAULT_ANALYST_WORKFLOW_CONFIG,
    now: datetime | None = None,
) -> dict:
    """
    管理分析师工作流。
    
    流程：
    1. 如果信号满足阈值，添加到 Triage Queue
    2. 如果提供了 action_type，记录操作
    3. 更新事件状态
    4. 记录审计轨迹
    5. 如果操作是 ADD_TO_WATCHLIST，添加到 Watchlist
    
    Args:
        signal: 信号
        event: 事件
        analyst_id: 分析师 ID（可选）
        action_type: 操作类型（可选）
        comment: 评论（可选）
        exposure_override: 暴露修正（可选）
        severity_override: 严重度修正（可选）
        agreement_with_ai: 是否认同 AI（可选）
        triage_repository: Triage 存储（可选）
        review_repository: 操作记录存储（可选）
        audit_repository: 审计存储（可选）
        watchlist_repository: Watchlist 存储（可选）
        event_repository: 事件存储（可选）
        config: 配置
        now: 当前时间
        
    Returns:
        工作流结果字典
    """
    if now is None:
        now = datetime.now()
    
    result = {
        "signal_id": signal.signal_id,
        "event_id": event.event_id,
        "actions": [],
    }
    
    # Step 1: 添加到 Triage Queue（如果满足阈值）
    triage_item = None
    if signal.rank_score >= config.triage_priority_threshold:
        try:
            triage_item = add_to_triage_queue(
                signal=signal,
                config=config,
                repository=triage_repository,
                now=now,
            )
            result["triage_item_added"] = True
            result["actions"].append("added_to_triage_queue")
        except ValueError:
            result["triage_item_added"] = False
    
    # Step 2: 如果提供了 analyst_id 和 action_type，执行操作
    if analyst_id and action_type:
        # 申领信号
        if triage_repository and triage_item:
            claim_signal(signal.signal_id, analyst_id, triage_repository, now)
            result["actions"].append("claimed")
        
        # 记录操作
        action = log_review_action(
            signal=signal,
            action_type=action_type,
            analyst_id=analyst_id,
            event=event,
            event_repository=event_repository,
            review_repository=review_repository,
            comment=comment,
            exposure_override=exposure_override,
            severity_override=severity_override,
            agreement_with_ai=agreement_with_ai,
            now=now,
        )
        result["action_id"] = action.action_id
        result["actions"].append("action_logged")
        
        # Step 3: 记录审计轨迹
        audit_entry = log_audit_trail(action, audit_repository, config)
        if audit_entry:
            result["audit_entry_id"] = audit_entry.entry_id
            result["actions"].append("audit_trail_logged")
        
        # Step 4: 如果操作是 ADD_TO_WATCHLIST，添加到 Watchlist
        if action_type == ReviewActionType.ADD_TO_WATCHLIST.value:
            watchlist_entry = route_signal_to_watchlist(
                signal=signal,
                analyst_id=analyst_id,
                reason=comment or "Added by analyst",
                config=config,
                watchlist_repository=watchlist_repository,
                now=now,
            )
            if watchlist_entry:
                result["watchlist_entry_added"] = True
                result["actions"].append("added_to_watchlist")
    
    return result
