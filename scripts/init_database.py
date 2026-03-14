#!/usr/bin/env python3
"""
Geo Market Watch v6 — Initialize Database

Creates the Geo Alpha Database with all required tables.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from database import init_database


def main():
    parser = argparse.ArgumentParser(
        description='Initialize Geo Alpha Database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/init_database.py --db data/geo_alpha.db
        """
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file (default: data/geo_alpha.db)'
    )
    
    args = parser.parse_args()
    
    # Ensure directory exists
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        init_database(str(db_path))
        print(f"✓ Database initialized: {db_path}")
        print(f"  Tables created: events, sources, indicators, flags, notifications, watchlist")
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
