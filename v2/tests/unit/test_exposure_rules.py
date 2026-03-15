"""
Unit tests for exposure rules.
"""

import pytest
from datetime import datetime
from v2.config import ExposureConfig, DEFAULT_EXPOSURE_CONFIG
from v2.domain.models import CanonicalEvent
from v2.domain.enums import EventStatus, EventPhase, ExposureDirection, ExposureChannel
from v2.services.exposure_rules import compute_direct_exposures


class TestShippingDisruptionRule:
    """Test shipping_disruption direct exposure rule."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_EXPOSURE_CONFIG
    
    @pytest.fixture
    def shipping_event(self):
        return CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Red Sea shipping disruption",
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
            evidence_count=1,
        )
    
    def test_creates_route_exposure(self, shipping_event, config):
        """Should create route exposure."""
        exposures = compute_direct_exposures(shipping_event, config)
        
        route_exps = [e for e in exposures if e.target_type == "route"]
        assert len(route_exps) >= 1
        
        route_exp = route_exps[0]
        assert route_exp.direction == ExposureDirection.NEGATIVE.value
        assert route_exp.exposure_channel == ExposureChannel.LOGISTICS_DISRUPTION.value
        assert route_exp.score == config.direct_exposure_base_score
    
    def test_creates_sector_exposure(self, shipping_event, config):
        """Should create container shipping sector exposure."""
        exposures = compute_direct_exposures(shipping_event, config)
        
        sector_exps = [e for e in exposures if e.target_id == "container_shipping"]
        assert len(sector_exps) == 1
        
        sector_exp = sector_exps[0]
        assert sector_exp.direction == ExposureDirection.MIXED.value
        assert sector_exp.exposure_channel == ExposureChannel.PRICING_POWER_SHIFT.value
    
    def test_creates_theme_exposure(self, shipping_event, config):
        """Should create import supply chain theme exposure."""
        exposures = compute_direct_exposures(shipping_event, config)
        
        theme_exps = [e for e in exposures if e.target_id == "import_supply_chain"]
        assert len(theme_exps) == 1
        
        theme_exp = theme_exps[0]
        assert theme_exp.direction == ExposureDirection.NEGATIVE.value
    
    def test_has_trace_steps(self, shipping_event, config):
        """Each exposure should have trace steps."""
        exposures = compute_direct_exposures(shipping_event, config)
        
        for exp in exposures:
            assert len(exp.trace_steps) >= 1
            assert exp.trace_steps[0].step_type == "direct_rule"
            assert exp.trace_steps[0].hop_count == 0


class TestExportControlRule:
    """Test export_control direct exposure rule."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_EXPOSURE_CONFIG
    
    @pytest.fixture
    def export_event(self):
        return CanonicalEvent(
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
            evidence_count=1,
        )
    
    def test_creates_commodity_exposure(self, export_event, config):
        """Should create commodity exposure."""
        exposures = compute_direct_exposures(export_event, config)
        
        commodity_exps = [e for e in exposures if e.target_type == "commodity"]
        assert len(commodity_exps) >= 1
        
        commodity_exp = commodity_exps[0]
        assert commodity_exp.target_id == "gallium"
        assert commodity_exp.direction == ExposureDirection.NEGATIVE.value
    
    def test_creates_country_exposure(self, export_event, config):
        """Should create country exposure."""
        exposures = compute_direct_exposures(export_event, config)
        
        country_exps = [e for e in exposures if e.target_type == "country"]
        assert len(country_exps) >= 1


class TestSanctionRule:
    """Test sanction direct exposure rule."""
    
    def test_creates_country_and_theme_exposures(self):
        """Should create country and theme exposures."""
        event = CanonicalEvent(
            event_id="EVT_003",
            cluster_id="CLUSTER_003",
            canonical_title="New sanctions on Russia",
            event_type="sanction",
            region="Eastern Europe",
            country_codes=["RU"],
            normalized_entities=["russia", "sanctions"],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.IMPLEMENTATION.value,
            evidence_count=1,
        )
        
        exposures = compute_direct_exposures(event, DEFAULT_EXPOSURE_CONFIG)
        
        # Should have country exposure
        country_exps = [e for e in exposures if e.target_type == "country"]
        assert len(country_exps) >= 1
        
        # Should have sanctions_risk theme
        theme_exps = [e for e in exposures if e.target_id == "sanctions_risk"]
        assert len(theme_exps) >= 1


class TestLaborStrikeRule:
    """Test labor_strike direct exposure rule."""
    
    def test_creates_facility_and_sector_exposures(self):
        """Should create facility and sector exposures."""
        event = CanonicalEvent(
            event_id="EVT_004",
            cluster_id="CLUSTER_004",
            canonical_title="Port of Montreal strike",
            event_type="labor_strike",
            region="North America",
            country_codes=["CA"],
            normalized_entities=["port of montreal", "labor union"],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.ACTIVE.value,
            phase=EventPhase.IMPLEMENTATION.value,
            evidence_count=1,
        )
        
        exposures = compute_direct_exposures(event, DEFAULT_EXPOSURE_CONFIG)
        
        # Should have facility exposure
        facility_exps = [e for e in exposures if e.target_type == "facility"]
        assert len(facility_exps) >= 1
        
        # Should have logistics sector exposure
        sector_exps = [e for e in exposures if e.target_id == "logistics"]
        assert len(sector_exps) >= 1


class TestGenericRule:
    """Test generic rule for unhandled event types."""
    
    def test_creates_generic_exposure(self):
        """Should create generic exposure for unknown event types."""
        event = CanonicalEvent(
            event_id="EVT_005",
            cluster_id="CLUSTER_005",
            canonical_title="Unknown event type",
            event_type="unknown_type",
            region="Global",
            country_codes=[],
            normalized_entities=["test"],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
        )
        
        exposures = compute_direct_exposures(event, DEFAULT_EXPOSURE_CONFIG)
        
        # Should create at least one generic exposure
        assert len(exposures) >= 1
        
        # Score should be lower than specific rules
        for exp in exposures:
            assert exp.score <= DEFAULT_EXPOSURE_CONFIG.direct_exposure_base_score * 0.60
