"""
Geo Market Watch v6 — Database Engine

Provides reusable helper functions for database setup and CRUD operations.
"""

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .database_models import CREATE_TABLES_SQL


def connect_db(db_path: str) -> sqlite3.Connection:
    """
    Connect to SQLite database.
    
    Args:
        db_path: Path to database file
        
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
    return conn


def init_database(db_path: str) -> None:
    """
    Initialize database with all tables.
    
    Args:
        db_path: Path to database file
    """
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = connect_db(db_path)
    try:
        conn.executescript(CREATE_TABLES_SQL)
        conn.commit()
    finally:
        conn.close()


def generate_id() -> str:
    """Generate unique ID."""
    return str(uuid.uuid4())[:16]


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


# Event CRUD operations

def insert_event(conn: sqlite3.Connection, event: dict[str, Any]) -> str:
    """
    Insert a new event with raw data snapshot.
    
    Args:
        conn: Database connection
        event: Event dict with all required fields
        
    Returns:
        Generated event_id
    """
    event_id = generate_id()
    now = now_iso()
    
    # Serialize full event payload for future recovery
    import json
    raw_data = json.dumps(event, ensure_ascii=False, sort_keys=True)
    
    conn.execute("""
        INSERT INTO events (
            event_id, event_key, event_title, date_detected, region, category,
            summary, score, band, trigger_full_analysis, status, raw_data, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id,
        event.get('event_key'),
        event.get('event_title'),
        event.get('date_detected'),
        event.get('region'),
        event.get('category'),
        event.get('summary'),
        event.get('score'),
        event.get('band'),
        1 if event.get('trigger_full_analysis') else 0,
        event.get('status', 'active'),
        raw_data,
        now,
        now
    ))
    
    return event_id


def upsert_event(conn: sqlite3.Connection, event: dict[str, Any]) -> str:
    """
    Upsert an event (insert if new, update if exists).
    
    Updates updated_at timestamp on every upsert.
    
    Args:
        conn: Database connection
        event: Event dict with all required fields
        
    Returns:
        event_id (existing or newly generated)
    """
    event_key = event.get('event_key')
    
    # Check if event already exists
    existing = get_event_by_key(conn, event_key) if event_key else None
    
    if existing:
        # Update existing event
        event_id = existing['event_id']
        now = now_iso()
        
        # Serialize updated event payload
        import json
        raw_data = json.dumps(event, ensure_ascii=False, sort_keys=True)
        
        conn.execute("""
            UPDATE events SET
                event_title = ?,
                date_detected = ?,
                region = ?,
                category = ?,
                summary = ?,
                score = ?,
                band = ?,
                trigger_full_analysis = ?,
                status = ?,
                raw_data = ?,
                updated_at = ?
            WHERE event_id = ?
        """, (
            event.get('event_title'),
            event.get('date_detected'),
            event.get('region'),
            event.get('category'),
            event.get('summary'),
            event.get('score'),
            event.get('band'),
            1 if event.get('trigger_full_analysis') else 0,
            event.get('status', 'active'),
            raw_data,
            now,
            event_id
        ))
        
        return event_id
    else:
        # Insert new event
        return insert_event(conn, event)


def get_event(conn: sqlite3.Connection, event_id: str) -> dict[str, Any] | None:
    """Get event by ID."""
    cursor = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_event_by_key(conn: sqlite3.Connection, event_key: str) -> dict[str, Any] | None:
    """Get event by event_key."""
    cursor = conn.execute("SELECT * FROM events WHERE event_key = ?", (event_key,))
    row = cursor.fetchone()
    return dict(row) if row else None


def list_events(conn: sqlite3.Connection, limit: int = 100) -> list[dict[str, Any]]:
    """List all events."""
    cursor = conn.execute(
        "SELECT * FROM events ORDER BY date_detected DESC LIMIT ?",
        (limit,)
    )
    return [dict(row) for row in cursor.fetchall()]


def search_events(
    conn: sqlite3.Connection,
    region: str | None = None,
    category: str | None = None,
    band: str | None = None,
    limit: int = 100
) -> list[dict[str, Any]]:
    """Search events by filters."""
    query = "SELECT * FROM events WHERE 1=1"
    params = []
    
    if region:
        query += " AND region = ?"
        params.append(region)
    if category:
        query += " AND category = ?"
        params.append(category)
    if band:
        query += " AND band = ?"
        params.append(band)
    
    query += " ORDER BY date_detected DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.execute(query, params)
    return [dict(row) for row in cursor.fetchall()]


# Related data operations

