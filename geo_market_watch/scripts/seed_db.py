#!/usr/bin/env python3
"""
Geo Market Watch — Seed Database CLI

Seeds the Geo Alpha Database with sample events.
"""

import argparse
import json
import sys
from pathlib import Path

from geo_market_watch.database import (
    connect_db,
    init_database,
    insert_event,
    insert_flags,
    insert_indicators,
    insert_source,
)


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
        events = json.load(f)
    
    conn = connect_db(db_path)
    count = 0
    
    try:
        for event in events:
            # Insert source
            if event.get('source'):
                insert_source(conn, event['source'])
            
            # Insert event
            event_id = insert_event(conn, event)
            
            # Insert indicators
            if event.get('indicators'):
                insert_indicators(conn, event_id, event['indicators'])
            
            # Insert flags
            if event.get('flags'):
                insert_flags(conn, event_id, event['flags'])
            
            count += 1
        
        conn.commit()
        return count
        
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Seed Geo Alpha Database with sample events',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gmw-seed-db --db data/geo_alpha.db --seed data/seed-events.json
        """
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file (default: data/geo_alpha.db)'
    )
    
    parser.add_argument(
        '--seed', '-s',
        required=True,
        help='Path to seed JSON file'
    )
    
    args = parser.parse_args()
    
    # Validate seed file exists
    if not Path(args.seed).exists():
        print(f"✗ Seed file not found: {args.seed}", file=sys.stderr)
        return 1
    
    try:
        count = seed_events(args.db, args.seed)
        print(f"✓ Seeded {count} events into {args.db}")
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
