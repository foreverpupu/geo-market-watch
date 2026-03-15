#!/usr/bin/env python3
"""
Geo Market Watch v6.4 — Close Trade Idea CLI

Close paper trading tracking and compute performance.

Usage:
    python scripts/close_trade_idea.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --close-price 79.10 \
        --close-time 2026-03-29T16:00:00Z \
        --notes "Closed after event de-escalation"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.performance_engine import close_tracking


def main():
    parser = argparse.ArgumentParser(
        description="Close tracking for a trade idea and compute performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Close tracking
    python scripts/close_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --close-price 79.10 \\
        --close-time 2026-03-29T16:00:00Z

    # With notes
    python scripts/close_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --close-price 79.10 \\
        --close-time 2026-03-29T16:00:00Z \\
        --notes "Target reached, thesis complete"
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
        help="Trade idea ID to close"
    )
    parser.add_argument(
        "--close-price",
        type=float,
        required=True,
        help="Close price (must be positive)"
    )
    parser.add_argument(
        "--close-time",
        required=True,
        help="Close timestamp (ISO format, e.g., 2026-03-29T16:00:00Z)"
    )
    parser.add_argument(
        "--notes",
        help="Optional close notes"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Validate close price
    if args.close_price <= 0:
        print("Error: Close price must be positive")
        sys.exit(1)
    
    # Close tracking
    success, message, result = close_tracking(
        db_path=str(db_path),
        trade_idea_id=args.idea_id,
        close_price=args.close_price,
        close_time=args.close_time,
        notes=args.notes
    )
    
    if success and result:
        print(f"✓ {message}")
        print(f"\nPerformance Summary:")
        print(f"  Trade Idea: {args.idea_id}")
        print(f"  Entry Price: {result['entry_price']}")
        print(f"  Close Price: {result['close_price']}")
        print(f"  Return: {result['return_pct']:.2f}%")
        print(f"  Outcome: {result['outcome'].upper()}")
        print(f"  Holding Period: {result['holding_period_days']} days")
        if args.notes:
            print(f"  Notes: {args.notes}")
        sys.exit(0)
    else:
        print(f"✗ Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
