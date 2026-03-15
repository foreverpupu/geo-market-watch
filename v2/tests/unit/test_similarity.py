"""
Unit tests for similarity scoring.
"""

import pytest
import math
from datetime import datetime, timedelta
from v2.services.similarity import (
    cosine_similarity,
    entity_overlap_score,
    time_window_score,
    combined_match_score,
)


class TestCosineSimilarity:
    """Test cosine_similarity function."""
    
    def test_identical_vectors(self):
        """Identical vectors should have similarity 1.0."""
        vec = [1.0, 0.0, 0.0]
        assert cosine_similarity(vec, vec) == 1.0
    
    def test_orthogonal_vectors(self):
        """Orthogonal vectors should have similarity 0.0."""
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [0.0, 1.0, 0.0]
        assert cosine_similarity(vec_a, vec_b) == 0.0
    
    def test_empty_vectors(self):
        """Empty vectors should return 0.0."""
        assert cosine_similarity(None, [1.0, 0.0]) == 0.0
        assert cosine_similarity([1.0, 0.0], None) == 0.0
        assert cosine_similarity(None, None) == 0.0
    
    def test_length_mismatch(self):
        """Should raise ValueError for length mismatch."""
        with pytest.raises(ValueError):
            cosine_similarity([1.0, 0.0], [1.0, 0.0, 0.0])
    
    def test_negative_clamped(self):
        """Negative similarity should be clamped to 0.0."""
        vec_a = [1.0, 0.0]
        vec_b = [-1.0, 0.0]
        result = cosine_similarity(vec_a, vec_b)
        assert result == 0.0


class TestEntityOverlapScore:
    """Test entity_overlap_score function."""
    
    def test_identical_sets(self):
        """Identical sets should have overlap 1.0."""
        entities = ["red sea", "houthis"]
        assert entity_overlap_score(entities, entities) == 1.0
    
    def test_no_overlap(self):
        """No overlap should return 0.0."""
        a = ["red sea"]
        b = ["panama canal"]
        assert entity_overlap_score(a, b) == 0.0
    
    def test_partial_overlap(self):
        """Partial overlap should return correct Jaccard."""
        a = ["red sea", "houthis", "shipping"]
        b = ["red sea", "suez canal", "shipping"]
        # intersection = 2, union = 4, Jaccard = 0.5
        assert entity_overlap_score(a, b) == 0.5
    
    def test_both_empty(self):
        """Both empty should return 0.0."""
        assert entity_overlap_score([], []) == 0.0
    
    def test_one_empty(self):
        """One empty should return 0.0."""
        assert entity_overlap_score(["red sea"], []) == 0.0
        assert entity_overlap_score([], ["red sea"]) == 0.0


class TestTimeWindowScore:
    """Test time_window_score function."""
    
    def test_within_window(self):
        """Time within window should return 1.0."""
        candidate_time = datetime(2024, 1, 15, 12, 0, 0)
        event_last_seen = datetime(2024, 1, 15, 10, 0, 0)
        assert time_window_score(candidate_time, event_last_seen, 30) == 1.0
    
    def test_outside_window(self):
        """Time outside window should return 0.0."""
        candidate_time = datetime(2024, 1, 15, 12, 0, 0)
        event_last_seen = datetime(2023, 12, 1, 10, 0, 0)  # > 30 days
        assert time_window_score(candidate_time, event_last_seen, 30) == 0.0
    
    def test_none_candidate_time(self):
        """None candidate_time should return 1.0."""
        event_last_seen = datetime(2024, 1, 15, 10, 0, 0)
        assert time_window_score(None, event_last_seen, 30) == 1.0
    
    def test_exactly_at_window_boundary(self):
        """Exactly at boundary should return 1.0."""
        event_last_seen = datetime(2024, 1, 1, 12, 0, 0)
        candidate_time = datetime(2024, 1, 31, 12, 0, 0)  # Exactly 30 days
        assert time_window_score(candidate_time, event_last_seen, 30) == 1.0


class TestCombinedMatchScore:
    """Test combined_match_score function."""
    
    def test_default_weights(self):
        """Test with default weights."""
        score = combined_match_score(
            embedding_similarity=1.0,
            entity_overlap=1.0,
            time_score=1.0,
        )
        # 0.55 * 1.0 + 0.30 * 1.0 + 0.15 * 1.0 = 1.0
        assert score == 1.0
    
    def test_zero_scores(self):
        """All zeros should return 0.0."""
        score = combined_match_score(0.0, 0.0, 0.0)
        assert score == 0.0
    
    def test_custom_weights(self):
        """Test with custom weights."""
        score = combined_match_score(
            embedding_similarity=1.0,
            entity_overlap=0.5,
            time_score=0.0,
            embedding_weight=0.5,
            entity_weight=0.5,
            time_weight=0.0,
        )
        # 0.5 * 1.0 + 0.5 * 0.5 + 0.0 * 0.0 = 0.75
        assert score == 0.75