def insert_source(conn: sqlite3.Connection, event_id: str, source: dict[str, Any]) -> str:
    """Insert source for an event."""
    source_id = generate_id()
    conn.execute("""
        INSERT INTO sources (source_id, event_id, source_name, source_url, published_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        source_id,
        event_id,
        source.get('source_name'),
        source.get('source_url'),
        source.get('published_at')
    ))
    return source_id


def insert_indicators(conn: sqlite3.Connection, event_id: str, indicators: dict[str, int]) -> str:
    """Insert indicators for an event."""
    indicator_id = generate_id()
    conn.execute("""
        INSERT INTO indicators (
            indicator_id, event_id, physical_disruption, transport_impact,
            policy_sanctions, market_transmission, escalation_risk
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        indicator_id,
        event_id,
        indicators.get('physical_disruption', 0),
        indicators.get('transport_impact', 0),
        indicators.get('policy_sanctions', 0),
        indicators.get('market_transmission', 0),
        indicators.get('escalation_risk', 0)
    ))
    return indicator_id


def insert_flags(conn: sqlite3.Connection, event_id: str, flags: dict[str, bool]) -> str:
    """Insert flags for an event."""
    flag_id = generate_id()
    conn.execute("""
        INSERT INTO flags (
            flag_id, event_id, confirmed_supply_disruption,
            strategic_transport_disruption, major_sanctions_escalation, military_escalation
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        flag_id,
        event_id,
        1 if flags.get('confirmed_supply_disruption') else 0,
        1 if flags.get('strategic_transport_disruption') else 0,
        1 if flags.get('major_sanctions_escalation') else 0,
        1 if flags.get('military_escalation') else 0
    ))
    return flag_id


def insert_notification(
    conn: sqlite3.Connection,
    event_id: str,
    notification_type: str,
    content: str,
    file_path: str | None = None
) -> str:
    """Insert notification for an event."""
    notification_id = generate_id()
    now = now_iso()
    conn.execute("""
        INSERT INTO notifications (notification_id, event_id, notification_type, file_path, content, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (notification_id, event_id, notification_type, file_path, content, now))
    return notification_id


# Statistics

def insert_watchlist_item(conn: sqlite3.Connection, event_id: str, company_name: str, ticker: str, sector: str) -> str:
    """
    Insert a watchlist item for an event.
    
    Args:
        conn: Database connection
        event_id: Event ID
        company_name: Company name
        ticker: Stock ticker
        sector: Industry sector
        
    Returns:
        watchlist_id
    """
    watchlist_id = generate_id()
    conn.execute("""
        INSERT INTO watchlist (watchlist_id, event_id, company_name, ticker, sector)
        VALUES (?, ?, ?, ?, ?)
    """, (watchlist_id, event_id, company_name, ticker, sector))
    return watchlist_id


def get_watchlist_by_event(conn: sqlite3.Connection, event_id: str) -> list[dict[str, Any]]:
    """Get watchlist items for an event."""
    cursor = conn.execute("SELECT * FROM watchlist WHERE event_id = ?", (event_id,))
    return [dict(row) for row in cursor.fetchall()]


def get_stats(conn: sqlite3.Connection) -> dict[str, Any]:
    """Get database statistics."""
    stats = {}
    
    cursor = conn.execute("SELECT COUNT(*) FROM events")
    stats['total_events'] = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM events WHERE band = 'full_analysis'")
    stats['full_analysis_events'] = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM events WHERE band = 'monitor'")
    stats['monitor_events'] = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM notifications")
    stats['total_notifications'] = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM watchlist")
    stats['total_watchlist_items'] = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT DISTINCT region FROM events")
    stats['regions'] = [row[0] for row in cursor.fetchall()]
    
    cursor = conn.execute("SELECT DISTINCT category FROM events")
    stats['categories'] = [row[0] for row in cursor.fetchall()]
    
    return stats


if __name__ == "__main__":
    # Example usage
    import os
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Initialize database
        init_database(db_path)
        print(f"Database initialized: {db_path}")
        
        # Connect and insert sample data
        conn = connect_db(db_path)
        try:
            event = {
                'event_key': 'test-event-001',
                'event_title': 'Test Event',
                'date_detected': '2024-01-15',
                'region': 'Test Region',
                'category': 'Test Category',
                'summary': 'Test summary',
                'score': 5,
                'band': 'monitor',
                'trigger_full_analysis': False
            }
            event_id = insert_event(conn, event)
            conn.commit()
            print(f"Inserted event: {event_id}")
            
            # Get stats
            stats = get_stats(conn)
            print(f"Stats: {stats}")
            
        finally:
            conn.close()
