"""
Integration test for exposure pipeline.
"""

from datetime import datetime

from v2.config import DEFAULT_EXPOSURE_CONFIG
from v2.domain.enums import EventPhase, EventStatus, ExposureDirection
from v2.domain.models import CanonicalEvent
from v2.repositories.exposure_repository import InMemoryExposureRepository
from v2.services.exposure_engine import compute_event_exposures


class TestExposurePipeline:
    """Integration test for full exposure pipeline."""
    
    def test_shipping_disruption_full_pipeline(self):
        """
        Test: Shipping disruption should generate correct exposures.
        
        Event: Red Sea shipping disruption
        Expected:
        - route:red_sea exposure
        - sector:container_shipping exposure
        - theme:import_supply_chain exposure
        - All aggregated correctly
        """
        event = CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Red Sea shipping disruption escalates",
            event_type="shipping_disruption",
            region="red sea",
            country_codes=["EG", "YE"],
            normalized_entities=["red sea", "container shipping", "houthis"],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.ESCALATION.value,
            evidence_count=3,
        )
        
        repository = InMemoryExposureRepository()
        config = DEFAULT_EXPOSURE_CONFIG
        
        result = compute_event_exposures(event, repository, config)
        
        # Should have direct exposures
        assert len(result.direct_exposures) >= 3
        
        # Should have aggregated exposures
        assert len(result.aggregated_exposures) >= 3
        
        # Should have net summaries
        assert len(result.net_exposure_summaries) >= 3
        
        # Check for route exposure
        route_exps = [e for e in result.direct_exposures if e.target_type == "route"]
        assert len(route_exps) >= 1
        assert route_exps[0].direction == ExposureDirection.NEGATIVE.value
        
        # Check for sector exposure
        sector_exps = [e for e in result.direct_exposures if e.target_id == "container_shipping"]
        assert len(sector_exps) >= 1
        
        # Check repository
        assert repository.count(event.event_id) == len(result.aggregated_exposures)
    
    def test_export_control_full_pipeline(self):
        """
        Test: Export control should generate commodity and country exposures.
        """
        event = CanonicalEvent(
            event_id="EVT_002",
            cluster_id="CLUSTER_002",
            canonical_title="China gallium export controls",
            event_type="export_control",
            region="Asia-Pacific",
            country_codes=["CN"],
            normalized_entities=["china", "gallium", "export controls"],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.IMPLEMENTATION.value,
            evidence_count=2,
        )
        
        repository = InMemoryExposureRepository()
        config = DEFAULT_EXPOSURE_CONFIG
        
        result = compute_event_exposures(event, repository, config)
        
        # Should have commodity exposure
        commodity_exps = [e for e in result.direct_exposures if e.target_type == "commodity"]
        assert len(commodity_exps) >= 1
        assert commodity_exps[0].target_id == "gallium"
        
        # Should have country exposure
        country_exps = [e for e in result.direct_exposures if e.target_type == "country"]
        assert len(country_exps) >= 1
