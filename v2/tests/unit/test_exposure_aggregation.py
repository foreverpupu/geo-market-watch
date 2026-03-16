"""
Unit tests for exposure aggregation.
"""

from datetime import datetime

import pytest
from v2.config import DEFAULT_EXPOSURE_CONFIG
from v2.domain.enums import ExposureDirection, ExposureSourceType
from v2.domain.models import ExposureCandidate, ExposureTraceStep
from v2.services.exposure_aggregation import aggregate_exposures, summarize_net_exposures


class TestAggregateExposures:
    """Test aggregate_exposures function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_EXPOSURE_CONFIG
    
    @pytest.fixture
    def sample_candidates(self):
        """Create sample exposure candidates."""
        return [
            ExposureCandidate(
                target_type="route",
                target_id="red_sea",
                target_name="Red Sea",
                exposure_channel="logistics_disruption",
                direction=ExposureDirection.NEGATIVE.value,
                score=0.75,
                confidence=0.80,
                horizon="days",
                source_type=ExposureSourceType.DIRECT_RULE.value,
                source_ref="rule1",
                reasoning_trace="direct rule",
                trace_steps=[ExposureTraceStep("direct_rule", "rule1", "event", "route:red_sea", 0.75, 0)],
            ),
            ExposureCandidate(
                target_type="sector",
                target_id="container_shipping",
                target_name="Container Shipping",
                exposure_channel="pricing_power_shift",
                direction=ExposureDirection.MIXED.value,
                score=0.64,
                confidence=0.65,
                horizon="weeks",
                source_type=ExposureSourceType.DIRECT_RULE.value,
                source_ref="rule2",
                reasoning_trace="direct rule",
                trace_steps=[ExposureTraceStep("direct_rule", "rule2", "event", "sector:container_shipping", 0.64, 0)],
            ),
        ]
    
    def test_aggregates_by_target(self, sample_candidates, config):
        """Should aggregate by target."""
        from v2.domain.models import CanonicalEvent
        
        event = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Test",
            event_type="shipping_disruption",
            region="test",
            country_codes=[],
            normalized_entities=[],
            first_seen_at=datetime.now(),
            last_seen_at=datetime.now(),
            occurred_at_start=None,
            occurred_at_end=None,
            status="active",
            phase="warning",
            evidence_count=1,
        )
        
        exposures = aggregate_exposures(event, sample_candidates, config)
        
        # Should have 2 exposures (different targets)
        assert len(exposures) == 2
    
    def test_combines_scores(self, config):
        """Should combine scores using conservative formula."""
        from v2.domain.models import CanonicalEvent
        
        # Two candidates for same target
        candidates = [
            ExposureCandidate(
                target_type="route",
                target_id="red_sea",
                target_name="Red Sea",
                exposure_channel="logistics_disruption",
                direction=ExposureDirection.NEGATIVE.value,
                score=0.40,
                confidence=0.70,
                horizon="days",
                source_type=ExposureSourceType.DIRECT_RULE.value,
                source_ref="rule1",
                reasoning_trace="path1",
                trace_steps=[],
            ),
            ExposureCandidate(
                target_type="route",
                target_id="red_sea",
                target_name="Red Sea",
                exposure_channel="logistics_disruption",
                direction=ExposureDirection.NEGATIVE.value,
                score=0.30,
                confidence=0.60,
                horizon="days",
                source_type=ExposureSourceType.DIRECT_RULE.value,
                source_ref="rule2",
                reasoning_trace="path2",
                trace_steps=[],
            ),
        ]
        
        event = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Test",
            event_type="shipping_disruption",
            region="test",
            country_codes=[],
            normalized_entities=[],
            first_seen_at=datetime.now(),
            last_seen_at=datetime.now(),
            occurred_at_start=None,
            occurred_at_end=None,
            status="active",
            phase="warning",
            evidence_count=1,
        )
        
        exposures = aggregate_exposures(event, candidates, config)
        
        # Should have 1 exposure (same target)
        assert len(exposures) == 1
        
        # Score should be 1 - (1-0.4)*(1-0.3) = 0.58
        expected_score = 1 - (1 - 0.4) * (1 - 0.3)
        assert abs(exposures[0].magnitude_score - expected_score) < 0.01


class TestSummarizeNetExposures:
    """Test summarize_net_exposures function."""
    
    def test_net_negative(self):
        """Should calculate net negative exposure."""
        from v2.domain.models import Exposure
        
        exposures = [
            Exposure(
                exposure_id="EXP_001",
                event_id="EVT_001",
                target_type="route",
                target_id="red_sea",
                target_name="Red Sea",
                exposure_channel="logistics_disruption",
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
        
        summaries = summarize_net_exposures(exposures)
        
        assert len(summaries) == 1
        assert summaries[0].net_direction == ExposureDirection.NEGATIVE.value
        assert summaries[0].negative_score == 0.75
        assert summaries[0].positive_score == 0.0
    
    def test_mixed_direction(self):
        """Should detect mixed direction."""
        from v2.domain.models import Exposure
        
        exposures = [
            Exposure(
                exposure_id="EXP_001",
                event_id="EVT_001",
                target_type="sector",
                target_id="container_shipping",
                target_name="Container Shipping",
                exposure_channel="pricing_power_shift",
                direction=ExposureDirection.MIXED.value,
                magnitude_score=0.64,
                confidence_score=0.65,
                horizon="weeks",
                source_type="direct_rule",
                source_ref="rule1",
                reasoning_trace="test",
                trace_steps=[],
            ),
        ]
        
        summaries = summarize_net_exposures(exposures)
        
        # Mixed contributes to both sides
        assert summaries[0].positive_score > 0
        assert summaries[0].negative_score > 0
        # Net should be close to 0
        assert abs(summaries[0].net_score) < 0.1
