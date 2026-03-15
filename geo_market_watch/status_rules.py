"""
Geo Market Watch v6.3 — Status Rules Engine

Defines allowed status transitions for trade ideas.
Invalid transitions are rejected.
"""

from typing import List, Set, Tuple

# Valid analyst_status values
ANALYST_STATUSES = {
    "pending_review",
    "approved",
    "rejected",
    "invalidated",
    "closed"
}

# Valid approval_status values
APPROVAL_STATUSES = {
    "unreviewed",
    "approved",
    "rejected"
}

# Valid review decisions
REVIEW_DECISIONS = {
    "approve",
    "monitor",
    "reject",
    "needs_revision"
}

# Valid confidence levels
CONFIDENCE_LEVELS = {
    "low",
    "medium",
    "high"
}

# Valid lifecycle event types
LIFECYCLE_EVENTS = {
    "created",
    "approved",
    "rejected",
    "invalidated",
    "updated",
    "closed",
    "tracking_started",
    "tracking_updated",
    "tracking_closed",
    "performance_corrected"
}

# Allowed status transitions for analyst_status
# Format: current_status -> {allowed_next_statuses}
ANALYST_STATUS_TRANSITIONS: dict[str, Set[str]] = {
    "pending_review": {"approved", "rejected", "invalidated"},
    "approved": {"invalidated", "closed", "updated"},
    "rejected": set(),  # Terminal state - no transitions allowed
    "invalidated": set(),  # Terminal state - no transitions allowed
    "closed": set()  # Terminal state - no transitions allowed
}

# Allowed status transitions for approval_status
APPROVAL_STATUS_TRANSITIONS: dict[str, Set[str]] = {
    "unreviewed": {"approved", "rejected"},
    "approved": {"rejected"},  # Can revoke approval
    "rejected": {"approved"}   # Can reconsider rejection
}


def validate_analyst_status_transition(old_status: str, new_status: str) -> Tuple[bool, str]:
    """
    Validate if a transition from old_status to new_status is allowed.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if old_status not in ANALYST_STATUSES:
        return False, f"Invalid old status: {old_status}. Must be one of: {ANALYST_STATUSES}"
    
    if new_status not in ANALYST_STATUSES:
        return False, f"Invalid new status: {new_status}. Must be one of: {ANALYST_STATUSES}"
    
    if old_status == new_status:
        return True, ""  # Same status is always valid (no-op)
    
    allowed = ANALYST_STATUS_TRANSITIONS.get(old_status, set())
    if new_status not in allowed:
        return False, f"Invalid transition: {old_status} → {new_status}. Allowed: {allowed or 'none (terminal state)'}"
    
    return True, ""


def validate_approval_status_transition(old_status: str, new_status: str) -> Tuple[bool, str]:
    """
    Validate if a transition from old_status to new_status is allowed for approval_status.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if old_status not in APPROVAL_STATUSES:
        return False, f"Invalid old approval status: {old_status}. Must be one of: {APPROVAL_STATUSES}"
    
    if new_status not in APPROVAL_STATUSES:
        return False, f"Invalid new approval status: {new_status}. Must be one of: {APPROVAL_STATUSES}"
    
    if old_status == new_status:
        return True, ""  # Same status is always valid (no-op)
    
    allowed = APPROVAL_STATUS_TRANSITIONS.get(old_status, set())
    if new_status not in allowed:
        return False, f"Invalid approval transition: {old_status} → {new_status}. Allowed: {allowed}"
    
    return True, ""


def get_allowed_analyst_transitions(status: str) -> Set[str]:
    """Get all allowed transitions from a given analyst status."""
    if status not in ANALYST_STATUSES:
        return set()
    return ANALYST_STATUS_TRANSITIONS.get(status, set())


def get_allowed_approval_transitions(status: str) -> Set[str]:
    """Get all allowed transitions from a given approval status."""
    if status not in APPROVAL_STATUSES:
        return set()
    return APPROVAL_STATUS_TRANSITIONS.get(status, set())


def is_terminal_status(status: str) -> bool:
    """Check if a status is terminal (no further transitions allowed)."""
    if status not in ANALYST_STATUSES:
        return False
    return len(ANALYST_STATUS_TRANSITIONS.get(status, set())) == 0


def get_review_decision_mapping() -> dict[str, str]:
    """
    Map review decisions to analyst_status values.
    
    Returns:
        Dict mapping decision -> status
    """
    return {
        "approve": "approved",
        "reject": "rejected",
        "monitor": "pending_review",
        "needs_revision": "pending_review"
    }


def validate_review_decision(decision: str) -> Tuple[bool, str]:
    """Validate if a review decision is valid."""
    if decision not in REVIEW_DECISIONS:
        return False, f"Invalid decision: {decision}. Must be one of: {REVIEW_DECISIONS}"
    return True, ""


def validate_confidence(confidence: str) -> Tuple[bool, str]:
    """Validate if a confidence level is valid."""
    if confidence not in CONFIDENCE_LEVELS:
        return False, f"Invalid confidence: {confidence}. Must be one of: {CONFIDENCE_LEVELS}"
    return True, ""


def validate_lifecycle_event(event_type: str) -> Tuple[bool, str]:
    """Validate if a lifecycle event type is valid."""
    if event_type not in LIFECYCLE_EVENTS:
        return False, f"Invalid lifecycle event: {event_type}. Must be one of: {LIFECYCLE_EVENTS}"
    return True, ""


def get_status_summary() -> dict:
    """Get a summary of all status rules for documentation."""
    return {
        "analyst_status": {
            "values": list(ANALYST_STATUSES),
            "transitions": {k: list(v) for k, v in ANALYST_STATUS_TRANSITIONS.items()},
            "terminal_states": [s for s in ANALYST_STATUSES if is_terminal_status(s)]
        },
        "approval_status": {
            "values": list(APPROVAL_STATUSES),
            "transitions": {k: list(v) for k, v in APPROVAL_STATUS_TRANSITIONS.items()}
        },
        "review_decisions": list(REVIEW_DECISIONS),
        "confidence_levels": list(CONFIDENCE_LEVELS),
        "lifecycle_events": list(LIFECYCLE_EVENTS)
    }


if __name__ == "__main__":
    # Test the status rules
    print("Geo Market Watch v6.3 — Status Rules Engine")
    print("=" * 50)
    print()
    
    # Test valid transitions
    test_cases = [
        ("pending_review", "approved"),
        ("pending_review", "rejected"),
        ("approved", "invalidated"),
        ("approved", "closed"),
        ("rejected", "approved"),  # Invalid
        ("closed", "approved"),    # Invalid
    ]
    
    print("Transition Tests:")
    for old, new in test_cases:
        valid, error = validate_analyst_status_transition(old, new)
        status = "✓" if valid else "✗"
        print(f"  {status} {old} → {new}")
        if error:
            print(f"      {error}")
    
    print()
    print("Terminal States:", [s for s in ANALYST_STATUSES if is_terminal_status(s)])
    print()
    print("Full Summary:")
    import json
    print(json.dumps(get_status_summary(), indent=2))
