#!/usr/bin/env python3
"""
Geo Market Watch v6.4 — Start Idea Tracking CLI

Start paper trading tracking for an approved trade idea.

Usage:
    python scripts/start_idea_tracking.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --entry-price 72.50 \
        --entry-time 2026-03-15T09:30:00Z \
        --notes "Tracking started after analyst approval"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.performance_engine import start_tracking


def main():
    parser = argparse.ArgumentParser(
        description="Start tracking performance for an approved trade idea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Start tracking
    python scripts/start_idea_tracking.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --entry-price 72.50 \\
        --entry-time 2026-03-15T09:30:00Z

    # With notes
    python scripts/start_idea_tracking.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --entry-price 72.50 \\
        --entry-time 2026-03-15T09:30:00Z \\
        --notes "Strong momentum confirmed"
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
        help="Trade idea ID to track"
    )
    parser.add_argument(
        "--entry-price",
        type=float,
        required=True,
        help="Entry price (must be positive)"
    )
    parser.add_argument(
        "--entry-time",
        required=True,
        help="Entry timestamp (ISO format, e.g., 2026-03-15T09:30:00Z)"
    )
    parser.add_argument(
        "--notes",
        help="Optional tracking notes"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Validate entry price
    if args.entry_price <= 0:
        print("Error: Entry price must be positive")
        sys.exit(1)
    
    # Start tracking
    success, message = start_tracking(
        db_path=str(db_path),
        trade_idea_id=args.idea_id,
        entry_price=args.entry_price,
        entry_time=args.entry_time,
        notes=args.notes
    )
    
    if success:
        print(f"✓ {message}")
        print(f"\nTracking Summary:")
        print(f"  Trade Idea: {args.idea_id}")
        print(f"  Entry Price: {args.entry_price}")
        print(f"  Entry Time: {args.entry_time}")
        if args.notes:
            print(f"  Notes: {args.notes}")
        sys.exit(0)
    else:
        print(f"✗ Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
