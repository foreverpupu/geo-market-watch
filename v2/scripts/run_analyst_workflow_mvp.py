"""
Analyst Workflow MVP Runner

演示分析师工作流。
"""

from datetime import datetime, timedelta

from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG
from v2.domain.enums import EventPhase, EventStatus, ReviewActionType, SignalClass
from v2.domain.models import CanonicalEvent, Signal
from v2.repositories.audit_trail_repository import InMemoryAuditTrailRepository
from v2.repositories.event_repository import InMemoryEventRepository
from v2.repositories.review_actions_repository import InMemoryReviewActionsRepository
from v2.repositories.triage_queue_repository import InMemoryTriageQueueRepository
from v2.repositories.watchlist_repository import InMemoryWatchlistRepository
from v2.services.analyst_workflow import manage_analyst_workflow
from v2.services.triage_queue import check_expired_items


def run_analyst_workflow_demo():
    """运行分析师工作流演示。"""
    print("=" * 70)
    print("Geo Market Watch V2 - Analyst Workflow MVP Demo")
    print("=" * 70)
    print()
    
    now = datetime(2024, 1, 15, 12, 0, 0)
    config = DEFAULT_ANALYST_WORKFLOW_CONFIG
    
    # 初始化 repositories
    triage_repo = InMemoryTriageQueueRepository()
    review_repo = InMemoryReviewActionsRepository()
    audit_repo = InMemoryAuditTrailRepository()
    watchlist_repo = InMemoryWatchlistRepository()
    event_repo = InMemoryEventRepository()
    
    # 创建示例事件和信号
    event = CanonicalEvent(
        event_id="EVT_001",
        cluster_id="CLUSTER_001",
        canonical_title="Red Sea shipping disruption escalates",
        event_type="shipping_disruption",
        region="red sea",
        country_codes=["EG", "YE"],
        normalized_entities=["red sea", "suez canal", "container shipping"],
        first_seen_at=now,
        last_seen_at=now,
        occurred_at_start=now,
        occurred_at_end=now,
        status=EventStatus.DETECTED.value,
        phase=EventPhase.ESCALATION.value,
        evidence_count=3,
    )
    event_repo.create_event(event)
    
    signal = Signal(
        signal_id="SIG_001",
        event_id="EVT_001",
        signal_class=SignalClass.HIGH_PRIORITY.value,
        rank_score=0.85,
        severity_score=0.70,
        market_relevance_score=0.80,
        novelty_score=0.75,
        confidence_score=0.68,
        breadth_score=0.60,
        urgency_score=0.90,
        watchlist_match_score=0.0,
        assigned_queue="triage",
        status="generated",
        summary_text="Red Sea shipping disruption with high urgency",
        reasoning_trace="High priority due to urgency and market relevance",
        generated_at=now,
    )
    
    print(f"Event: {event.event_id} | {event.canonical_title}")
    print(f"Signal: {signal.signal_id} | rank_score={signal.rank_score}")
    print(f"Initial Event Status: {event.status}")
    print()
    
    # 场景 1: 信号进入 Triage Queue
    print("-" * 70)
    print("Scenario 1: Signal enters Triage Queue")
    print("-" * 70)
    
    result1 = manage_analyst_workflow(
        signal=signal,
        event=event,
        triage_repository=triage_repo,
        config=config,
        now=now,
    )
    
    print(f"Triage item added: {result1.get('triage_item_added', False)}")
    print(f"Actions: {result1.get('actions', [])}")
    print()
    
    # 场景 2: 分析师申领并标记为相关
    print("-" * 70)
    print("Scenario 2: Analyst claims and marks as relevant")
    print("-" * 70)
    
    result2 = manage_analyst_workflow(
        signal=signal,
        event=event,
        analyst_id="analyst_001",
        action_type=ReviewActionType.MARK_AS_RELEVANT.value,
        comment="Confirmed: major shipping disruption",
        agreement_with_ai=True,
        triage_repository=triage_repo,
        review_repository=review_repo,
        audit_repository=audit_repo,
        event_repository=event_repo,
        config=config,
        now=now,
    )
    
    print(f"Actions: {result2.get('actions', [])}")
    print(f"Action ID: {result2.get('action_id')}")
    print(f"Audit Entry ID: {result2.get('audit_entry_id')}")
    
    # 检查事件状态更新
    updated_event = event_repo.get_event(event.event_id)
    print(f"Updated Event Status: {updated_event.status}")
    print()
    
    # 场景 3: 分析师添加到 Watchlist
    print("-" * 70)
    print("Scenario 3: Analyst adds to watchlist")
    print("-" * 70)
    
    result3 = manage_analyst_workflow(
        signal=signal,
        event=updated_event,
        analyst_id="analyst_001",
        action_type=ReviewActionType.ADD_TO_WATCHLIST.value,
        comment="Monitor for further escalation",
        triage_repository=triage_repo,
        review_repository=review_repo,
        audit_repository=audit_repo,
        watchlist_repository=watchlist_repo,
        config=config,
        now=now,
    )
    
    print(f"Actions: {result3.get('actions', [])}")
    print(f"Watchlist entry added: {result3.get('watchlist_entry_added', False)}")
    print()
    
    # 场景 4: 检查过期项
    print("-" * 70)
    print("Scenario 4: Check expired items")
    print("-" * 70)
    
    # 创建一个即将过期的信号
    old_signal = Signal(
        signal_id="SIG_002",
        event_id="EVT_002",
        signal_class=SignalClass.MONITOR.value,
        rank_score=0.82,
        severity_score=0.60,
        market_relevance_score=0.70,
        novelty_score=0.50,
        confidence_score=0.65,
        breadth_score=0.40,
        urgency_score=0.60,
        watchlist_match_score=0.0,
        assigned_queue="triage",
        status="generated",
        summary_text="Old signal",
        reasoning_trace="Monitor",
        generated_at=now - timedelta(hours=50),
    )
    
    from v2.services.triage_queue import add_to_triage_queue
    add_to_triage_queue(old_signal, config, triage_repo, now - timedelta(hours=50))
    
    # 检查过期
    expired = check_expired_items(triage_repo, now)
    print(f"Expired items found: {len(expired)}")
    if expired:
        print(f"Expired signal: {expired[0].signal_id}, status: {expired[0].status}")
    print()
    
    # 场景 5: 分析师修正 AI 结果
    print("-" * 70)
    print("Scenario 5: Analyst overrides AI results")
    print("-" * 70)
    
    result5 = manage_analyst_workflow(
        signal=signal,
        event=updated_event,
        analyst_id="analyst_002",
        action_type=ReviewActionType.COMMENT.value,
        comment="Adjusting severity based on new intel",
        severity_override=0.90,  # 修正严重度
        agreement_with_ai=False,  # 不认同 AI
        triage_repository=triage_repo,
        review_repository=review_repo,
        audit_repository=audit_repo,
        config=config,
        now=now,
    )
    
    print(f"Actions: {result5.get('actions', [])}")
    print(f"Action ID: {result5.get('action_id')}")
    print()
    
    # 最终摘要
    print("=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"\nTriage Queue: {triage_repo.count()} items")
    print(f"Review Actions: {review_repo.count()} actions")
    print(f"Audit Trail: {audit_repo.count()} entries")
    print(f"Watchlist: {watchlist_repo.count()} entries")
    print()
    
    # 显示审计轨迹
    print("Audit Trail Entries:")
    for entry in audit_repo.list_entries():
        print(f"  - {entry.timestamp}: {entry.action_taken_by} -> {entry.action_type}")
        print(f"    Detail: {entry.action_detail}")


if __name__ == "__main__":
    run_analyst_workflow_demo()
