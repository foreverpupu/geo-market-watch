"""
Unit tests for signal bucketing.
"""

import pytest
from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.enums import SignalClass
from v2.services.signal_bucketing import classify_signal


class TestClassifySignal:
    """Test classify_signal function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_RANKING_CONFIG
    
    def test_major_shock(self, config):
        """Should classify >= 0.80 as major_shock."""
        result = classify_signal(0.85, config)
        assert result == SignalClass.MAJOR_SHOCK.value
    
    def test_high_priority(self, config):
        """Should classify >= 0.65 as high_priority."""
        result = classify_signal(0.70, config)
        assert result == SignalClass.HIGH_PRIORITY.value
    
    def test_watchlist_upgrade(self, config):
        """Should classify >= 0.50 as watchlist_upgrade."""
        result = classify_signal(0.55, config)
        assert result == SignalClass.WATCHLIST_UPGRADE.value
    
    def test_monitor(self, config):
        """Should classify >= 0.35 as monitor."""
        result = classify_signal(0.40, config)
        assert result == SignalClass.MONITOR.value
    
    def test_low_signal(self, config):
        """Should classify < 0.35 as low_signal."""
        result = classify_signal(0.20, config)
        assert result == SignalClass.LOW_SIGNAL.value
    
    def test_boundary_major_shock(self, config):
        """Should handle boundary at 0.80."""
        result = classify_signal(0.80, config)
        assert result == SignalClass.MAJOR_SHOCK.value
    
    def test_boundary_high_priority(self, config):
        """Should handle boundary at 0.65."""
        result = classify_signal(0.65, config)
        assert result == SignalClass.HIGH_PRIORITY.value
