"""
Resolution MVP Runner

演示 runner，展示 resolution 流程。
"""

from datetime import datetime
from v2.config import DEFAULT_RESOLUTION_CONFIG
from v2.domain.models import EventCandidate
from v2.repositories.event_repository import InMemoryEventRepository
from v2.services.resolution_engine import resolve_candidate, apply_resolution
from v2.services.candidate_builder import build_candidate_from_dict


def run_resolution_demo():
    """运行 resolution 演示。"""
    print("=" * 70)
    print("Geo Market Watch V2 - Resolution MVP Demo")
    print("=" * 70)
    print()
    
    # 初始化
    now = datetime(2024, 1, 15, 12, 0, 0)
    repository = InMemoryEventRepository()
    config = DEFAULT_RESOLUTION_CONFIG
    
    # 示例候选事件
    candidates_data = [
        {
            "title": "Red Sea attacks force rerouting of container vessels",
            "summary": "Houthi attacks in Red Sea force major shipping lines to reroute",
            "event_type": "shipping_disruption",
            "region": "Middle East",
            "country_codes": ["YE", "EG"],
            "entity_names": ["Red Sea", "container shipping", "Houthis"],
            "occurred_at": "2024-01-15T10:00:00",
            "embedding": [0.91, 0.05, 0.12],
        },
        {
            "title": "Container ships diverted around Cape of Good Hope amid Red Sea risk",
            "summary": "Shipping companies announce Cape route to avoid Red Sea attacks",
            "event_type": "shipping_disruption",
            "region": "Middle East",
            "country_codes": ["ZA", "EG"],
            "entity_names": ["red sea", "container shipping", "cape of good hope"],
            "occurred_at": "2024-01-15T14:00:00",
            "embedding": [0.89, 0.08, 0.10],
        },
        {
            "title": "Labor strike begins at Port of Montreal after talks fail",
            "summary": "Port workers strike disrupts Canadian maritime trade",
            "event_type": "labor_strike",
            "region": "North America",
            "country_codes": ["CA"],
            "entity_names": ["port of montreal", "labor union"],
            "occurred_at": "2024-01-15T08:00:00",
            "embedding": [0.71, 0.14, 0.10],
        },
        {
            "title": "Short",
            "summary": "Too short",
            "event_type": "",
            "region": None,
            "country_codes": [],
            "entity_names": [],
            "occurred_at": "2024-01-15T08:00:00",
            "embedding": None,
        },
    ]
    
    results = []
    
    for i, data in enumerate(candidates_data, 1):
        print(f"\n--- Candidate {i} ---")
        print(f"Title: {data['title'][:60]}...")
        
        # 构建候选
        candidate = build_candidate_from_dict(data, now)
        
        # Resolve
        decision = resolve_candidate(candidate, repository, now, config)
        print(f"Decision: {decision.decision_type}")
        
        if decision.matched_event_id:
            print(f"Matched Event: {decision.matched_event_id}")
        if decision.matched_cluster_id:
            print(f"Cluster: {decision.matched_cluster_id}")
        print(f"Scores: sim={decision.similarity_score:.2f}, entity={decision.entity_overlap_score:.2f}, time={decision.time_score:.2f}")
        print(f"Reason: {decision.reason}")
        
        # Apply resolution
        result = apply_resolution(candidate, decision, repository, now)
        results.append(result)
        
        print(f"Result: Event {result.event.event_id}, Evidence count: {result.event.evidence_count}")
    
    # 最终摘要
    print("\n" + "=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"\nTotal canonical events: {repository.count()}")
    
    for event in repository.list_all_events():
        print(f"- {event.event_id} | {event.canonical_title[:50]}... | evidence_count={event.evidence_count} | phase={event.phase}")
    
    print()
    
    # 统计
    new_events = sum(1 for r in results if r.created_new_event)
    updated_events = sum(1 for r in results if r.updated_existing_event)
    rejected = sum(1 for r in results if r.decision.decision_type == "REJECT_CANDIDATE")
    
    print(f"Stats: {new_events} new, {updated_events} updated, {rejected} rejected")


if __name__ == "__main__":
    run_resolution_demo()
