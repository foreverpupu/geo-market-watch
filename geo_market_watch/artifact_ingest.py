"""
Geo Market Watch v6 — Artifact Ingest

Ingests v5.5 agent loop outputs into the Geo Alpha Database.
"""

import json
from pathlib import Path
from typing import Any

from geo_market_watch.database import (
    connect_db,
    init_database,
    insert_event,
    insert_flags,
    insert_indicators,
    insert_notification,
    insert_source,
)


def ingest_agent_loop_output(
    db_path: str,
    agent_output: dict[str, Any],
    notification_files: dict[str, str] = None
) -> list[str]:
    """
    Ingest agent loop output into database.
    
    Args:
        db_path: Path to SQLite database
        agent_output: Output from agent_loop.run_agent_loop()
        notification_files: Dict mapping event_key to notification file path
        
    Returns:
        List of inserted event IDs
    """
    # Ensure database exists
    if not Path(db_path).exists():
        init_database(db_path)
    
    conn = connect_db(db_path)
    inserted_ids = []
    
    try:
        for event in agent_output.get('processed_events', []):
            # Check if event already exists
            from database import get_event_by_key
            existing = get_event_by_key(conn, event.get('event_key'))
            if existing:
                # Skip duplicate
                continue
            
            # Insert main event
            event_id = insert_event(conn, event)
            inserted_ids.append(event_id)
            
            # Insert source info
            source = {
                'source_name': event.get('source_name', 'Unknown'),
                'source_url': event.get('source_url', ''),
                'published_at': event.get('date_detected')
            }
            insert_source(conn, event_id, source)
            
            # Insert indicators
            if 'indicators' in event:
                insert_indicators(conn, event_id, event['indicators'])
            
            # Insert flags
            if 'flags' in event:
                insert_flags(conn, event_id, event['flags'])
            
            # Insert notification if available
            event_key = event.get('event_key')
            if notification_files and event_key in notification_files:
                file_path = notification_files[event_key]
                try:
                    with open(file_path) as f:
                        content = f.read()
                    
                    notification_type = 'full_analysis' if event.get('trigger_full_analysis') else 'monitor'
                    insert_notification(conn, event_id, notification_type, content, file_path)
                except OSError:
                    pass  # Skip if file can't be read
        
        conn.commit()
        
    finally:
        conn.close()
    
    return inserted_ids


def ingest_json_events(db_path: str, json_path: str) -> list[str]:
    """
    Ingest events from JSON file into database.
    
    Args:
        db_path: Path to SQLite database
        json_path: Path to JSON file with events
        
    Returns:
        List of inserted event IDs
    """
    with open(json_path) as f:
        data = json.load(f)
    
    # Handle both { "items": [...] } and [...] formats
    if isinstance(data, dict) and 'items' in data:
        events = data['items']
    elif isinstance(data, list):
        events = data
    else:
        events = [data]
    
    # Ensure database exists
    if not Path(db_path).exists():
        init_database(db_path)
    
    conn = connect_db(db_path)
    inserted_ids = []
    
    try:
        for event in events:
            # Check if event already exists
            from database import get_event_by_key
            event_key = event.get('event_key')
            if event_key:
                existing = get_event_by_key(conn, event_key)
                if existing:
                    continue
            
            # Insert event
            event_id = insert_event(conn, event)
            inserted_ids.append(event_id)
            
            # Insert related data
            if 'indicators' in event:
                insert_indicators(conn, event_id, event['indicators'])
            if 'flags' in event:
                insert_flags(conn, event_id, event['flags'])
        
        conn.commit()
        
    finally:
        conn.close()
    
    return inserted_ids


if __name__ == "__main__":
    # Example usage
    import os
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "geo_alpha.db")
        
        # Sample agent output
        agent_output = {
            'processed_events': [
                {
                    'event_key': 'GMW-2024-001',
                    'event_title': 'Red Sea shipping disruption',
                    'date_detected': '2024-01-12',
                    'region': 'Middle East',
                    'category': 'Maritime disruption',
                    'summary': 'Major container lines reroute vessels.',
                    'score': 5,
                    'band': 'monitor',
                    'trigger_full_analysis': True,
                    'source_name': 'Reuters',
                    'source_url': 'https://example.com',
                    'indicators': {
                        'physical_disruption': 1,
                        'transport_impact': 2,
                        'policy_sanctions': 0,
                        'market_transmission': 1,
                        'escalation_risk': 1
                    },
                    'flags': {
                        'confirmed_supply_disruption': False,
                        'strategic_transport_disruption': True,
                        'major_sanctions_escalation': False,
                        'military_escalation': False
                    }
                }
            ]
        }
        
        # Ingest
        inserted = ingest_agent_loop_output(db_path, agent_output)
        print(f"Inserted {len(inserted)} events: {inserted}")
        
        # Verify
        from database import connect_db, get_stats
        conn = connect_db(db_path)
        stats = get_stats(conn)
        print(f"Database stats: {stats}")
        conn.close()
