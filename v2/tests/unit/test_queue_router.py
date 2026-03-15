"""
Unit tests for queue router.
"""

import pytest
from datetime import datetime
from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.models import CanonicalEvent, Exposure, NetExposureSummary
from v2.domain.enums import EventStatus, EventPhase, SignalClass, QueueType, ExposureDirection
from v2.services.queue_router import assign_signal_queue


class TestAssignSignalQueue:
    """Test assign_signal_queue function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_RANKING_CONFIG
    
    @pytest.fixture
    def base_event(self):
        return CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Test",
            event_type="shipping_disruption",
            region="test",
            country_codes=[],
            normalized_entities=[],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
        )
    
    @pytest.fixture
    def base_exposures(self):
        return []
    
    def test_watchlist_priority(self, base_event, base_exposures, config):
        """Should route to watchlist if watchlist_matches provided."""
        watchlist_matches = [{"weight": 0.5}]
        
        queue = assign_signal_queue(
            base_event, SignalClass.HIGH_PRIORITY.value, base_exposures,
            watchlist_matches=watchlist_matches, config=config
        )
        
        assert queue == QueueType.WATCHLIST.value
    
    def test_conflict_queue_for_mixed_exposure(self, base_event, base_exposures, config):
        """Should route to conflict for mixed exposure with small gap."""
        net_exposures = [
            NetExposureSummary(
                target_type="sector",
                target_id="test",
                target_name="Test",
                net_direction=ExposureDirection.MIXED.value,
                net_score=0.10,
                positive_score=0.40,
                negative_score=0.35,
                confidence=0.70,
                contributing_sources=["direct"],
                reasoning_summary="mixed",
            ),
        ]
        
        queue = assign_signal_queue(
            base_event, SignalClass.MONITOR.value, base_exposures,
            net_exposures=net_exposures, config=config
        )
        
        assert queue == QueueType.CONFLICT.value
    
    def test_triage_for_major_shock(self, base_event, base_exposures, config):
        """Should route to triage for major_shock."""
        queue = assign_signal_queue(
            base_event, SignalClass.MAJOR_SHOCK.value, base_exposures, config=config
        )
        
        assert queue == QueueType.TRIAGE.value
    
    def test_active_event_for_active_status(self, base_event, base_exposures, config):
        """Should route to active_event for active status."""
        base_event.status = EventStatus.ACTIVE.value
        
        queue = assign_signal_queue(
            base_event, SignalClass.WATCHLIST_UPGRADE.value, base_exposures, config=config
        )
        
        assert queue == QueueType.ACTIVE_EVENT.value
    
    def test_postmortem_for_resolved(self, base_event, base_exposures, config):
        """Should route to postmortem for resolved status."""
        base_event.status = "resolved"
        
        queue = assign_signal_queue(
            base_event, SignalClass.LOW_SIGNAL.value, base_exposures, config=config
        )
        
        assert queue == QueueType.POSTMORTEM.value
    
    def test_default_triage(self, base_event, base_exposures, config):
        """Should default to triage."""
        queue = assign_signal_queue(
            base_event, SignalClass.LOW_SIGNAL.value, base_exposures, config=config
        )
        
        assert queue == QueueType.TRIAGE.value
