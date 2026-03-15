#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Invalidate Trade Idea CLI

Invalidate a trade idea when conditions change.
"""

import argparse
import sys
from engine.lifecycle_engine import invalidate_trade_idea


def main():
    parser = argparse.ArgumentParser(
        description="Invalidate a trade idea in Geo Market Watch"
    )
    parser.add_argument(
        "--db",
        default="data/geo_alpha.db",
        help="Path to SQLite database"
    )
    parser.add_argument(
        "--idea-id",
        required=True,
        help="Trade idea ID to invalidate"
    )
    parser.add_argument(
        "--reason",
        required=True,
        help="Invalidation reason (required)"
    )
    
    args = parser.parse_args()
    
    # Invalidate idea
    success, error = invalidate_trade_idea(
        db_path=args.db,
        trade_idea_id=args.idea_id,
        reason=args.reason
    )
    
    if not success:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Trade idea invalidated")
    print(f"  Trade Idea: {args.idea_id}")
    print(f"  Reason: {args.reason}")


if __name__ == "__main__":
    main()
