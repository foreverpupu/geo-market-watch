#!/usr/bin/env python3
"""
Geo Market Watch v6.4 — Update Idea Price Reference CLI

Update entry or close price references for tracked ideas.

Usage:
    # Update entry reference
    python scripts/update_idea_price_reference.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --field entry \
        --price 73.00 \
        --time 2026-03-15T09:30:00Z \
        --notes "Corrected entry reference"

    # Update close reference
    python scripts/update_idea_price_reference.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --field close \
        --price 78.80 \
        --time 2026-03-29T16:00:00Z \
        --notes "Corrected close reference"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.performance_engine import get_performance_record, recompute_performance
import sqlite3
from datetime import datetime, timezone


def get_db_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    parser = argparse.ArgumentParser(
        description="Update price reference for a tracked trade idea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Update entry reference
    python scripts/update_idea_price_reference.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --field entry --price 73.00 \\
        --time 2026-03-15T09:30:00Z --notes "Corrected entry"

    # Update close reference
    python scripts/update_idea_price_reference.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --field close --price 78.80 \\
        --time 2026-03-29T16:00:00Z --notes "Corrected close"
        """
    )
    
    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database"
    )
    parser.add_argument(
        "--idea-id",
        required=True,
        help="Trade idea ID to update"
    )
    parser.add_argument(
        "--field",
        required=True,
        choices=["entry", "close"],
        help="Which field to update (entry or close)"
    )
    parser.add_argument(
        "--price",
        type=float,
        required=True,
        help="New price value (must be positive)"
    )
    parser.add_argument(
        "--time",
        required=True,
        help="New timestamp (ISO format)"
    )
    parser.add_argument(
        "--notes",
        required=True,
        help="Required: reason for correction"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Validate price
    if args.price <= 0:
        print("Error: Price must be positive")
        sys.exit(1)
    
    # Check if tracking record exists
    perf = get_performance_record(str(db_path), args.idea_id)
    if not perf:
        print(f"Error: No tracking record found for {args.idea_id}")
        sys.exit(1)
    
    try:
        conn = get_db_connection(str(db_path))
        cursor = conn.cursor()
        
        now = datetime.now(timezone.utc).isoformat()
        
        if args.field == "entry":
            # Validate that close time (if exists) is not earlier than new entry time
            if perf.get('close_time'):
                entry_dt = datetime.fromisoformat(args.time.replace('Z', '+00:00'))
                close_dt = datetime.fromisoformat(perf['close_time'].replace('Z', '+00:00'))
                if close_dt < entry_dt:
                    print("Error: Close time would be earlier than new entry time")
                    sys.exit(1)
            
            cursor.execute(
                """
                UPDATE trade_idea_performance
                SET entry_price = ?, entry_time = ?, notes = ?, updated_at = ?
                WHERE trade_idea_id = ?
                """,
                (args.price, args.time, args.notes, now, args.idea_id)
            )
        else:  # close
            # Validate that new close time is not earlier than entry time
            if perf.get('entry_time'):
                entry_dt = datetime.fromisoformat(perf['entry_time'].replace('Z', '+00:00'))
                close_dt = datetime.fromisoformat(args.time.replace('Z', '+00:00'))
                if close_dt < entry_dt:
                    print("Error: Close time must not be earlier than entry time")
                    sys.exit(1)
            
            cursor.execute(
                """
                UPDATE trade_idea_performance
                SET close_price = ?, close_time = ?, notes = ?, updated_at = ?
                WHERE trade_idea_id = ?
                """,
                (args.price, args.time, args.notes, now, args.idea_id)
            )
        
        conn.commit()
        conn.close()
        
        # Recompute performance if both entry and close exist
        recompute_performance(str(db_path), args.idea_id)
        
        print(f"✓ Updated {args.field} reference for {args.idea_id}")
        print(f"\nUpdate Summary:")
        print(f"  Field: {args.field}")
        print(f"  New Price: {args.price}")
        print(f"  New Time: {args.time}")
        print(f"  Notes: {args.notes}")
        
        # Show updated performance if available
        updated_perf = get_performance_record(str(db_path), args.idea_id)
        if updated_perf and updated_perf.get('return_pct') is not None:
            print(f"\nUpdated Performance:")
            print(f"  Return: {updated_perf['return_pct']:.2f}%")
            print(f"  Outcome: {updated_perf.get('outcome', 'N/A')}")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
