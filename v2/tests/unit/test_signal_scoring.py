"""
Unit tests for signal scoring.
"""

import pytest
from v2.config import DEFAULT_RANKING_CONFIG
from v2.domain.models import RankingFeatureSet
from v2.services.signal_scoring import compute_signal_score


class TestComputeSignalScore:
    """Test compute_signal_score function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_RANKING_CONFIG
    
    @pytest.fixture
    def base_features(self):
        return RankingFeatureSet(
            severity_score=0.70,
            market_relevance_score=0.60,
            novelty_score=0.75,
            confidence_score=0.65,
            breadth_score=0.50,
            urgency_score=0.80,
        )
    
    def test_base_score_calculation(self, base_features, config):
        """Should calculate base score correctly."""
        breakdown = compute_signal_score(base_features, config)
        
        # Expected: 0.22*0.70 + 0.20*0.60 + 0.16*0.75 + 0.14*0.65 + 0.14*0.50 + 0.14*0.80
        expected_base = (
            0.22 * 0.70 +
            0.20 * 0.60 +
            0.16 * 0.75 +
            0.14 * 0.65 +
            0.14 * 0.50 +
            0.14 * 0.80
        )
        
        assert abs(breakdown.base_score - expected_base) < 0.01
    
    def test_watchlist_boost_capped(self, base_features, config):
        """Should cap watchlist boost."""
        base_features.watchlist_match_score = 1.0  # Max match
        
        breakdown = compute_signal_score(base_features, config)
        
        # Should be capped at watchlist_boost_max (0.10)
        assert breakdown.watchlist_boost == config.watchlist_boost_max
    
    def test_penalties_applied(self, base_features, config):
        """Should apply penalties."""
        base_features.duplicate_penalty = 0.10
        base_features.low_evidence_penalty = 0.15
        
        breakdown = compute_signal_score(base_features, config)
        
        assert breakdown.duplicate_penalty == 0.10
        assert breakdown.low_evidence_penalty == 0.15
        
        # Final should be lower than base
        assert breakdown.final_score < breakdown.base_score
    
    def test_final_score_clamped(self, base_features, config):
        """Should clamp final score to [0, 1]."""
        # Set very high penalties to go below 0
        base_features.duplicate_penalty = 1.0
        base_features.low_evidence_penalty = 1.0
        
        breakdown = compute_signal_score(base_features, config)
        
        assert breakdown.final_score == 0.0
    
    def test_formula_trace_generated(self, base_features, config):
        """Should generate formula trace."""
        breakdown = compute_signal_score(base_features, config)
        
        assert "base=" in breakdown.formula_trace
        assert "watchlist_boost=" in breakdown.formula_trace
        assert "final=" in breakdown.formula_trace
    
    def test_feature_contributions(self, base_features, config):
        """Should include feature contributions."""
        breakdown = compute_signal_score(base_features, config)
        
        assert "severity" in breakdown.feature_contributions
        assert "market_relevance" in breakdown.feature_contributions
        assert "novelty" in breakdown.feature_contributions
