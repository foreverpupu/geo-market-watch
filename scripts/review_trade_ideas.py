#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Review Trade Ideas CLI

Submit analyst reviews for trade ideas.

Usage:
    python scripts/review_trade_ideas.py \
        --db data/geo_alpha.db \
        --idea-id TRADE_ID \
        --reviewer analyst1 \
        --decision approve \
        --confidence medium \
        --notes "Energy price risk justified"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.idea_review_engine import submit_review


def main():
    parser = argparse.ArgumentParser(
        description="Submit analyst review for a trade idea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Approve an idea
    python scripts/review_trade_ideas.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --reviewer amy --decision approve --confidence high

    # Reject with notes
    python scripts/review_trade_ideas.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --reviewer amy --decision reject \\
        --notes "Insufficient risk/reward"

    # Monitor (no status change)
    python scripts/review_trade_ideas.py --db data/geo_alpha.db \\
        --idea-id TRADE_ID --reviewer amy --decision monitor
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
        help="Trade idea ID to review"
    )
    parser.add_argument(
        "--reviewer",
        required=True,
        help="Name/ID of the reviewer"
    )
    parser.add_argument(
        "--decision",
        required=True,
        choices=["approve", "monitor", "reject", "needs_revision"],
        help="Review decision"
    )
    parser.add_argument(
        "--confidence",
        choices=["low", "medium", "high"],
        help="Confidence level (optional)"
    )
    parser.add_argument(
        "--notes",
        help="Review notes (optional)"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Submit review
    success, message = submit_review(
        db_path=str(db_path),
        trade_idea_id=args.idea_id,
        reviewer=args.reviewer,
        decision=args.decision,
        confidence=args.confidence,
        notes=args.notes
    )
    
    if success:
        print(f"✓ {message}")
        sys.exit(0)
    else:
        print(f"✗ Error: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
