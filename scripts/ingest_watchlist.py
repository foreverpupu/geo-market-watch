#!/usr/bin/env python3
"""
Geo Market Watch — Watchlist Ingest

Ingest watchlist items into the Geo Alpha Database.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from database import connect_db, insert_watchlist_item, get_event_by_key


def ingest_watchlist(db_path: str, watchlist_path: str) -> dict:
    """
    Ingest watchlist items into database.
    
    Args:
        db_path: Path to SQLite database
        watchlist_path: Path to watchlist JSON file
        
    Returns:
        Ingestion summary
    """
    # Load watchlist data
    with open(watchlist_path, 'r') as f:
        data = json.load(f)
    
    conn = connect_db(db_path)
    
    total_items = 0
    inserted_items = 0
    skipped_items = 0
    
    try:
        for event_group in data:
            event_key = event_group.get('event_key')
            watchlist = event_group.get('watchlist', [])
            
            # Find event_id by event_key
            event = get_event_by_key(conn, event_key)
            if not event:
                print(f"Warning: Event not found for key {event_key}, skipping {len(watchlist)} items")
                skipped_items += len(watchlist)
                continue
            
            event_id = event['event_id']
            
            for item in watchlist:
                total_items += 1
                
                try:
                    insert_watchlist_item(
                        conn,
                        event_id,
                        item.get('company_name'),
                        item.get('ticker'),
                        item.get('sector')
                    )
                    inserted_items += 1
                    print(f"  Inserted: {item.get('company_name')} ({item.get('ticker')})")
                except Exception as e:
                    print(f"  Error inserting {item}: {e}")
                    skipped_items += 1
        
        conn.commit()
        
    finally:
        conn.close()
    
    return {
        'total': total_items,
        'inserted': inserted_items,
        'skipped': skipped_items
    }


def main():
    parser = argparse.ArgumentParser(
        description='Ingest watchlist items into Geo Alpha Database',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file'
    )
    
    parser.add_argument(
        '--watchlist', '-w',
        required=True,
        help='Path to watchlist JSON file'
    )
    
    args = parser.parse_args()
    
    if not Path(args.watchlist).exists():
        print(f"Error: Watchlist file not found: {args.watchlist}", file=sys.stderr)
        return 1
    
    try:
        result = ingest_watchlist(args.db, args.watchlist)
        
        print(f"\n{'='*60}")
        print("Watchlist Ingestion Summary")
        print(f"{'='*60}")
        print(f"Total items: {result['total']}")
        print(f"Inserted: {result['inserted']}")
        print(f"Skipped: {result['skipped']}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
