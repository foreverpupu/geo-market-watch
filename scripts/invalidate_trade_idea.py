#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Invalidate Trade Idea CLI

Invalidate a trade idea when the thesis no longer holds.

Usage:
    python scripts/invalidate_trade_idea.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --reason "Shipping traffic normalized, risk faded"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.lifecycle_engine import invalidate_trade_idea


def main():
    parser = argparse.ArgumentParser(
        description="Invalidate a trade idea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Invalidate due to normalized conditions
    python scripts/invalidate_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID \\
        --reason "Shipping traffic normalized"

    # Invalidate due to thesis failure
    python scripts/invalidate_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID \\
        --reason "Fertilizer supply remained stable despite disruption fears"
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
        help="Trade idea ID to invalidate"
    )
    parser.add_argument(
        "--reason",
        required=True,
        help="Reason for invalidation (required)"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Invalidate
    success, message = invalidate_trade_idea(
        db_path=str(db_path),
        trade_idea_id=args.idea_id,
        reason=args.reason
    )
    
    if success:
        print(f"✓ {message}")
        sys.exit(0)
    else:
        print(f"✗ Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
