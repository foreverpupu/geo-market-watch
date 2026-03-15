"""
Engine Core Logic Tests

Comprehensive tests for engine layer business logic.
"""

import unittest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestEventNormalization(unittest.TestCase):
    """Test event normalization logic."""
    
    def test_normalize_valid_event(self):
        """Valid event should normalize successfully."""
        from engine.intake_normalizer import normalize_event
        
        raw = {
            "headline": "Red Sea shipping disruption",
            "source": "FT",
            "timestamp": "2026-03-15T08:00:00Z"
        }
        
        result = normalize_event(raw)
        
        self.assertIsNotNone(result)
        self.assertIn("event_id", result)
        self.assertEqual(result["category"], "shipping")
        self.assertEqual(result["region"], "Middle East")
    
    def test_normalize_missing_required_fields(self):
        """Missing required fields should raise error."""
        from engine.intake_normalizer import normalize_event
        
        raw = {"source": "FT"}  # Missing headline
        
        with self.assertRaises(ValueError):
            normalize_event(raw)
    
    def test_normalize_deterministic_output(self):
        """Same input should produce same output."""
        from engine.intake_normalizer import normalize_event
        
        raw = {
            "headline": "Test event",
            "source": "Test",
            "timestamp": "2026-03-15T08:00:00Z"
        }
        
        result1 = normalize_event(raw)
        result2 = normalize_event(raw)
        
        self.assertEqual(result1["category"], result2["category"])
        self.assertEqual(result1["region"], result2["region"])


class TestDedupeLogic(unittest.TestCase):
    """Test deduplication logic."""
    
    def test_identical_events_detected(self):
        """Identical events should be flagged as duplicates."""
        from engine.dedupe_memory import check_duplicate
        
        event1 = {"headline": "Same headline", "timestamp": "2026-03-15T08:00:00Z"}
        event2 = {"headline": "Same headline", "timestamp": "2026-03-15T08:00:00Z"}
        
        # First event is new
        is_dup1, reason1 = check_duplicate(event1, memory={})
        self.assertFalse(is_dup1)
        
        # Second event is duplicate
        memory = {"hash_abc": event1}
        is_dup2, reason2 = check_duplicate(event2, memory=memory)
        self.assertTrue(is_dup2)
        self.assertIn("duplicate", reason2.lower())
    
    def test_different_events_not_duplicate(self):
        """Different events should not be flagged."""
        from engine.dedupe_memory import check_duplicate
        
        event1 = {"headline": "Event A", "timestamp": "2026-03-15T08:00:00Z"}
        event2 = {"headline": "Event B", "timestamp": "2026-03-15T08:00:00Z"}
        
        memory = {"hash_abc": event1}
        is_dup, reason = check_duplicate(event2, memory=memory)
        
        self.assertFalse(is_dup)


class TestScoringEngine(unittest.TestCase):
    """Test scoring engine logic."""
    
    def test_shipping_disruption_high_score(self):
        """Shipping disruption should score high (7-9)."""
        from engine.scoring_engine import compute_score
        
        event = {
            "category": "shipping",
            "severity": "high",
            "scope": "global"
        }
        
        score = compute_score(event)
        
        self.assertGreaterEqual(score, 7)
        self.assertLessEqual(score, 9)
    
    def test_score_within_valid_range(self):
        """All scores should be 0-10."""
        from engine.scoring_engine import compute_score
        
        test_cases = [
            {"category": "shipping", "severity": "high"},
            {"category": "conflict", "severity": "medium"},
            {"category": "election", "severity": "low"}
        ]
        
        for event in test_cases:
            score = compute_score(event)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 10)
    
    def test_score_deterministic(self):
        """Same input should produce same score."""
        from engine.scoring_engine import compute_score
        
        event = {"category": "shipping", "severity": "high"}
        
        score1 = compute_score(event)
        score2 = compute_score(event)
        
        self.assertEqual(score1, score2)


