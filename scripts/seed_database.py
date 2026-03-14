#!/usr/bin/env python3
"""
Geo Market Watch v6 — Seed Database

Seeds the Geo Alpha Database with sample events.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from database import connect_db, init_database, insert_event, insert_source
from database import insert_indicators, insert_flags


def seed_events(db_path: str, seed_file: str) -> int:
    """
    Seed database with events from JSON file.
    
    Args:
        db_path: Path to database
        seed_file: Path to seed JSON file
        
    Returns:
        Number of events inserted
    """
    # Ensure database exists
    if not Path(db_path).exists():
        init_database(db_path)
    
    # Load seed data
    with open(seed_file, 'r') as f:
        data = json.load(f)
    
    events = data.get('events', []) if isinstance(data, dict) else data
    
    conn = connect_db(db_path)
    inserted = 0
    
    try:
        for event in events:
            # Check if already exists
            from database import get_event_by_key
            event_key = event.get('event_key')
            if event_key and get_event_by_key(conn, event_key):
                print(f"  Skipping (exists): {event.get('event_title', 'Unknown')}")
                continue
            
            # Insert event
            event_id = insert_event(conn, event)
            
            # Insert source
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
            
            inserted += 1
            print(f"  Inserted: {event.get('event_title', 'Unknown')}")
        
        conn.commit()
        
    finally:
        conn.close()
    
    return inserted


def main():
    parser = argparse.ArgumentParser(
        description='Seed Geo Alpha Database with sample events',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/seed_database.py --db data/geo_alpha.db --seed data/db-seed-events.json
        """
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file (default: data/geo_alpha.db)'
    )
    
    parser.add_argument(
        '--seed', '-s',
        default='data/db-seed-events.json',
        help='Path to seed JSON file (default: data/db-seed-events.json)'
    )
    
    args = parser.parse_args()
    
    # Check seed file exists
    if not Path(args.seed).exists():
        print(f"✗ Seed file not found: {args.seed}", file=sys.stderr)
        return 1
    
    try:
        count = seed_events(args.db, args.seed)
        print(f"\n✓ Seeded {count} events into {args.db}")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
