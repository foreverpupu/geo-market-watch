"""
Unit tests for event search.
"""

from datetime import datetime, timedelta

import pytest
from v2.config import DEFAULT_RESOLUTION_CONFIG
from v2.domain.enums import EventPhase, EventStatus
from v2.domain.models import CanonicalEvent, EventCandidate
from v2.repositories.event_repository import InMemoryEventRepository
from v2.services.event_search import find_candidate_matches


class TestFindCandidateMatches:
    """Test find_candidate_matches function."""
    
    @pytest.fixture
    def repository(self):
        """Create a repository with sample events."""
        repo = InMemoryEventRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Event 1: Red Sea shipping
        event1 = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Red Sea shipping disruption",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=["EG"],
            normalized_entities=["red sea", "container shipping"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
            embedding=[0.9, 0.1, 0.0],
        )
        repo.create_event(event1)
        
        # Event 2: Labor strike (different type)
        event2 = CanonicalEvent(
            event_id="EVT_002",
            cluster_id="CLUSTER_002",
            canonical_title="Port strike",
            event_type="labor_strike",
            region="North America",
            country_codes=["CA"],
            normalized_entities=["port", "labor union"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
            embedding=[0.1, 0.9, 0.0],
        )
        repo.create_event(event2)
        
        return repo
    
    def test_filter_by_event_type(self, repository):
        """Should filter by event_type."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Red Sea update",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            entity_names=["red sea"],
            normalized_entities=["red sea"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.85, 0.15, 0.0],
        )
        
        matches = find_candidate_matches(candidate, repository, now, config)
        
        # Should only match EVT_001 (same event_type)
        assert len(matches) == 1
        assert matches[0].event.event_id == "EVT_001"
    
    def test_sort_by_total_score(self, repository):
        """Should sort by total score descending."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        # Add another shipping event
        event3 = CanonicalEvent(
            event_id="EVT_003",
            cluster_id="CLUSTER_003",
            canonical_title="Another shipping event",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            normalized_entities=["suez canal"],
            first_seen_at=now - timedelta(days=1),
            last_seen_at=now - timedelta(days=1),
            occurred_at_start=now - timedelta(days=1),
            occurred_at_end=now - timedelta(days=1),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
            embedding=[0.1, 0.1, 0.8],  # Low similarity
        )
        repository.create_event(event3)
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Red Sea update",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            entity_names=["red sea", "container shipping"],
            normalized_entities=["red sea", "container shipping"],
            occurred_at=now,
            detected_at=now,
            embedding=[0.9, 0.1, 0.0],
        )
        
        matches = find_candidate_matches(candidate, repository, now, config)
        
        # EVT_001 should have higher score than EVT_003
        assert len(matches) == 2
        assert matches[0].event.event_id == "EVT_001"
        assert matches[0].total_score > matches[1].total_score
    
    def test_region_priority(self, repository):
        """Should prioritize same region."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        config = DEFAULT_RESOLUTION_CONFIG
        
        candidate = EventCandidate(
            candidate_id="CAND_001",
            source_id="SRC_001",
            title="Shipping update",
            summary="Update",
            event_type="shipping_disruption",
            region="Middle East",
            country_codes=[],
            entity_names=[],
            normalized_entities=[],
            occurred_at=now,
            detected_at=now,
            embedding=[0.9, 0.1, 0.0],
        )
        
        matches = find_candidate_matches(candidate, repository, now, config)
        
        # Should find EVT_001 (Middle East)
        assert len(matches) >= 1
