"""
Unit tests for resolution engine.
"""

import pytest
from datetime import datetime, timedelta
from v2.config import DEFAULT_RESOLUTION_CONFIG
from v2.domain.models import EventCandidate, CanonicalEvent, ResolutionDecision
from v2.domain.enums import ResolutionDecisionType, EventStatus, EventPhase
from v2.repositories.event_repository import InMemoryEventRepository
from v2.services.resolution_engine import resolve_candidate, apply_resolution


class TestResolveCandidate:
    """Test resolve_candidate function."""
    
    @pytest.fixture
    def repository(self):
        """Create a repository with sample events."""
        repo = InMemoryEventRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        event = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Red Sea shipping disruption",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["EG"],
            normalized_entities=["red sea", "container shipping", "houthis"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
            embedding=[0.91, 0.05, 0.12],
        )
        repo.create_event(event)
        
        return repo
    
    def test_reject_short_title(self):
        """Should reject candidate with short title."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        repo = InMemoryEventRepository()
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Short",
            summary="Too short",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            entity_names=["test"],
            normalized_entities=["test"],
            occurred_at=now,
            detected_at=now,
        )
        
        decision = resolve_candidate(candidate, repo, now, config)
        
        assert decision.decision_type == ResolutionDecisionType.REJECT_CANDIDATE.value
        assert "title too short" in decision.reason
    
    def test_reject_missing_event_type(self):
        """Should reject candidate with missing event_type."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        repo = InMemoryEventRepository()
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Valid title here",
            summary="Summary",
            event_type="",
            region="Middle East",
            country_codes=[],
            entity_names=["test"],
            normalized_entities=["test"],
            occurred_at=now,
            detected_at=now,
        )
        
        decision = resolve_candidate(candidate, repo, now, config)
        
        assert decision.decision_type == ResolutionDecisionType.REJECT_CANDIDATE.value
        assert "event_type is empty" in decision.reason
    
    def test_update_existing_event(self, repository):
        """Should update existing event when high similarity."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Candidate with high similarity to EVT_001
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Container ships diverted around Cape of Good Hope amid Red Sea risk",
            summary="Shipping update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["ZA"],
            entity_names=["red sea", "container shipping", "cape of good hope"],
            normalized_entities=["red sea", "container shipping", "cape of good hope"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.89, 0.08, 0.10],  # High similarity
        )
        
        decision = resolve_candidate(candidate, repository, now, config)
        
        assert decision.decision_type == ResolutionDecisionType.UPDATE_EVENT.value
        assert decision.matched_event_id == "EVT_001"
        assert decision.similarity_score >= config.same_event_embedding_threshold
    
    def test_new_event_in_existing_cluster(self, repository):
        """Should create new event in existing cluster when moderate similarity."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Candidate with moderate similarity
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Suez Canal shipping update",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["EG"],
            entity_names=["suez canal", "shipping"],
            normalized_entities=["suez canal", "shipping"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.70, 0.20, 0.10],  # Moderate similarity
        )
        
        decision = resolve_candidate(candidate, repository, now, config)
        
        # Should be NEW_EVENT or NEW_EVENT_IN_EXISTING_CLUSTER
        assert decision.decision_type in [
            ResolutionDecisionType.NEW_EVENT.value,
            ResolutionDecisionType.NEW_EVENT_IN_EXISTING_CLUSTER.value,
        ]
    
    def test_new_event_no_match(self, repository):
        """Should create new event when no match found."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Candidate with very different embedding
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Labor strike at Montreal port",
            summary="Labor update",
            event_type="labor_strike",
            region="North America",
            country_codes=["CA"],
            entity_names=["montreal", "labor"],
            normalized_entities=["montreal", "labor"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.10, 0.90, 0.00],  # Very different
        )
        
        decision = resolve_candidate(candidate, repository, now, config)
        
        assert decision.decision_type == ResolutionDecisionType.NEW_EVENT.value
        assert decision.matched_event_id is None
    
    def test_time_window_exceeded(self, repository):
        """Should create new event when time window exceeded."""
        now = datetime(2024, 2, 20, 12, 0, 0)  # 35 days later
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Candidate with high similarity but outside time window
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Red Sea shipping disruption continues",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["EG"],
            entity_names=["red sea", "container shipping", "houthis"],
            normalized_entities=["red sea", "container shipping", "houthis"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.91, 0.05, 0.12],
        )
        
        decision = resolve_candidate(candidate, repository, now, config)
        
        # Time score should be 0, so no update
        assert decision.decision_type == ResolutionDecisionType.NEW_EVENT.value


class TestApplyResolution:
    """Test apply_resolution function."""
    
    def test_create_new_event(self):
        """Should create new event for NEW_EVENT decision."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        repo = InMemoryEventRepository()
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Test event",
            summary="Test",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            entity_names=["test"],
            normalized_entities=["test"],
            occurred_at=now,
            detected_at=now,
        )
        
        decision = ResolutionDecision(
            decision_type=ResolutionDecisionType.NEW_EVENT.value,
            matched_event_id=None,
            matched_cluster_id=None,
            similarity_score=0.0,
            entity_overlap_score=0.0,
            time_score=0.0,
            reason="test",
        )
        
        result = apply_resolution(candidate, decision, repo, now)
        
        assert result.created_new_event is True
        assert result.updated_existing_event is False
        assert repo.count() == 1
    
    def test_update_existing_event(self):
        """Should update existing event for UPDATE_EVENT decision."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        repo = InMemoryEventRepository()
        
        # Create existing event
        existing = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Original title",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["EG"],
            normalized_entities=["red sea"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
        )
        repo.create_event(existing)
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Updated title",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["SA"],
            entity_names=["red sea", "houthis"],
            normalized_entities=["red sea", "houthis"],
            occurred_at=now,
            detected_at=now,
        )
        
        decision = ResolutionDecision(
            decision_type=ResolutionDecisionType.UPDATE_EVENT.value,
            matched_event_id="EVT_001",
            matched_cluster_id="CLUSTER_001",
            similarity_score=0.9,
            entity_overlap_score=0.5,
            time_score=1.0,
            reason="test",
        )
        
        result = apply_resolution(candidate, decision, repo, now)
        
        assert result.created_new_event is False
        assert result.updated_existing_event is True
        assert result.event.evidence_count == 2
        assert "houthis" in result.event.normalized_entities
