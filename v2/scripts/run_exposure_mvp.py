"""
Exposure MVP Runner (Step 2a - Direct Rules Only)

演示 runner，展示 direct exposure 流程。
"""

from datetime import datetime
from v2.config import DEFAULT_EXPOSURE_CONFIG
from v2.domain.models import CanonicalEvent
from v2.domain.enums import EventStatus, EventPhase
from v2.repositories.exposure_repository import InMemoryExposureRepository
from v2.services.exposure_engine import compute_event_exposures


def run_exposure_demo():
    """运行 exposure 演示（Step 2a）。"""
    print("=" * 70)
    print("Geo Market Watch V2 - Exposure MVP Demo (Step 2a: Direct Rules)")
    print("=" * 70)
    print()
    
    now = datetime(2024, 1, 15, 12, 0, 0)
    config = DEFAULT_EXPOSURE_CONFIG
    repository = InMemoryExposureRepository()
    
    # 示例事件 1: Shipping Disruption
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
    
    # 示例事件 2: Export Control
    event2 = CanonicalEvent(
        event_id="EVT_002",
        cluster_id="CLUSTER_002",
        canonical_title="China gallium export controls",
        event_type="export_control",
        region="Asia-Pacific",
        country_codes=["CN"],
        normalized_entities=["china", "gallium", "export controls"],
        first_seen_at=now,
        last_seen_at=now,
        occurred_at_start=now,
        occurred_at_end=now,
        status=EventStatus.ACTIVE.value,
        phase=EventPhase.IMPLEMENTATION.value,
        evidence_count=2,
    )
    
    # 示例事件 3: Labor Strike
    event3 = CanonicalEvent(
        event_id="EVT_003",
        cluster_id="CLUSTER_003",
        canonical_title="Port of Montreal labor strike",
        event_type="labor_strike",
        region="North America",
        country_codes=["CA"],
        normalized_entities=["port of montreal", "labor union", "canada"],
        first_seen_at=now,
        last_seen_at=now,
        occurred_at_start=now,
        occurred_at_end=now,
        status=EventStatus.ACTIVE.value,
        phase=EventPhase.IMPLEMENTATION.value,
        evidence_count=1,
    )
    
    events = [event1, event2, event3]
    
    for event in events:
        print(f"\n{'='*70}")
        print(f"Event: {event.event_id} | {event.canonical_title}")
        print(f"Type: {event.event_type} | Region: {event.region}")
        print(f"Entities: {', '.join(event.normalized_entities)}")
        print("=" * 70)
        
        # 计算暴露
        result = compute_event_exposures(event, repository, config)
        
        # 打印 Direct Exposures
        print("\nDirect Exposures:")
        for exp in result.direct_exposures:
            print(f"  - {exp.target_type}:{exp.target_id} | {exp.direction} | {exp.exposure_channel} | score={exp.magnitude_score:.2f}")
        
        # 打印 Aggregated Exposures
        print("\nAggregated Exposures:")
        for exp in result.aggregated_exposures[:5]:  # 只显示前5个
            print(f"  - {exp.target_type}:{exp.target_id} | {exp.direction} | {exp.exposure_channel} | score={exp.magnitude_score:.2f} | conf={exp.confidence_score:.2f}")
        
        # 打印 Net Exposure Summary
        print("\nNet Exposure Summaries:")
        for summary in result.net_exposure_summaries[:3]:  # 只显示前3个
            print(f"  - {summary.target_type}:{summary.target_id} | net={summary.net_direction} | score={summary.net_score:.2f} (+{summary.positive_score:.2f}/-{summary.negative_score:.2f})")
        
        # 打印 Trace 示例
        if result.aggregated_exposures:
            print("\nSample Reasoning Trace:")
            sample = result.aggregated_exposures[0]
            print(f"  {sample.reasoning_trace}")
    
    # 最终摘要
    print("\n" + "=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"\nTotal events processed: {len(events)}")
    print(f"Total exposures stored: {repository.count()}")
    
    for event in events:
        count = repository.count(event.event_id)
        print(f"  - {event.event_id}: {count} exposures")


if __name__ == "__main__":
    run_exposure_demo()
