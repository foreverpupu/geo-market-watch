"""
Unit tests for ranking features.
"""

import pytest
from datetime import datetime, timedelta
from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.models import CanonicalEvent, Exposure
from v2.domain.enums import EventStatus, EventPhase, ExposureDirection, ExposureChannel
from v2.services.ranking_features import build_ranking_features


class TestBuildRankingFeatures:
    """Test build_ranking_features function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_RANKING_CONFIG
    
    @pytest.fixture
    def base_event(self):
        return CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Test Event",
            event_type="shipping_disruption",
            region="test",
            country_codes=["EG"],
            normalized_entities=["red sea", "shipping"],
            first_seen_at=datetime(2024, 1, 15, 10, 0, 0),
            last_seen_at=datetime(2024, 1, 15, 12, 0, 0),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.ESCALATION.value,
            evidence_count=3,
        )
    
    @pytest.fixture
    def base_exposures(self):
        return [
            Exposure(
                exposure_id="EXP_001",
                event_id="EVT_001",
                target_type="route",
                target_id="red_sea",
                target_name="Red Sea",
                exposure_channel=ExposureChannel.LOGISTICS_DISRUPTION.value,
                direction=ExposureDirection.NEGATIVE.value,
                magnitude_score=0.75,
                confidence_score=0.80,
                horizon="days",
                source_type="direct_rule",
                source_ref="rule1",
                reasoning_trace="test",
                trace_steps=[],
            ),
        ]
    
    def test_severity_from_event_type(self, base_event, base_exposures, config):
        """Should get severity from event_type defaults."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        features = build_ranking_features(base_event, base_exposures, now=now, config=config)
        
        # shipping_disruption default severity is 0.70
        assert features.severity_score == 0.70
    
    def test_market_relevance_calculation(self, base_event, base_exposures, config):
        """Should calculate market relevance."""
        now = datetime(2024, 1, 15, 12, 0, 0)
        features = build_ranking_features(base_event, base_exposures, now=now, config=config)
        
        # Should be > 0 with exposures
        assert features.market_relevance_score > 0
    
    def test_novelty_with_time_decay(self, base_event, base_exposures, config):
        """Should apply time decay to novelty."""
        # Event from 2 hours ago
        base_event.first_seen_at = datetime(2024, 1, 15, 10, 0, 0)
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        features = build_ranking_features(base_event, base_exposures, now=now, config=config)
        
        # Should have decayed from base 0.85
        assert features.novelty_score < 0.85
        assert features.novelty_score >= config.novelty_min_score
    
    def test_urgency_with_escalation_phase(self, base_event, base_exposures, config):
        """Should have higher urgency for escalation phase."""
        base_event.phase = EventPhase.ESCALATION.value
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        features = build_ranking_features(base_event, base_exposures, now=now, config=config)
        
        # Escalation should add 0.20
        assert features.urgency_score >= 0.70  # base 0.50 + 0.20
    
    def test_low_evidence_penalty(self, base_event, base_exposures, config):
        """Should apply penalty for single evidence."""
        base_event.evidence_count = 1
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        features = build_ranking_features(base_event, base_exposures, now=now, config=config)
        
        assert features.low_evidence_penalty == config.low_evidence_penalty
    
    def test_watchlist_match(self, base_event, base_exposures, config):
        """Should calculate watchlist match score."""
        watchlist_matches = [
            {"weight": 0.5},
            {"weight": 0.3},
        ]
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        features = build_ranking_features(
            base_event, base_exposures, watchlist_matches=watchlist_matches, now=now, config=config
        )
        
        # Should sum to 0.8 but cap at 1.0
        assert features.watchlist_match_score == 0.8
