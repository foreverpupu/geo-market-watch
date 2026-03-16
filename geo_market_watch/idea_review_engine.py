"""
Geo Market Watch v6.3 — Idea Review Engine

Processes analyst review decisions and manages review workflow.
"""

import sqlite3
import uuid
from datetime import UTC, datetime

from .status_rules import (
    get_review_decision_mapping,
    validate_analyst_status_transition,
    validate_confidence,
    validate_review_decision,
)


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def submit_review(
    db_path: str,
    trade_idea_id: str,
    reviewer: str,
    decision: str,
    confidence: str | None = None,
    notes: str | None = None
) -> tuple[bool, str]:
    """
    Submit an analyst review for a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        reviewer: Name/ID of the reviewer
        decision: Review decision (approve, monitor, reject, needs_revision)
        confidence: Optional confidence level (low, medium, high)
        notes: Optional review notes
    
    Returns:
        Tuple of (success, message_or_error)
    """
    # Validate inputs
    valid, error = validate_review_decision(decision)
    if not valid:
        return False, error
    
    if confidence:
        valid, error = validate_confidence(confidence)
        if not valid:
            return False, error
    
    if not reviewer:
        return False, "Reviewer name is required"
    
    # Enforce notes for reject and needs_revision decisions
    if decision in ("reject", "needs_revision") and not notes:
        return False, f"Review notes are required for '{decision}' decisions"
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Check if trade idea exists
        cursor.execute(
            "SELECT analyst_status, approval_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        current_analyst_status = row["analyst_status"]
        current_approval_status = row["approval_status"]
        
        # Map decision to new status
        decision_map = get_review_decision_mapping()
        new_analyst_status = decision_map.get(decision)
        
        # Validate transition
        valid, error = validate_analyst_status_transition(current_analyst_status, new_analyst_status)
        if not valid:
            return False, error
        
        # Create review record
        review_id = str(uuid.uuid4())
        created_at = datetime.now(UTC).isoformat()
        
        cursor.execute(
            """
            INSERT INTO idea_reviews (review_id, trade_idea_id, reviewer, review_decision, confidence, review_notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (review_id, trade_idea_id, reviewer, decision, confidence, notes, created_at)
        )
        
        # Update trade idea status
        new_approval_status = "approved" if decision == "approve" else ("rejected" if decision == "reject" else current_approval_status)
        
        cursor.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, approval_status = ?, last_reviewed_at = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (new_analyst_status, new_approval_status, created_at, created_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_event = "approved" if decision == "approve" else ("rejected" if decision == "reject" else "updated")
        lifecycle_reason = f"Review by {reviewer}: {decision}"
        if notes:
            lifecycle_reason += f" - {notes}"
        
        lifecycle_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, lifecycle_event, lifecycle_reason, created_at)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Review submitted: {decision} for {trade_idea_id} by {reviewer}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def get_reviews_for_idea(db_path: str, trade_idea_id: str) -> list[dict]:
    """
    Get all reviews for a specific trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
    
    Returns:
        List of review records as dictionaries
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT review_id, reviewer, review_decision, confidence, review_notes, created_at
            FROM idea_reviews
            WHERE trade_idea_id = ?
            ORDER BY created_at DESC
            """,
            (trade_idea_id,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


def get_pending_reviews(db_path: str) -> list[dict]:
    """
    Get all trade ideas pending review.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of trade ideas awaiting review
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.created_at
            FROM trade_ideas t
            WHERE t.analyst_status = 'pending_review'
            ORDER BY t.created_at ASC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


def get_review_statistics(db_path: str) -> dict:
    """
    Get review statistics across all trade ideas.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        Dictionary with review statistics
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Count by analyst_status
        cursor.execute(
            """
            SELECT analyst_status, COUNT(*) as count
            FROM trade_ideas
            GROUP BY analyst_status
            """
        )
        status_counts = {row["analyst_status"]: row["count"] for row in cursor.fetchall()}
        
        # Count by approval_status
        cursor.execute(
            """
            SELECT approval_status, COUNT(*) as count
            FROM trade_ideas
            GROUP BY approval_status
            """
        )
        approval_counts = {row["approval_status"]: row["count"] for row in cursor.fetchall()}
        
        # Total reviews submitted
        cursor.execute("SELECT COUNT(*) as count FROM idea_reviews")
        total_reviews = cursor.fetchone()["count"]
        
        # Reviews by decision type
        cursor.execute(
            """
            SELECT review_decision, COUNT(*) as count
            FROM idea_reviews
            GROUP BY review_decision
            """
        )
        decision_counts = {row["review_decision"]: row["count"] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "by_analyst_status": status_counts,
            "by_approval_status": approval_counts,
            "total_reviews_submitted": total_reviews,
            "reviews_by_decision": decision_counts
        }
    
    except sqlite3.Error as e:
        return {"error": str(e)}


def batch_review(
    db_path: str,
    reviewer: str,
    reviews: list[dict]
) -> tuple[int, list[str]]:
    """
    Submit multiple reviews in a batch.
    
    Args:
        db_path: Path to the SQLite database
        reviewer: Name/ID of the reviewer
        reviews: List of review dicts with keys: trade_idea_id, decision, confidence (optional), notes (optional)
    
    Returns:
        Tuple of (success_count, list_of_errors)
    """
    success_count = 0
    errors = []
    
    for review in reviews:
        trade_idea_id = review.get("trade_idea_id")
        decision = review.get("decision")
        confidence = review.get("confidence")
        notes = review.get("notes")
        
        success, message = submit_review(
            db_path, trade_idea_id, reviewer, decision, confidence, notes
        )
        
        if success:
            success_count += 1
        else:
            errors.append(f"{trade_idea_id}: {message}")
    
    return success_count, errors


def get_reviewer_activity(db_path: str, reviewer: str | None = None) -> list[dict]:
    """
    Get reviewer activity statistics.
    
    Args:
        db_path: Path to the SQLite database
        reviewer: Optional specific reviewer to query
    
    Returns:
        List of reviewer activity records
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        if reviewer:
            cursor.execute(
                """
                SELECT 
                    reviewer,
                    review_decision,
                    COUNT(*) as count,
                    MIN(created_at) as first_review,
                    MAX(created_at) as last_review
                FROM idea_reviews
                WHERE reviewer = ?
                GROUP BY reviewer, review_decision
                """,
                (reviewer,)
            )
        else:
            cursor.execute(
                """
                SELECT 
                    reviewer,
                    review_decision,
                    COUNT(*) as count,
                    MIN(created_at) as first_review,
                    MAX(created_at) as last_review
                FROM idea_reviews
                GROUP BY reviewer, review_decision
                ORDER BY reviewer, review_decision
                """
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


if __name__ == "__main__":
    print("Geo Market Watch v6.3 — Idea Review Engine")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  • submit_review()")
    print("  • get_reviews_for_idea()")
    print("  • get_pending_reviews()")
    print("  • get_review_statistics()")
    print("  • batch_review()")
    print("  • get_reviewer_activity()")
