"""
Integration test for resolution pipeline.
"""

from datetime import datetime, timedelta

from v2.config import DEFAULT_RESOLUTION_CONFIG
from v2.domain.enums import ResolutionDecisionType
from v2.repositories.event_repository import InMemoryEventRepository
from v2.services.candidate_builder import build_candidates_from_list
from v2.services.resolution_engine import apply_resolution, resolve_candidate


class TestResolutionPipeline:
    """Integration test for full resolution pipeline."""
    
    def test_full_pipeline_same_event_different_headlines(self):
        """
        Test: Same event with different headlines should UPDATE_EVENT.
        
        Candidate A: Red Sea attacks force rerouting of container vessels
        Candidate B: Container ships diverted around Cape of Good Hope amid Red Sea risk
        
        Expected: Both go to same canonical event, evidence_count=2
        """
        now = datetime(2024, 1, 15, 12, 0, 0)
        repository = InMemoryEventRepository()
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidates_data = [
            {
                "title": "Red Sea attacks force rerouting of container vessels",
                "summary": "Houthi attacks force rerouting",
                "event_type": "shipping_disruption",
                "region": "Middle East",
                "country_codes": ["YE", "EG"],
                "entity_names": ["Red Sea", "container shipping", "Houthis"],
                "occurred_at": "2024-01-15T10:00:00",
                "embedding": [0.91, 0.05, 0.12],
            },
            {
                "title": "Container ships diverted around Cape of Good Hope amid Red Sea risk",
                "summary": "Shipping companies divert vessels",
                "event_type": "shipping_disruption",
                "region": "Middle East",
                "country_codes": ["ZA", "EG"],
                "entity_names": ["red sea", "container shipping", "cape of good hope"],
                "occurred_at": "2024-01-15T14:00:00",
                "embedding": [0.89, 0.08, 0.10],
            },
        ]
        
        candidates = build_candidates_from_list(candidates_data, now)
        
        # Process first candidate
        decision1 = resolve_candidate(candidates[0], repository, now, config)
        result1 = apply_resolution(candidates[0], decision1, repository, now)
        
        assert decision1.decision_type == ResolutionDecisionType.NEW_EVENT.value
        assert result1.created_new_event is True
        
        # Process second candidate
        decision2 = resolve_candidate(candidates[1], repository, now, config)
        result2 = apply_resolution(candidates[1], decision2, repository, now)
        
        # Should update existing event
        assert decision2.decision_type == ResolutionDecisionType.UPDATE_EVENT.value
        assert result2.updated_existing_event is True
        assert result2.event.event_id == result1.event.event_id
        assert result2.event.evidence_count == 2
    
    def test_full_pipeline_different_events(self):
        """
        Test: Different events should create separate canonical events.
        
        Candidate A: Red Sea shipping (shipping_disruption)
        Candidate B: Labor strike at Port of Montreal (labor_strike)
        
        Expected: Two separate canonical events
        """
        now = datetime(2024, 1, 15, 12, 0, 0)
        repository = InMemoryEventRepository()
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidates_data = [
            {
                "title": "Red Sea attacks force rerouting of container vessels",
                "summary": "Houthi attacks",
                "event_type": "shipping_disruption",
                "region": "Middle East",
                "country_codes": ["EG"],
                "entity_names": ["Red Sea", "container shipping"],
                "occurred_at": "2024-01-15T10:00:00",
                "embedding": [0.91, 0.05, 0.12],
            },
            {
                "title": "Labor strike begins at Port of Montreal after talks fail",
                "summary": "Port workers strike",
                "event_type": "labor_strike",
                "region": "North America",
                "country_codes": ["CA"],
                "entity_names": ["port of montreal", "labor union"],
                "occurred_at": "2024-01-15T08:00:00",
                "embedding": [0.71, 0.14, 0.10],
            },
        ]
        
        candidates = build_candidates_from_list(candidates_data, now)
        
        # Process both candidates
        for candidate in candidates:
            decision = resolve_candidate(candidate, repository, now, config)
            apply_resolution(candidate, decision, repository, now)
        
        # Should have 2 separate events
        assert repository.count() == 2
        
        events = repository.list_all_events()
        event_types = {e.event_type for e in events}
        assert event_types == {"shipping_disruption", "labor_strike"}
    
    def test_full_pipeline_high_semantic_low_entity(self):
        """
        Test: High semantic similarity but low entity overlap should NOT update.
        
        Existing: Export restrictions on gallium from China
        Candidate: Export restrictions on graphite from Mozambique
        
        Expected: NEW_EVENT (not update)
        """
        now = datetime(2024, 1, 15, 12, 0, 0)
        repository = InMemoryEventRepository()
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Create existing event
        from v2.domain.enums import EventPhase, EventStatus
        from v2.domain.models import CanonicalEvent
        
        existing = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Export restrictions on gallium from China",
            event_type="export_control",
            region="Asia-Pacific",
            country_codes=["CN"],
            normalized_entities=["china", "gallium"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
            embedding=[0.82, 0.10, 0.05],
        )
        repository.create_event(existing)
        
        # Candidate with similar embedding but different entities
        candidate_data = {
            "title": "Export restrictions on graphite from Mozambique",
            "summary": "New export controls",
            "event_type": "export_control",
            "region": "Africa",
            "country_codes": ["MZ"],
            "entity_names": ["mozambique", "graphite"],
            "occurred_at": "2024-01-15T10:00:00",
            "embedding": [0.81, 0.09, 0.06],  # Similar embedding
        }
        
        candidate = build_candidates_from_list([candidate_data], now)[0]
        
        decision = resolve_candidate(candidate, repository, now, config)
        
        # Should be NEW_EVENT because entity overlap is low
        assert decision.decision_type == ResolutionDecisionType.NEW_EVENT.value
        assert decision.entity_overlap_score < config.same_event_entity_overlap_threshold
