"""
Integration test for ranking pipeline.
"""

from datetime import datetime, timedelta

from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.enums import EventPhase, EventStatus, ExposureChannel, ExposureDirection, SignalClass
from v2.domain.models import CanonicalEvent, Exposure
from v2.repositories.signal_repository import InMemorySignalRepository
from v2.services.signal_engine import generate_signal_for_event


class TestRankingPipeline:
    """Integration test for full ranking pipeline."""
    
    def test_shipping_disruption_high_priority(self):
        """
        Test: Shipping disruption should generate high priority signal.
        
        Event: Red Sea shipping disruption
        Phase: escalation
        Status: active
        Exposures: route, theme, sector
        
        Expected:
        - rank_score >= 0.65
        - signal_class == high_priority
        - queue = triage
        - reasoning_trace contains urgency and exposures
        """
        now = datetime(2024, 1, 15, 12, 0, 0)
        
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
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.ESCALATION.value,
            evidence_count=3,
        )
        
        exposures = [
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
                reasoning_trace="direct",
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
                source_type="template",
                source_ref="tmpl1",
                reasoning_trace="template",
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
                source_ref="rule2",
                reasoning_trace="direct",
                trace_steps=[],
            ),
        ]
        
        repository = InMemorySignalRepository()
        config = DEFAULT_RANKING_CONFIG
        
        result = generate_signal_for_event(
            event=event,
            exposures=exposures,
            signal_repository=repository,
            now=now,
            config=config,
        )
        
        # Verify high priority
        assert result.signal.rank_score >= 0.65
        assert result.signal.signal_class == SignalClass.HIGH_PRIORITY.value
        assert result.signal.assigned_queue == "triage"
        
        # Verify features
        assert result.features.urgency_score >= 0.70  # escalation phase
        assert result.features.market_relevance_score > 0.50
        
        # Verify reasoning
        assert "urgency" in result.signal.reasoning_trace.lower()
        assert "red_sea" in result.signal.reasoning_trace.lower()
        
        # Verify saved
        assert repository.count() == 1
    
    def test_old_low_confidence_strike_low_signal(self):
        """
        Test: Old low-confidence local strike should generate low signal.
        
        Event: Local labor strike
        Phase: warning
        Status: monitoring
        Evidence: 1
        Exposures: single low score
        
        Expected:
        - rank_score < 0.50
        - signal_class == low_signal
        """
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        event = CanonicalEvent(
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
        
        exposures = [
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
                reasoning_trace="direct",
                trace_steps=[],
            ),
        ]
        
        repository = InMemorySignalRepository()
        config = DEFAULT_RANKING_CONFIG
        
        result = generate_signal_for_event(
            event=event,
            exposures=exposures,
            signal_repository=repository,
            now=now,
            config=config,
        )
        
        # Verify low signal
        assert result.signal.rank_score < 0.50
        assert result.signal.signal_class == SignalClass.LOW_SIGNAL.value
        
        # Verify penalties applied
        assert result.features.low_evidence_penalty > 0
        
        # Verify novelty decayed
        assert result.features.novelty_score < 0.50
