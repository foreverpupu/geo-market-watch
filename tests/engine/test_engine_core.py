"""
Engine Core Logic Tests

Comprehensive tests for engine layer business logic.
"""

import os
import tempfile
import unittest
from datetime import datetime

from geo_market_watch.dedupe_memory import DedupeMemory
from geo_market_watch.intake_normalizer import IntakeNormalizer
from geo_market_watch.models import NormalizedEvent, ScoreResult, TriggerResult
from geo_market_watch.scoring_engine import ScoringEngine
from geo_market_watch.trigger_engine import TriggerEngine


class TestEventNormalization(unittest.TestCase):
    """Test event normalization logic."""
    
    def test_normalize_valid_event(self):
        """Valid event should normalize successfully."""
        normalizer = IntakeNormalizer()
        
        raw = {
            "headline": "Red Sea shipping disruption",
            "source": "FT",
            "timestamp": "2026-03-15T08:00:00Z"
        }
        
        result = normalizer.normalize(raw)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, NormalizedEvent)
        self.assertTrue(result.event_id.startswith("evt_"))
        self.assertEqual(result.category, "shipping")
        self.assertEqual(result.region, "Middle East")
    
    def test_normalize_missing_required_fields(self):
        """Missing required fields should raise error."""
        normalizer = IntakeNormalizer()
        
        raw = {"source": "FT"}  # Missing headline
        
        with self.assertRaises(Exception):
            normalizer.normalize(raw)
    
    def test_normalize_deterministic_output(self):
        """Same input should produce same normalized fields."""
        normalizer = IntakeNormalizer()
        
        raw = {
            "headline": "Test event",
            "source": "Test",
            "timestamp": "2026-03-15T08:00:00Z"
        }
        
        result1 = normalizer.normalize(raw)
        result2 = normalizer.normalize(raw)
        
        self.assertEqual(result1.category, result2.category)
        self.assertEqual(result1.region, result2.region)


class TestDedupeLogic(unittest.TestCase):
    """Test deduplication logic."""
    
    def test_identical_events_detected(self):
        """Identical events should be flagged as duplicates."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{}')
            memory_path = f.name
        
        try:
            memory = DedupeMemory(memory_path)
            
            # Create a normalized event
            event = NormalizedEvent(
                event_id="evt_001",
                headline="Same headline",
                timestamp=datetime.now(),
                region="Middle East",
                category="shipping",
                severity="high",
                canonical_key="same headline"
            )
            
            # First event is new
            is_dup1, reason1 = memory.check_duplicate(event)
            self.assertFalse(is_dup1)
            
            # Second event is duplicate
            is_dup2, reason2 = memory.check_duplicate(event)
            self.assertTrue(is_dup2)
            self.assertIn("match", reason2.lower())
        finally:
            os.unlink(memory_path)
    
    def test_different_events_not_duplicate(self):
        """Different events should not be flagged."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{}')
            memory_path = f.name
        
        try:
            memory = DedupeMemory(memory_path)
            
            event1 = NormalizedEvent(
                event_id="evt_001",
                headline="Major earthquake strikes Japan causing widespread damage",
                timestamp=datetime.now(),
                region="Asia-Pacific",
                category="conflict",
                severity="critical",
                canonical_key="earthquake japan damage"
            )
            
            event2 = NormalizedEvent(
                event_id="evt_002",
                headline="Federal Reserve announces interest rate hike decision",
                timestamp=datetime.now(),
                region="North America",
                category="election",
                severity="medium",
                canonical_key="fed rate hike decision"
            )
            
            # First event is new
            memory.check_duplicate(event1)
            
            # Second event should not be duplicate (completely different)
            is_dup, reason = memory.check_duplicate(event2)
            self.assertFalse(is_dup, f"Expected not duplicate but got: {reason}")
        finally:
            os.unlink(memory_path)


