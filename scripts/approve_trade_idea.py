#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Approve Trade Idea CLI

Quick approval shortcut for trade ideas.

Usage:
    python scripts/approve_trade_idea.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --reviewer analyst1 \
        --confidence high \
        --notes "Strong thesis, clear catalyst"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.idea_review_engine import submit_review


def main():
    parser = argparse.ArgumentParser(
        description="Quickly approve a trade idea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Quick approve
    python scripts/approve_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --reviewer amy

    # Approve with confidence and notes
    python scripts/approve_trade_idea.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --reviewer amy \\
        --confidence high --notes "Strong thesis"
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
        help="Trade idea ID to approve"
    )
    parser.add_argument(
        "--reviewer",
        required=True,
        help="Name/ID of the reviewer"
    )
    parser.add_argument(
        "--confidence",
        choices=["low", "medium", "high"],
        default="medium",
        help="Confidence level (default: medium)"
    )
    parser.add_argument(
        "--notes",
        help="Approval notes (optional)"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Submit approval
    success, message = submit_review(
        db_path=str(db_path),
        trade_idea_id=args.idea_id,
        reviewer=args.reviewer,
        decision="approve",
        confidence=args.confidence,
        notes=args.notes
    )
    
    if success:
        print(f"✓ Approved: {message}")
        sys.exit(0)
    else:
        print(f"✗ Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
