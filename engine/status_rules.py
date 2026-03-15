"""
Geo Market Watch v6.3 — Status Rules Engine

Defines allowed status transitions for trade ideas.
"""

from typing import List, Tuple, Optional


# Valid status values
ANALYST_STATUSES = [
    "pending_review",
    "approved",
    "rejected",
    "invalidated",
    "closed"
]

APPROVAL_STATUSES = [
    "unreviewed",
    "approved",
    "rejected"
]

REVIEW_DECISIONS = [
    "approve",
    "monitor",
    "reject",
    "needs_revision"
]

CONFIDENCE_LEVELS = [
    "low",
    "medium",
    "high"
]

LIFECYCLE_EVENT_TYPES = [
    "created",
    "approved",
    "rejected",
    "invalidated",
    "updated",
    "closed"
]


# Valid status transitions
# Format: (from_status, to_status) -> allowed
VALID_TRANSITIONS = {
    # From pending_review
    ("pending_review", "approved"): True,
    ("pending_review", "rejected"): True,
    ("pending_review", "invalidated"): True,
    ("pending_review", "closed"): True,
    
    # From approved
    ("approved", "invalidated"): True,
    ("approved", "closed"): True,
    ("approved", "updated"): True,
    
    # From rejected (no transitions allowed)
    # From invalidated (no transitions allowed)
    # From closed (no transitions allowed)
}


def validate_status_transition(old_status: str, new_status: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if a status transition is allowed.
    
    Args:
        old_status: Current analyst status
        new_status: Proposed new status
        
    Returns:
        (is_valid, error_message)
    """
    if old_status == new_status:
        return True, None
    
    if old_status not in ANALYST_STATUSES:
        return False, f"Invalid current status: {old_status}"
    
    if new_status not in ANALYST_STATUSES:
        return False, f"Invalid target status: {new_status}"
    
    # Check if transition is valid
    if (old_status, new_status) in VALID_TRANSITIONS:
        return True, None
    
    # Transition not found - invalid
    return False, f"Transition from '{old_status}' to '{new_status}' is not allowed"


def get_allowed_transitions(status: str) -> List[str]:
    """
    Get list of allowed transitions from a given status.
    
    Args:
        status: Current analyst status
        
    Returns:
        List of allowed target statuses
    """
    if status not in ANALYST_STATUSES:
        return []
    
    allowed = []
    for (from_status, to_status), permitted in VALID_TRANSITIONS.items():
        if from_status == status and permitted:
            allowed.append(to_status)
    
    return allowed


def get_review_decision_analyst_status(decision: str) -> str:
    """
    Map review decision to analyst status.
    
    Args:
        decision: Review decision (approve, monitor, reject, needs_revision)
        
    Returns:
        Corresponding analyst status
    """
    mapping = {
        "approve": "approved",
        "reject": "rejected",
        "monitor": "pending_review",
        "needs_revision": "pending_review"
    }
    return mapping.get(decision, "pending_review")


def get_review_decision_approval_status(decision: str) -> str:
    """
    Map review decision to approval status.
    
    Args:
        decision: Review decision
        
    Returns:
        Corresponding approval status
    """
    mapping = {
        "approve": "approved",
        "reject": "rejected",
        "monitor": "unreviewed",
        "needs_revision": "unreviewed"
    }
    return mapping.get(decision, "unreviewed")


def requires_review_notes(decision: str) -> bool:
    """
    Check if a review decision requires notes.
    
    Args:
        decision: Review decision
        
    Returns:
        True if notes are required
    """
    return decision in ["reject", "needs_revision"]


def validate_review_decision(decision: str, notes: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate a review decision including notes requirement.
    
    Args:
        decision: Review decision
        notes: Review notes (may be None)
        
    Returns:
        (is_valid, error_message)
    """
    if decision not in REVIEW_DECISIONS:
        return False, f"Invalid review decision: {decision}. Must be one of: {', '.join(REVIEW_DECISIONS)}"
    
    if requires_review_notes(decision):
        if not notes or not notes.strip():
            return False, f"Review decision '{decision}' requires notes. Please provide feedback."
    
    return True, None


if __name__ == "__main__":
    # Test transitions
    print("Status Rules Engine — v6.3")
    print("=" * 50)
    print()
    
    print("Valid transitions from pending_review:")
    for status in get_allowed_transitions("pending_review"):
        print(f"  → {status}")
    
    print()
    print("Valid transitions from approved:")
    for status in get_allowed_transitions("approved"):
        print(f"  → {status}")
    
    print()
    print("Valid transitions from rejected:")
    for status in get_allowed_transitions("rejected"):
        print(f"  → {status}")
    
    print()
    print("Review decision validation:")
    for decision in REVIEW_DECISIONS:
        requires = "required" if requires_review_notes(decision) else "optional"
        print(f"  {decision}: notes {requires}")
