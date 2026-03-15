"""
Unit tests for replay core.
"""

import pytest
from datetime import datetime, timedelta
from v2.config import DEFAULT_REPLAY_CONFIG
from v2.domain.models import Signal, PricePoint
from v2.repositories.price_repository import MockPriceRepository
from v2.services.replay_core import build_event_timeline, calculate_lead_time


class TestBuildEventTimeline:
    """Test build_event_timeline function."""
    
    @pytest.fixture
    def base_signal(self):
        return Signal(
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
            generated_at=datetime(2024, 1, 15, 12, 0, 0),
        )
    
    def test_builds_timeline_with_price_data(self, base_signal):
        """Should build timeline with price data."""
        price_repo = MockPriceRepository()
        config = DEFAULT_REPLAY_CONFIG
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        timeline = build_event_timeline(base_signal, ["SPY"], price_repo, config, now)
        
        assert timeline.event_id == "EVT_001"
        assert len(timeline.price_points_before) > 0
        assert len(timeline.price_points_after) > 0
        assert timeline.signal_generated_at == now
    
    def test_detects_market_reaction(self, base_signal):
        """Should detect market reaction."""
        price_repo = MockPriceRepository()
        config = DEFAULT_REPLAY_CONFIG
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # 注入市场变动
        price_repo.inject_market_move("SPY", now, 30, 0.05)
        
        timeline = build_event_timeline(base_signal, ["SPY"], price_repo, config, now)
        
        assert timeline.market_reaction_detected_at is not None
        assert timeline.market_move_direction in ["up", "down"]
        assert timeline.market_move_magnitude is not None


class TestCalculateLeadTime:
    """Test calculate_lead_time function."""
    
    @pytest.fixture
    def base_signal(self):
        return Signal(
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
            generated_at=datetime(2024, 1, 15, 12, 0, 0),
        )
    
    def test_calculates_lead_time(self, base_signal):
        """Should calculate lead time correctly."""
        from v2.domain.models import EventTimeline
        
        config = DEFAULT_REPLAY_CONFIG
        
        # 市场反应在信号后 15 分钟
        reaction_time = datetime(2024, 1, 15, 12, 15, 0)
        
        timeline = EventTimeline(
            event_id="EVT_001",
            signal_generated_at=base_signal.generated_at,
            price_points_before=[],
            price_points_after=[],
            market_reaction_detected_at=reaction_time,
            market_move_direction="up",
            market_move_magnitude=0.05,
        )
        
        lead_time = calculate_lead_time(base_signal, timeline, config)
        
        assert lead_time == 15
    
    def test_returns_none_if_no_reaction(self, base_signal):
        """Should return None if no market reaction."""
        from v2.domain.models import EventTimeline
        
        config = DEFAULT_REPLAY_CONFIG
        
        timeline = EventTimeline(
            event_id="EVT_001",
            signal_generated_at=base_signal.generated_at,
            price_points_before=[],
            price_points_after=[],
            market_reaction_detected_at=None,
            market_move_direction=None,
            market_move_magnitude=None,
        )
        
        lead_time = calculate_lead_time(base_signal, timeline, config)
        
        assert lead_time is None
