"""
Geo Market Watch v6.3 — Lifecycle Engine

Tracks lifecycle events for trade ideas.
"""

import sqlite3
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from engine.status_rules import validate_status_transition, LIFECYCLE_EVENT_TYPES


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())[:12]


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def record_lifecycle_event(
    db_path: str,
    trade_idea_id: str,
    event_type: str,
    reason: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Record a lifecycle event for a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        event_type: Type of lifecycle event
        reason: Reason for the event
        
    Returns:
        (success, error_message, event_record)
    """
    if event_type not in LIFECYCLE_EVENT_TYPES:
        return False, f"Invalid event type: {event_type}. Must be one of: {', '.join(LIFECYCLE_EVENT_TYPES)}", None
    
    conn = sqlite3.connect(db_path)
    
    try:
        lifecycle_id = generate_id()
        created_at = get_timestamp()
        
        conn.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, event_type, reason, created_at)
        )
        
        conn.commit()
        
        event_record = {
            "lifecycle_id": lifecycle_id,
            "trade_idea_id": trade_idea_id,
            "event_type": event_type,
            "reason": reason,
            "created_at": created_at
        }
        
        return True, None, event_record
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database error: {e}", None
    finally:
        conn.close()


def invalidate_trade_idea(
    db_path: str,
    trade_idea_id: str,
    reason: str
) -> Tuple[bool, Optional[str]]:
    """
    Invalidate a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        reason: Invalidation reason
        
    Returns:
        (success, error_message)
    """
    if not reason or not reason.strip():
        return False, "Invalidation requires a reason"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        # Get current status
        cursor = conn.execute(
            "SELECT analyst_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        old_status = row["analyst_status"]
        new_status = "invalidated"
        
        # Validate transition
        is_valid, error = validate_status_transition(old_status, new_status)
        if not is_valid:
            return False, error
        
        updated_at = get_timestamp()
        
        # Update status
        conn.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, status = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (new_status, "invalidated", updated_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_id = generate_id()
        conn.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "invalidated", reason, updated_at)
        )
        
        conn.commit()
        return True, None
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def close_trade_idea(
    db_path: str,
    trade_idea_id: str,
    reason: str
) -> Tuple[bool, Optional[str]]:
    """
    Close a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        reason: Closure reason
        
    Returns:
        (success, error_message)
    """
    if not reason or not reason.strip():
        return False, "Closure requires a reason"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        # Get current status
        cursor = conn.execute(
            "SELECT analyst_status FROM trade_ideas WHERE trade_idea_id = ?",
            (trade_idea_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return False, f"Trade idea not found: {trade_idea_id}"
        
        old_status = row["analyst_status"]
        new_status = "closed"
        
        # Validate transition
        is_valid, error = validate_status_transition(old_status, new_status)
        if not is_valid:
            return False, error
        
        updated_at = get_timestamp()
        
        # Update status
        conn.execute(
            """
            UPDATE trade_ideas 
            SET analyst_status = ?, status = ?, updated_at = ?
            WHERE trade_idea_id = ?
            """,
            (new_status, "closed", updated_at, trade_idea_id)
        )
        
        # Record lifecycle event
        lifecycle_id = generate_id()
        conn.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "closed", reason, updated_at)
        )
        
        conn.commit()
        return True, None
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def update_trade_idea(
    db_path: str,
    trade_idea_id: str,
    update_reason: str
) -> Tuple[bool, Optional[str]]:
    """
    Update a trade idea with a reason.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        update_reason: Reason for update
        
    Returns:
        (success, error_message)
    """
    if not update_reason or not update_reason.strip():
        return False, "Update requires a reason"
    
    conn = sqlite3.connect(db_path)
    
    try:
        updated_at = get_timestamp()
        
        # Record lifecycle event
        lifecycle_id = generate_id()
        conn.execute(
            """
            INSERT INTO idea_lifecycle (lifecycle_id, trade_idea_id, event_type, event_reason, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lifecycle_id, trade_idea_id, "updated", update_reason, updated_at)
        )
        
        # Update timestamp
        conn.execute(
            "UPDATE trade_ideas SET updated_at = ? WHERE trade_idea_id = ?",
            (updated_at, trade_idea_id)
        )
        
        conn.commit()
        return True, None
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def get_lifecycle_history(db_path: str, trade_idea_id: str) -> List[Dict[str, Any]]:
    """
    Get lifecycle history for a trade idea.
    
    Args:
        db_path: Path to SQLite database
        trade_idea_id: Trade idea ID
        
    Returns:
        List of lifecycle events
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute(
            """
            SELECT * FROM idea_lifecycle 
            WHERE trade_idea_id = ?
            ORDER BY created_at ASC
            """,
            (trade_idea_id,)
        )
        
        return [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()


if __name__ == "__main__":
    print("Lifecycle Engine — v6.3")
    print("=" * 50)
    print()
    print("Functions:")
    print("  • record_lifecycle_event()")
    print("  • invalidate_trade_idea()")
    print("  • close_trade_idea()")
    print("  • update_trade_idea()")
    print("  • get_lifecycle_history()")