class TestEscalationTrigger(unittest.TestCase):
    """Test escalation trigger logic."""
    
    def test_high_score_triggers_analysis(self):
        """Score >= 7 should trigger full analysis."""
        from engine.trigger_engine import should_escalate
        
        should_esc, reason = should_escalate(score=8)
        
        self.assertTrue(should_esc)
        self.assertIsNotNone(reason)
    
    def test_low_score_monitors_only(self):
        """Score < 5 should not trigger."""
        from engine.trigger_engine import should_escalate
        
        should_esc, reason = should_escalate(score=3)
        
        self.assertFalse(should_esc)
    
    def test_medium_score_context_dependent(self):
        """Medium scores (5-6) depend on context."""
        from engine.trigger_engine import should_escalate
        
        # With high severity context
        should_esc, _ = should_escalate(score=6, context={"severity": "high"})
        self.assertTrue(should_esc)
        
        # Without context
        should_esc, _ = should_escalate(score=6)
        self.assertFalse(should_esc)


class TestLifecycleManagement(unittest.TestCase):
    """Test lifecycle state management."""
    
    def test_valid_state_transitions(self):
        """Valid transitions should succeed."""
        from engine.status_rules import validate_status_transition
        
        # Valid transitions
        valid_cases = [
            ("pending_review", "approved"),
            ("pending_review", "rejected"),
            ("approved", "invalidated"),
            ("approved", "closed")
        ]
        
        for old, new in valid_cases:
            is_valid, error = validate_status_transition(old, new)
            self.assertTrue(is_valid, f"{old} -> {new} should be valid")
    
    def test_invalid_state_transitions_blocked(self):
        """Invalid transitions should be blocked."""
        from engine.status_rules import validate_status_transition
        
        # Invalid transitions
        invalid_cases = [
            ("rejected", "approved"),
            ("closed", "approved"),
            ("invalidated", "closed")
        ]
        
        for old, new in invalid_cases:
            is_valid, error = validate_status_transition(old, new)
            self.assertFalse(is_valid, f"{old} -> {new} should be invalid")


class TestPerformanceCalculation(unittest.TestCase):
    """Test performance calculation logic."""
    
    def test_long_return_calculation(self):
        """Long position return calculation."""
        from engine.performance_engine import _calculate_return
        
        ret = _calculate_return("long", entry_price=100, close_price=115)
        
        self.assertEqual(ret, 15.0)  # (115-100)/100 * 100
    
    def test_short_return_calculation(self):
        """Short position return calculation."""
        from engine.performance_engine import _calculate_return
        
        ret = _calculate_return("short", entry_price=100, close_price=85)
        
        self.assertEqual(ret, 15.0)  # (100-85)/100 * 100
    
    def test_outcome_classification(self):
        """Return classification into outcome buckets."""
        from engine.performance_engine import _classify_outcome
        
        test_cases = [
            (15.0, "strong_positive"),
            (7.0, "positive"),
            (2.0, "flat"),
            (-7.0, "negative"),
            (-15.0, "strong_negative")
        ]
        
        for ret, expected in test_cases:
            outcome = _classify_outcome(ret)
            self.assertEqual(outcome, expected)


class TestDatabaseOperations(unittest.TestCase):
    """Test database layer operations."""
    
    def test_database_connection(self):
        """Should connect to SQLite database."""
        from engine.database import connect_db
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            conn = connect_db(db_path)
            self.assertIsNotNone(conn)
            conn.close()
        finally:
            os.unlink(db_path)
    
    def test_event_insertion_and_retrieval(self):
        """Should insert and retrieve events."""
        from engine.database import connect_db
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            conn = connect_db(db_path)
            cursor = conn.cursor()
            
            # Create test table
            cursor.execute('''
                CREATE TABLE test_events (
                    event_id TEXT PRIMARY KEY,
                    headline TEXT
                )
            ''')
            
            # Insert
            cursor.execute(
                "INSERT INTO test_events VALUES (?, ?)",
                ("evt_001", "Test event")
            )
            conn.commit()
            
            # Retrieve
            cursor.execute("SELECT * FROM test_events WHERE event_id = ?", ("evt_001",))
            row = cursor.fetchone()
            
            self.assertIsNotNone(row)
            self.assertEqual(row["headline"], "Test event")
            
            conn.close()
        finally:
            os.unlink(db_path)


def run_all_tests():
    """Run all engine tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEventNormalization))
    suite.addTests(loader.loadTestsFromTestCase(TestDedupeLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestScoringEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEscalationTrigger))
    suite.addTests(loader.loadTestsFromTestCase(TestLifecycleManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperations))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
