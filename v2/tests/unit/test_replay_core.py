"""
Unit tests for replay core (optimized).
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from v2.config import DEFAULT_REPLAY_CONFIG
from v2.domain.models import Signal
from v2.repositories.price_repository import MockPriceRepository
from v2.services.replay_core import (
    build_event_timeline_optimized,
    calculate_lead_time,
    _detect_market_move_optimized,
)


class TestDetectMarketMoveOptimized:
    """Test _detect_market_move_optimized function."""
    
    def test_detects_with_2sigma(self):
        """Should detect market move using 2-Sigma method."""
        config = DEFAULT_REPLAY_CONFIG
        signal_time = datetime(2024, 1, 15, 12, 0, 0)
        
        # 生成足够的历史数据（> 60 个点）
        timestamps = pd.date_range(start=signal_time - timedelta(hours=2), periods=180, freq="1min")
        prices = pd.Series([100.0 + i * 0.01 for i in range(180)])  # 缓慢上升趋势
        
        # 信号后价格突破 2-Sigma
        prices.iloc[120:] = prices.iloc[120] * 1.05  # 5% jump
        
        result = _detect_market_move_optimized(
            prices, timestamps, signal_time, prices.iloc[119], config
        )
        
        assert result["detected_at"] is not None
        assert result["direction"] == "up"
        assert result["method"] == "2sigma"
    
    def test_uses_fixed_threshold_when_insufficient_data(self):
        """Should use fixed threshold when insufficient historical data."""
        config = DEFAULT_REPLAY_CONFIG
        signal_time = datetime(2024, 1, 15, 12, 0, 0)
        
        # 只有 30 个历史数据点（< 60）
        timestamps = pd.date_range(start=signal_time - timedelta(minutes=30), periods=90, freq="1min")
        prices = pd.Series([100.0] * 30 + [100.0 + i * 0.05 for i in range(60)])  # 后 60 分钟上升
        
        result = _detect_market_move_optimized(
            prices, timestamps, signal_time, 100.0, config
        )
        
        assert result["detected_at"] is not None
        assert result["method"] == "fixed_threshold"
    
    def test_marks_as_neutral_after_24h_no_movement(self):
        """Should mark as neutral if no movement within 24 hours."""
        config = DEFAULT_REPLAY_CONFIG
        signal_time = datetime(2024, 1, 15, 12, 0, 0)
        
        # 生成数据，但价格几乎不变
        timestamps = pd.date_range(start=signal_time - timedelta(hours=2), periods=180, freq="1min")
        prices = pd.Series([100.0 + (i % 10) * 0.001 for i in range(180)])  # 微小波动
        
        result = _detect_market_move_optimized(
            prices, timestamps, signal_time, 100.0, config
        )
        
        assert result["direction"] == "neutral"
        assert result["method"] == "neutral"
        assert result["magnitude"] == 0.0


class TestBuildEventTimelineOptimized:
    """Test build_event_timeline_optimized function."""
    
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
    
    def test_builds_timeline_with_optimized_detection(self, base_signal):
        """Should build timeline with optimized market detection."""
        price_repo = MockPriceRepository()
        config = DEFAULT_REPLAY_CONFIG
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # 注入市场变动
        price_repo.inject_market_move("SPY", now, 30, 0.05)
        
        timeline = build_event_timeline_optimized(base_signal, ["SPY"], price_repo, config, now)
        
        assert timeline.event_id == "EVT_001"
        assert len(timeline.price_points_before) > 0
        assert len(timeline.price_points_after) > 0
        assert timeline.market_reaction_detected_at is not None
        assert timeline.market_move_direction in ["up", "down"]


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
            market_move_direction="neutral",
            market_move_magnitude=0.0,
        )
        
        lead_time = calculate_lead_time(base_signal, timeline, config)
        
        assert lead_time is None
