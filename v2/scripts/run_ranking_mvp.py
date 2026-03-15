"""
Ranking MVP Runner

演示 runner，展示 ranking 流程。
"""

from datetime import datetime
from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.models import CanonicalEvent, Exposure
from v2.domain.enums import EventStatus, EventPhase, ExposureDirection, ExposureChannel
from v2.repositories.signal_repository import InMemorySignalRepository
from v2.services.signal_engine import generate_signal_for_event


def run_ranking_demo():
    """运行 ranking 演示。"""
    print("=" * 70)
    print("Geo Market Watch V2 - Ranking MVP Demo")
    print("=" * 70)
    print()
    
    now = datetime(2024, 1, 15, 12, 0, 0)
    config = DEFAULT_RANKING_CONFIG
    repository = InMemorySignalRepository()
    
    # 示例事件 1: Red Sea shipping disruption (high priority)
    event1 = CanonicalEvent(
        event_id="EVT_001",
        cluster_id="CLUSTER_001",
        canonical_title="Red Sea shipping disruption escalates",
        event_type="shipping_disruption",
        region="red sea",
        country_codes=["EG", "YE"],
        normalized_entities=["red sea", "suez canal", "container shipping", "houthis"],
        first_seen_at=now,
        last_seen_at=now,
        occurred_at_start=now,
        occurred_at_end=now,
        status=EventStatus.ACTIVE.value,
        phase=EventPhase.ESCALATION.value,
        evidence_count=3,
    )
    
    exposures1 = [
        Exposure(
            exposure_id="EXP_001",
            event_id="EVT_001",
            target_type="route",
            target_id="red_sea",
            target_name="Red Sea",
            exposure_channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            direction=ExposureDirection.NEGATIVE.value,
            magnitude_score=0.80,
            confidence_score=0.85,
            horizon="days",
            source_type="direct_rule",
            source_ref="rule1",
            reasoning_trace="direct rule",
            trace_steps=[],
        ),
        Exposure(
            exposure_id="EXP_002",
            event_id="EVT_001",
            target_type="theme",
            target_id="europe_import_supply_chain",
            target_name="Europe Import Supply Chain",
            exposure_channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            direction=ExposureDirection.NEGATIVE.value,
            magnitude_score=0.58,
            confidence_score=0.70,
            horizon="weeks",
            source_type="direct_rule",
            source_ref="rule2",
            reasoning_trace="template expansion",
            trace_steps=[],
        ),
        Exposure(
            exposure_id="EXP_003",
            event_id="EVT_001",
            target_type="sector",
            target_id="container_shipping",
            target_name="Container Shipping",
            exposure_channel=ExposureChannel.PRICING_POWER_SHIFT.value,
            direction=ExposureDirection.MIXED.value,
            magnitude_score=0.65,
            confidence_score=0.65,
            horizon="weeks",
            source_type="direct_rule",
            source_ref="rule3",
            reasoning_trace="direct rule",
            trace_steps=[],
        ),
    ]
    
    # 示例事件 2: Old low-confidence local strike (low signal)
    event2 = CanonicalEvent(
        event_id="EVT_002",
        cluster_id="CLUSTER_002",
        canonical_title="Local labor strike at small factory",
        event_type="labor_strike",
        region="North America",
        country_codes=["US"],
        normalized_entities=["factory", "labor"],
        first_seen_at=now - timedelta(days=5),
        last_seen_at=now - timedelta(days=5),
        occurred_at_start=now - timedelta(days=5),
        occurred_at_end=now - timedelta(days=5),
        status=EventStatus.MONITORING.value,
        phase=EventPhase.WARNING.value,
        evidence_count=1,
    )
    
    exposures2 = [
        Exposure(
            exposure_id="EXP_004",
            event_id="EVT_002",
            target_type="facility",
            target_id="local_factory",
            target_name="Local Factory",
            exposure_channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
            direction=ExposureDirection.NEGATIVE.value,
            magnitude_score=0.30,
            confidence_score=0.50,
            horizon="days",
            source_type="direct_rule",
            source_ref="rule1",
            reasoning_trace="direct rule",
            trace_steps=[],
        ),
    ]
    
    events_data = [
        (event1, exposures1, "High priority shipping disruption"),
        (event2, exposures2, "Low priority local strike"),
    ]
    
    for event, exposures, desc in events_data:
        print(f"\n{'='*70}")
        print(f"Event: {event.event_id} | {event.canonical_title}")
        print(f"Description: {desc}")
        print("=" * 70)
        
        # 生成信号
        result = generate_signal_for_event(
            event=event,
            exposures=exposures,
            signal_repository=repository,
            now=now,
            config=config,
        )
        
        # 打印 Features
        print("\nFeatures:")
        features = result.features
        print(f"  - severity={features.severity_score:.2f}")
        print(f"  - market_relevance={features.market_relevance_score:.2f}")
        print(f"  - novelty={features.novelty_score:.2f}")
        print(f"  - confidence={features.confidence_score:.2f}")
        print(f"  - breadth={features.breadth_score:.2f}")
        print(f"  - urgency={features.urgency_score:.2f}")
        
        # 打印 Score Breakdown
        print("\nScore Breakdown:")
        breakdown = result.breakdown
        print(f"  - base={breakdown.base_score:.2f}")
        print(f"  - watchlist_boost={breakdown.watchlist_boost:.2f}")
        print(f"  - analyst_boost={breakdown.analyst_interest_boost:.2f}")
        print(f"  - duplicate_penalty={breakdown.duplicate_penalty:.2f}")
        print(f"  - low_evidence_penalty={breakdown.low_evidence_penalty:.2f}")
        print(f"  - final={breakdown.final_score:.2f}")
        
        # 打印 Signal
        print("\nSignal:")
        signal = result.signal
        print(f"  - class={signal.signal_class}")
        print(f"  - queue={signal.assigned_queue}")
        print(f"  - rank_score={signal.rank_score:.2f}")
        
        # 打印 Summary
        print("\nSummary:")
        print(f"  {signal.summary_text}")
        
        # 打印 Reasoning Trace（简化）
        print("\nReasoning (first 200 chars):")
        print(f"  {signal.reasoning_trace[:200]}...")
    
    # 最终摘要
    print("\n" + "=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"\nTotal signals generated: {repository.count()}")
    
    for signal in repository.list_signals():
        print(f"  - {signal.signal_id}: {signal.signal_class} (score={signal.rank_score:.2f}, queue={signal.assigned_queue})")


if __name__ == "__main__":
    from datetime import timedelta
    run_ranking_demo()
