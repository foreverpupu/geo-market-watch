"""
Geo Market Watch v6.3 — Idea Review Engine

Processes analyst review decisions for trade ideas.
"""

import sqlite3
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from engine.status_rules import (
    validate_review_decision,
    get_review_decision_analyst_status,
    get_review_decision_approval_status,
    requires_review_notes
)


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())[:12]


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def submit_review(
    db_path: str,
    trade_idea_id: str,
    reviewer: str,
    decision: str,
    confidence: Optional[str] = None,
    notes: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Submit a review for a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: ID of trade idea being reviewed
        reviewer: Name/ID of reviewer
        decision: Review decision (approve, monitor, reject, needs_revision)
        confidence: Reviewer confidence (low, medium, high)
        notes: Review notes
        
    Returns:
        (success, error_message, review_record)
    """
    # Validate decision
    is_valid, error = validate_review_decision(decision, notes)
    if not is_valid:
        return False, error, None
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        # Check if trade idea exists
        cursor = conn.execute(
            "SELECT * FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        idea = cursor.fetchone()
        
        if not idea:
            return False, f"Trade idea not found: {trade_idea_id}", None
        
        # Create review record
        review_id = generate_id()
        created_at = get_timestamp()
        
        conn.execute(
            """
            INSERT INTO idea_reviews (review_id, trade_idea_id, reviewer, 
                                      review_decision, confidence, review_notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (review_id, trade_idea_id, reviewer, decision, confidence, notes, created_at)
        )
        
        # Update trade idea status
        analyst_status = get_review_decision_analyst_status(decision)
        approval_status = get_review_decision_approval_status(decision)
        
        conn.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, approval_status = ?, last_reviewed_at = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (analyst_status, approval_status, created_at, created_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_id = generate_id()
        event_type = decision.replace("needs_revision", "updated")  # Map to lifecycle event
        
        conn.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, event_type, notes, created_at)
        )
        
        conn.commit()
        
        review_record = {
            "review_id": review_id,
            "trade_idea_id": trade_idea_id,
            "reviewer": reviewer,
            "decision": decision,
            "confidence": confidence,
            "notes": notes,
            "created_at": created_at
        }
        
        return True, None, review_record
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database error: {e}", None
    finally:
        conn.close()


def get_reviews_for_idea(db_path: str, trade_idea_id: str) -> List[Dict[str, Any]]:
    """
    Get all reviews for a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        
    Returns:
        List of review records
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute(
            """
            SELECT * FROM idea_reviews 
            WHERE trade_idea_id = ?
            ORDER BY created_at DESC
            """,
            (trade_idea_id,)
        )
        
        return [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()


def get_review_summary(db_path: str, trade_idea_id: str) -> Optional[Dict[str, Any]]:
    """
    Get summary of reviews for a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        
    Returns:
        Review summary or None
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute(
            """
            SELECT 
                COUNT(*) as total_reviews,
                COUNT(CASE WHEN review_decision = 'approve' THEN 1 END) as approvals,
                COUNT(CASE WHEN review_decision = 'reject' THEN 1 END) as rejections,
                COUNT(CASE WHEN review_decision = 'monitor' THEN 1 END) as monitors,
                COUNT(CASE WHEN review_decision = 'needs_revision' THEN 1 END) as revisions
            FROM idea_reviews 
            WHERE trade_idea_id = ?
            """,
            (trade_idea_id,)
        )
        
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None
        
    finally:
        conn.close()


def update_idea_status_after_review(
    db_path: str,
    trade_idea_id: str,
    decision: str
) -> Tuple[bool, Optional[str]]:
    """
    Update trade idea status based on review decision.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        decision: Review decision
        
    Returns:
        (success, error_message)
    """
    conn = sqlite3.connect(db_path)
    
    try:
        analyst_status = get_review_decision_analyst_status(decision)
        approval_status = get_review_decision_approval_status(decision)
        updated_at = get_timestamp()
        
        conn.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, approval_status = ?, last_reviewed_at = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (analyst_status, approval_status, updated_at, updated_at, trade_idea_id)
        )
        
        conn.commit()
        return True, None
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


if __name__ == "__main__":
    print("Idea Review Engine — v6.3")
    print("=" * 50)
    print()
    print("Functions:")
    print("  • submit_review()")
    print("  • get_reviews_for_idea()")
    print("  • get_review_summary()")
    print("  • update_idea_status_after_review()")
