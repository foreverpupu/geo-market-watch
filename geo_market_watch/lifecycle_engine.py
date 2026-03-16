"""
Geo Market Watch v6.3 — Lifecycle Engine

Tracks lifecycle events for trade ideas.
Supports invalidation, closure, and updates.
"""

import sqlite3
import uuid
from datetime import UTC, datetime

from .status_rules import (
    LIFECYCLE_EVENTS,
    validate_analyst_status_transition,
    validate_lifecycle_event,
)


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def record_lifecycle_event(
    db_path: str,
    trade_idea_id: str,
    event_type: str,
    reason: str | None = None
) -> tuple[bool, str]:
    """
    Record a lifecycle event for a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        event_type: Type of event (created, approved, rejected, invalidated, updated, closed)
        reason: Optional reason for the event
    
    Returns:
        Tuple of (success, message_or_error)
    """
    # Validate event type
    valid, error = validate_lifecycle_event(event_type)
    if not valid:
        return False, error
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Check if trade idea exists
        cursor.execute(
            "SELECT trade_idea_id FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        if not cursor.fetchone():
            return False, f"Trade idea not found: {trade_idea_id}"
        
        # Create lifecycle event
        lifecycle_id = str(uuid.uuid4())
        created_at = datetime.now(UTC).isoformat()
        
        cursor.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, event_type, reason, created_at)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Lifecycle event recorded: {event_type} for {trade_idea_id}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def invalidate_trade_idea(
    db_path: str,
    trade_idea_id: str,
    reason: str
) -> tuple[bool, str]:
    """
    Invalidate a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        reason: Reason for invalidation (required)
    
    Returns:
        Tuple of (success, message_or_error)
    """
    if not reason:
        return False, "Reason is required for invalidation"
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute(
            "SELECT analyst_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        current_status = row["analyst_status"]
        
        # Validate transition
        valid, error = validate_analyst_status_transition(current_status, "invalidated")
        if not valid:
            return False, error
        
        # Update trade idea status
        updated_at = datetime.now(UTC).isoformat()
        cursor.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            ("invalidated", updated_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "invalidated", reason, updated_at)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Trade idea {trade_idea_id} invalidated: {reason}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def close_trade_idea(
    db_path: str,
    trade_idea_id: str,
    reason: str
) -> tuple[bool, str]:
    """
    Close a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        reason: Reason for closure (required)
    
    Returns:
        Tuple of (success, message_or_error)
    """
    if not reason:
        return False, "Reason is required for closure"
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute(
            "SELECT analyst_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        current_status = row["analyst_status"]
        
        # Validate transition
        valid, error = validate_analyst_status_transition(current_status, "closed")
        if not valid:
            return False, error
        
        # Update trade idea status
        updated_at = datetime.now(UTC).isoformat()
        cursor.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, status = 'closed', updated_at = ?
            WHERE trade_idea_id = ?
            """,
            ("closed", updated_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "closed", reason, updated_at)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Trade idea {trade_idea_id} closed: {reason}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def update_trade_idea(
    db_path: str,
    trade_idea_id: str,
    update_reason: str,
    **updates
) -> tuple[bool, str]:
    """
    Update a trade idea with changes and record the update event.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
        update_reason: Reason for the update (required)
        **updates: Field updates to apply (e.g., conviction='high', thesis='new thesis')
    
    Returns:
        Tuple of (success, message_or_error)
    """
    if not update_reason:
        return False, "Reason is required for updates"
    
    if not updates:
        return False, "No updates provided"
    
    allowed_fields = {
        "company_name", "ticker", "sector", "idea_type", "direction",
        "conviction", "thesis", "invalidation_condition"
    }
    
    # Filter to only allowed fields
    valid_updates = {k: v for k, v in updates.items() if k in allowed_fields}
    
    if not valid_updates:
        return False, f"No valid update fields provided. Allowed: {allowed_fields}"
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        # Check if trade idea exists
        cursor.execute(
            "SELECT analyst_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        current_status = row["analyst_status"]
        
        # Can only update if approved (or pending_review for minor edits)
        if current_status not in ["approved", "pending_review"]:
            return False, f"Cannot update trade idea in status: {current_status}"
        
        # Build update query
        updated_at = datetime.now(UTC).isoformat()
        set_clause = ", ".join([f"{k} = ?" for k in valid_updates.keys()])
        values = list(valid_updates.values()) + [updated_at, trade_idea_id]
        
        cursor.execute(
            f"""
            UPDATE trade_ideas 
            SET {set_clause}, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            values
        )
        
        # Record lifecycle event
        lifecycle_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "updated", update_reason, updated_at)
        )
        
        conn.commit()
        conn.close()
        
        return True, f"Trade idea {trade_idea_id} updated: {update_reason}"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"


def get_lifecycle_history(
    db_path: str,
    trade_idea_id: str
) -> list[dict]:
    """
    Get the full lifecycle history for a trade idea.
    
    Args:
        db_path: Path to the SQLite database
        trade_idea_id: The trade idea ID
    
    Returns:
        List of lifecycle events as dictionaries
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT lifecycle_id, event_type, event_reason, created_at
            FROM idea_lifecycle
            WHERE trade_idea_id = ?
            ORDER BY created_at ASC
            """,
            (trade_idea_id,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


def get_active_ideas(db_path: str) -> list[dict]:
    """
    Get all active (non-terminal) trade ideas.
    Dashboard priority: approved + high conviction first, then by created_at.
    
    Args:
        db_path: Path to the SQLite database
    
    Returns:
        List of active trade ideas sorted by dashboard priority
    """
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.analyst_status, t.approval_status, t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.analyst_status NOT IN ('rejected', 'invalidated', 'closed')
            ORDER BY 
                CASE t.analyst_status
                    WHEN 'approved' THEN 1
                    WHEN 'pending_review' THEN 2
                    ELSE 3
                END,
                CASE t.conviction
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                    ELSE 4
                END,
                t.created_at DESC
            """
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


def get_ideas_by_status(db_path: str, status: str) -> list[dict]:
    """
    Get trade ideas filtered by analyst status.
    
    Args:
        db_path: Path to the SQLite database
        status: The analyst status to filter by
    
    Returns:
        List of matching trade ideas
    """
    if status not in LIFECYCLE_EVENTS and status not in ["pending_review", "approved", "rejected", "invalidated", "closed"]:
        return []
    
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT 
                t.trade_idea_id, t.event_id, t.company_name, t.ticker,
                t.sector, t.idea_type, t.direction, t.conviction, t.thesis,
                t.analyst_status, t.approval_status, t.created_at, t.updated_at
            FROM trade_ideas t
            WHERE t.analyst_status = ?
            ORDER BY t.created_at DESC
            """,
            (status,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except sqlite3.Error:
        return []


if __name__ == "__main__":
    print("Geo Market Watch v6.3 — Lifecycle Engine")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  • record_lifecycle_event()")
    print("  • invalidate_trade_idea()")
    print("  • close_trade_idea()")
    print("  • update_trade_idea()")
    print("  • get_lifecycle_history()")
    print("  • get_active_ideas()")
    print("  • get_ideas_by_status()")