class TestScoringEngine(unittest.TestCase):
    """Test scoring engine logic."""
    
    def test_shipping_disruption_high_score(self):
        """Shipping disruption should score high (7-9)."""
        engine = ScoringEngine()
        
        event = NormalizedEvent(
            event_id="evt_001",
            headline="Shipping disruption",
            timestamp=datetime.now(),
            region="Middle East",
            category="shipping",
            severity="high"
        )
        
        result = engine.compute_score(event)
        
        self.assertIsInstance(result, ScoreResult)
        self.assertGreaterEqual(result.value, 7)
        self.assertLessEqual(result.value, 10)
    
    def test_score_within_valid_range(self):
        """All scores should be 0-10."""
        engine = ScoringEngine()
        
        test_cases = [
            {"category": "shipping", "severity": "high"},
            {"category": "conflict", "severity": "medium"},
            {"category": "election", "severity": "low"}
        ]
        
        for case in test_cases:
            event = NormalizedEvent(
                event_id="evt_001",
                headline="Test",
                timestamp=datetime.now(),
                region="Global",
                category=case["category"],
                severity=case["severity"]
            )
            result = engine.compute_score(event)
            self.assertGreaterEqual(result.value, 0)
            self.assertLessEqual(result.value, 10)
    
    def test_score_deterministic(self):
        """Same input should produce same score."""
        engine = ScoringEngine()
        
        event = NormalizedEvent(
            event_id="evt_001",
            headline="Test",
            timestamp=datetime.now(),
            region="Global",
            category="shipping",
            severity="high"
        )
        
        result1 = engine.compute_score(event)
        result2 = engine.compute_score(event)
        
        self.assertEqual(result1.value, result2.value)


class TestEscalationTrigger(unittest.TestCase):
    """Test escalation trigger logic."""
    
    def test_high_score_triggers_analysis(self):
        """Score >= 7 should trigger full analysis."""
        engine = TriggerEngine()
        
        score_result = ScoreResult(value=8.0, band="high")
        result = engine.should_escalate(score_result)
        
        self.assertIsInstance(result, TriggerResult)
        self.assertTrue(result.trigger_full_analysis)
        self.assertIsNotNone(result.trigger_reasons)
    
    def test_low_score_monitors_only(self):
        """Score < 5 should not trigger."""
        engine = TriggerEngine()
        
        score_result = ScoreResult(value=3.0, band="low")
        result = engine.should_escalate(score_result)
        
        self.assertFalse(result.trigger_full_analysis)
    
    def test_medium_score_context_dependent(self):
        """Medium scores (5-6) depend on context."""
        engine = TriggerEngine()
        
        # With high severity context
        score_result = ScoreResult(value=6.0, band="medium")
        result = engine.should_escalate(score_result, context={"severity": "critical"})
        self.assertTrue(result.trigger_full_analysis)
        
        # Without context
        result = engine.should_escalate(score_result)
        self.assertFalse(result.trigger_full_analysis)


class TestLifecycleManagement(unittest.TestCase):
    """Test lifecycle state management."""
    
    def test_valid_state_transitions(self):
        """Valid transitions should succeed."""
        from geo_market_watch.status_rules import validate_analyst_status_transition
        
        # Valid transitions
        valid_cases = [
            ("pending_review", "approved"),
            ("pending_review", "rejected"),
            ("approved", "invalidated"),
            ("approved", "closed")
        ]
        
        for old, new in valid_cases:
            is_valid, error = validate_analyst_status_transition(old, new)
            self.assertTrue(is_valid, f"{old} -> {new} should be valid")
    
    def test_invalid_state_transitions_blocked(self):
        """Invalid transitions should be blocked."""
        from geo_market_watch.status_rules import validate_analyst_status_transition
        
        # Invalid transitions
        invalid_cases = [
            ("rejected", "approved"),
            ("closed", "approved"),
            ("invalidated", "closed")
        ]
        
        for old, new in invalid_cases:
            is_valid, error = validate_analyst_status_transition(old, new)
            self.assertFalse(is_valid, f"{old} -> {new} should be invalid")


class TestPerformanceCalculation(unittest.TestCase):
    """Test performance calculation logic."""
    
    def test_long_return_calculation(self):
        """Long position return calculation."""
        from geo_market_watch.performance_engine import _calculate_return
        
        ret = _calculate_return("long", entry_price=100, close_price=115)
        
        self.assertEqual(ret, 15.0)  # (115-100)/100 * 100
    
    def test_short_return_calculation(self):
        """Short position return calculation."""
        from geo_market_watch.performance_engine import _calculate_return
        
        ret = _calculate_return("short", entry_price=100, close_price=85)
        
        self.assertEqual(ret, 15.0)  # (100-85)/100 * 100
    
    def test_outcome_classification(self):
        """Return classification into outcome buckets."""
        from geo_market_watch.performance_engine import _classify_outcome
        
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
        from geo_market_watch.database import connect_db
        
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
        import sqlite3
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
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
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
