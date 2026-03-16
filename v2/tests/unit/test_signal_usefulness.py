"""
Unit tests for signal usefulness metrics.
"""

from datetime import datetime

import pytest
from v2.config import DEFAULT_REPLAY_CONFIG
from v2.domain.enums import EventTypeCategory, SignalUsefulnessRating
from v2.domain.models import EventTimeline, Signal
from v2.services.signal_usefulness import (
    calculate_usefulness_score,
    classify_event_category,
    determine_usefulness_rating,
    evaluate_signal_usefulness,
)


class TestClassifyEventCategory:
    """Test classify_event_category function."""
    
    def test_classifies_directionality_events(self):
        """Should classify directionality events."""
        assert classify_event_category("tariff") == EventTypeCategory.DIRECTIONALITY.value
        assert classify_event_category("sanction") == EventTypeCategory.DIRECTIONALITY.value
    
    def test_classifies_volatility_events(self):
        """Should classify volatility events."""
        assert classify_event_category("military_strike") == EventTypeCategory.VOLATILITY.value
        assert classify_event_category("military_exercise") == EventTypeCategory.VOLATILITY.value
    
    def test_defaults_to_volatility(self):
        """Should default to volatility for unknown types."""
        assert classify_event_category("unknown_event") == EventTypeCategory.VOLATILITY.value


class TestCalculateUsefulnessScore:
    """Test calculate_usefulness_score function."""
    
    def test_false_alarm_gets_zero(self):
        """False alarm should get 0 score."""
        score = calculate_usefulness_score(30, 0.01, True)
        assert score == 0.0
    
    def test_ideal_lead_time_gets_high_score(self):
        """Ideal lead time (15-60 min) should get high score."""
        score = calculate_usefulness_score(30, 0.005, False)
        assert score >= 0.7
    
    def test_short_lead_time_gets_lower_score(self):
        """Short lead time (< 15 min) should get lower score."""
        score_short = calculate_usefulness_score(10, 0.005, False)
        score_ideal = calculate_usefulness_score(30, 0.005, False)
        assert score_short < score_ideal


class TestDetermineUsefulnessRating:
    """Test determine_usefulness_rating function."""
    
    def test_high_rating(self):
        """Score >= 0.70 should be high."""
        assert determine_usefulness_rating(0.75) == SignalUsefulnessRating.HIGH.value
    
    def test_medium_rating(self):
        """Score >= 0.50 should be medium."""
        assert determine_usefulness_rating(0.60) == SignalUsefulnessRating.MEDIUM.value
    
    def test_low_rating(self):
        """Score >= 0.30 should be low."""
        assert determine_usefulness_rating(0.40) == SignalUsefulnessRating.LOW.value
    
    def test_false_alarm_rating(self):
        """Score < 0.30 should be false_alarm."""
        assert determine_usefulness_rating(0.20) == SignalUsefulnessRating.FALSE_ALARM.value


class TestEvaluateSignalUsefulness:
    """Test evaluate_signal_usefulness function."""
    
    @pytest.fixture
    def base_signal(self):
        return Signal(
            signal_id="SIG_001",
            event_id="EVT_shipping_001",
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
    
    @pytest.fixture
    def base_timeline(self):
        return EventTimeline(
            event_id="EVT_001",
            signal_generated_at=datetime(2024, 1, 15, 12, 0, 0),
            price_points_before=[],
            price_points_after=[],
            market_reaction_detected_at=datetime(2024, 1, 15, 12, 15, 0),
            market_move_direction="up",
            market_move_magnitude=0.05,
        )
    
    def test_evaluates_signal(self, base_signal, base_timeline):
        """Should evaluate signal usefulness."""
        config = DEFAULT_REPLAY_CONFIG
        
        metrics = evaluate_signal_usefulness(base_signal, base_timeline, 15, config)
        
        assert metrics.signal_id == "SIG_001"
        assert metrics.lead_time_minutes == 15
        assert not metrics.is_false_alarm
        assert metrics.event_category in ["directionality", "volatility"]
    
    def test_detects_false_alarm(self, base_signal):
        """Should detect false alarm when no market reaction."""
        config = DEFAULT_REPLAY_CONFIG
        
        timeline = EventTimeline(
            event_id="EVT_001",
            signal_generated_at=datetime(2024, 1, 15, 12, 0, 0),
            price_points_before=[],
            price_points_after=[],
            market_reaction_detected_at=None,
            market_move_direction="neutral",
            market_move_magnitude=0.0,
        )
        
        metrics = evaluate_signal_usefulness(base_signal, timeline, None, config)
        
        assert metrics.is_false_alarm
        assert metrics.usefulness_rating == SignalUsefulnessRating.FALSE_ALARM.value
