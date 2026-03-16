"""
Unit tests for review actions.
"""

from datetime import datetime

import pytest
from v2.domain.enums import EventPhase, EventStatus, ReviewActionType
from v2.domain.models import CanonicalEvent, Signal
from v2.repositories.event_repository import InMemoryEventRepository
from v2.repositories.review_actions_repository import InMemoryReviewActionsRepository
from v2.services.review_actions import log_review_action


class TestLogReviewAction:
    """Test log_review_action function."""
    
    @pytest.fixture
    def base_event(self):
        return CanonicalEvent(
            event_id="EVT_001",
            cluster_id="CLUSTER_001",
            canonical_title="Test Event",
            event_type="shipping_disruption",
            region="test",
            country_codes=[],
            normalized_entities=[],
            first_seen_at=datetime(2024, 1, 15),
            last_seen_at=datetime(2024, 1, 15),
            occurred_at_start=datetime(2024, 1, 15),
            occurred_at_end=datetime(2024, 1, 15),
            status=EventStatus.DETECTED.value,
            phase=EventPhase.WARNING.value,
            evidence_count=1,
        )
    
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
    
    def test_logs_action(self, base_signal, base_event):
        """Should log action."""
        review_repo = InMemoryReviewActionsRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        action = log_review_action(
            signal=base_signal,
            action_type=ReviewActionType.COMMENT.value,
            analyst_id="analyst_001",
            review_repository=review_repo,
            comment="Test comment",
            now=now,
        )
        
        assert action.signal_id == "SIG_001"
        assert action.action_type == ReviewActionType.COMMENT.value
        assert action.action_taken_by == "analyst_001"
        assert action.comment == "Test comment"
        assert review_repo.count() == 1
    
    def test_updates_event_status_to_confirmed(self, base_signal, base_event):
        """Should update event status to confirmed when marked relevant."""
        review_repo = InMemoryReviewActionsRepository()
        event_repo = InMemoryEventRepository()
        event_repo.create_event(base_event)
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        log_review_action(
            signal=base_signal,
            action_type=ReviewActionType.MARK_AS_RELEVANT.value,
            analyst_id="analyst_001",
            event=base_event,
            event_repository=event_repo,
            review_repository=review_repo,
            now=now,
        )
        
        updated_event = event_repo.get_event(base_event.event_id)
        assert updated_event.status == EventStatus.CONFIRMED.value
    
    def test_updates_event_status_to_resolved(self, base_signal, base_event):
        """Should update event status to resolved when archived."""
        review_repo = InMemoryReviewActionsRepository()
        event_repo = InMemoryEventRepository()
        event_repo.create_event(base_event)
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        log_review_action(
            signal=base_signal,
            action_type=ReviewActionType.ARCHIVE.value,
            analyst_id="analyst_001",
            event=base_event,
            event_repository=event_repo,
            review_repository=review_repo,
            now=now,
        )
        
        updated_event = event_repo.get_event(base_event.event_id)
        assert updated_event.status == EventStatus.RESOLVED.value
    
    def test_records_override_values(self, base_signal, base_event):
        """Should record override values."""
        review_repo = InMemoryReviewActionsRepository()
        now = datetime(2024, 1, 15, 12, 0, 0)
        
        action = log_review_action(
            signal=base_signal,
            action_type=ReviewActionType.COMMENT.value,
            analyst_id="analyst_001",
            review_repository=review_repo,
            severity_override=0.95,
            exposure_override={"direction": "negative"},
            agreement_with_ai=False,
            now=now,
        )
        
        assert action.severity_override == 0.95
        assert action.exposure_override == {"direction": "negative"}
        assert action.agreement_with_ai is False
