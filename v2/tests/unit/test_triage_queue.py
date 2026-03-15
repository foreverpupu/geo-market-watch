"""
Unit tests for triage queue.
"""

import pytest
from datetime import datetime, timedelta
from v2.config import DEFAULT_ANALYST_WORKFLOW_CONFIG
from v2.domain.models import Signal
from v2.domain.enums import TriageStatus, SignalClass
from v2.repositories.triage_queue_repository import InMemoryTriageQueueRepository
from v2.services.triage_queue import add_to_triage_queue, claim_signal, check_expired_items


class TestAddToTriageQueue:
    """Test add_to_triage_queue function."""
    
    @pytest.fixture
    def config(self):
        return DEFAULT_ANALYST_WORKFLOW_CONFIG
    
    @pytest.fixture
    def high_priority_signal(self):
        return Signal(
            signal_id="SIG_001",
            event_id="EVT_001",
            signal_class=SignalClass.HIGH_PRIORITY.value,
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
    
    def test_adds_high_priority_signal(self, high_priority_signal, config):
        """Should add high priority signal to queue."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        item = add_to_triage_queue(high_priority_signal, config, repository, now)
        
        assert item.signal_id == "SIG_001"
        assert item.status == TriageStatus.PENDING.value
        assert item.assigned_to is None
        assert repository.count() == 1
    
    def test_rejects_low_priority_signal(self, config):
        """Should reject signal below threshold."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        low_signal = Signal(
            signal_id="SIG_002",
            event_id="EVT_002",
            signal_class=SignalClass.LOW_SIGNAL.value,
            rank_score=0.30,  # Below threshold
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
        
        with pytest.raises(ValueError):
            add_to_triage_queue(low_signal, config, repository, now)


class TestClaimSignal:
    """Test claim_signal function."""
    
    def test_claims_unassigned_signal(self):
        """Should allow claiming unassigned signal."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Add item first
        from v2.domain.models import TriageQueueItem
        item = TriageQueueItem(
            signal_id="SIG_001",
            event_id="EVT_001",
            rank_score=0.85,
            assigned_to=None,
            added_at=now,
            due_by=now + timedelta(hours=48),
            status=TriageStatus.PENDING.value,
        )
        repository.add_item(item)
        
        # Claim
        claimed = claim_signal("SIG_001", "analyst_001", repository, now)
        
        assert claimed.assigned_to == "analyst_001"
        assert claimed.status == TriageStatus.IN_REVIEW.value
    
    def test_rejects_claiming_assigned_signal(self):
        """Should reject claiming already assigned signal."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Add item with assignment
        from v2.domain.models import TriageQueueItem
        item = TriageQueueItem(
            signal_id="SIG_001",
            event_id="EVT_001",
            rank_score=0.85,
            assigned_to="analyst_001",
            added_at=now,
            due_by=now + timedelta(hours=48),
            status=TriageStatus.IN_REVIEW.value,
        )
        repository.add_item(item)
        
        # Try to claim
        with pytest.raises(ValueError):
            claim_signal("SIG_001", "analyst_002", repository, now)


class TestCheckExpiredItems:
    """Test check_expired_items function."""
    
    def test_finds_expired_items(self):
        """Should find and mark expired items."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Add expired item
        from v2.domain.models import TriageQueueItem
        item = TriageQueueItem(
            signal_id="SIG_001",
            event_id="EVT_001",
            rank_score=0.85,
            assigned_to=None,
            added_at=now - timedelta(hours=50),
            due_by=now - timedelta(hours=2),
            status=TriageStatus.PENDING.value,
        )
        repository.add_item(item)
        
        # Check expired
        expired = check_expired_items(repository, now)
        
        assert len(expired) == 1
        assert expired[0].status == TriageStatus.EXPIRED.value
    
    def test_ignores_non_expired_items(self):
        """Should not mark non-expired items."""
        repository = InMemoryTriageQueueRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        # Add non-expired item
        from v2.domain.models import TriageQueueItem
        item = TriageQueueItem(
            signal_id="SIG_001",
            event_id="EVT_001",
            rank_score=0.85,
            assigned_to=None,
            added_at=now,
            due_by=now + timedelta(hours=48),
            status=TriageStatus.PENDING.value,
        )
        repository.add_item(item)
        
        # Check expired
        expired = check_expired_items(repository, now)
        
        assert len(expired) == 0
