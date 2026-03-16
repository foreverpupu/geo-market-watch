"""
Unit tests for watchlist routing.
"""

from datetime import datetime

import pytest
from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG
from v2.domain.enums import WatchlistStatus
from v2.domain.models import Signal
from v2.repositories.watchlist_repository import InMemoryWatchlistRepository
from v2.services.watchlist_routing import (
    auto_route_high_priority_signals,
    route_signal_to_watchlist,
)


class TestRouteSignalToWatchlist:
    """Test route_signal_to_watchlist function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_ANALYST_WORKFLOW_CONFIG
    
    @pytest.fixture
    def high_priority_signal(self):
        return Signal(
            signal_id="SIG_001",
            event_id="EVT_001",
            signal_class="high_priority",
            rank_score=0.85,  # Above threshold
            severity_score=0.70,
            market_relevance_score=0.80,
            novelty_score=0.75,
            confidence_score=0.68,
            breadth_score=0.60,
            urgency_score=0.90,
            watchlist_match_score=0.0,
            assigned_queue="triage",
            status="generated",
            summary_text="Test",
            reasoning_trace="Test",
            generated_at=datetime(2024, 1, 15, 12, 0, 0),
        )
    
    def test_routes_high_priority_signal(self, high_priority_signal, config):
        """Should route high priority signal to watchlist."""
        repository = InMemoryWatchlistRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        entry = route_signal_to_watchlist(
            high_priority_signal, "analyst_001", "Important signal", config, repository, now
        )
        
        assert entry is not None
        assert entry.signal_id == "SIG_001"
        assert entry.assigned_to == "analyst_001"
        assert entry.status == WatchlistStatus.ACTIVE.value
        assert repository.count() == 1
    
    def test_rejects_low_priority_signal(self, config):
        """Should reject signal below threshold."""
        repository = InMemoryWatchlistRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        low_signal = Signal(
            signal_id="SIG_002",
            event_id="EVT_002",
            signal_class="monitor",
            rank_score=0.40,  # Below threshold
            severity_score=0.50,
            market_relevance_score=0.40,
            novelty_score=0.30,
            confidence_score=0.50,
            breadth_score=0.30,
            urgency_score=0.40,
            watchlist_match_score=0.0,
            assigned_queue="triage",
            status="generated",
            summary_text="Test",
            reasoning_trace="Test",
            generated_at=now,
        )
        
        entry = route_signal_to_watchlist(
            low_signal, "analyst_001", "Low priority", config, repository, now
        )
        
        assert entry is None
    
    def test_enforces_max_watchlist_size(self, high_priority_signal, config):
        """Should enforce max watchlist size."""
        repository = InMemoryWatchlistRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Fill up watchlist
        for i in range(config.max_watchlist_size):
            signal = Signal(
                signal_id=f"SIG_{i:03d}",
                event_id=f"EVT_{i:03d}",
                signal_class="high_priority",
                rank_score=0.85,
                severity_score=0.70,
                market_relevance_score=0.80,
                novelty_score=0.75,
                confidence_score=0.68,
                breadth_score=0.60,
                urgency_score=0.90,
                watchlist_match_score=0.0,
                assigned_queue="triage",
                status="generated",
                summary_text="Test",
                reasoning_trace="Test",
                generated_at=now,
            )
            route_signal_to_watchlist(signal, "analyst_001", "Test", config, repository, now)
        
        # Try to add one more
        with pytest.raises(ValueError):
            route_signal_to_watchlist(
                high_priority_signal, "analyst_001", "Overflow", config, repository, now
            )


class TestAutoRouteHighPrioritySignals:
    """Test auto_route_high_priority_signals function."""
    
    def test_routes_to_multiple_analysts(self):
        """Should route to multiple analysts."""
        config = DEFAULT_ANALYST_WORKFLOW_CONFIG
        repository = InMemoryWatchlistRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        signal = Signal(
            signal_id="SIG_001",
            event_id="EVT_001",
            signal_class="high_priority",
            rank_score=0.85,
            severity_score=0.70,
            market_relevance_score=0.80,
            novelty_score=0.75,
            confidence_score=0.68,
            breadth_score=0.60,
            urgency_score=0.90,
            watchlist_match_score=0.0,
            assigned_queue="triage",
            status="generated",
            summary_text="Test",
            reasoning_trace="Test",
            generated_at=now,
        )
        
        entries = auto_route_high_priority_signals(
            signal, ["analyst_001", "analyst_002", "analyst_003"], config, repository, now
        )
        
        assert len(entries) == 3
        assert repository.count() == 3
