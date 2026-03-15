#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Approve Trade Idea CLI

Quick approval script for trade ideas.
"""

import argparse
import sys
from engine.idea_review_engine import submit_review


def main():
    parser = argparse.ArgumentParser(
        description="Approve a trade idea in Geo Market Watch"
    )
    parser.add_argument(
        "--db",
        default="data/geo_alpha.db",
        help="Path to SQLite database"
    )
    parser.add_argument(
        "--idea-id",
        required=True,
        help="Trade idea ID to approve"
    )
    parser.add_argument(
        "--reviewer",
        required=True,
        help="Reviewer name/ID"
    )
    parser.add_argument(
        "--confidence",
        default="medium",
        choices=["low", "medium", "high"],
        help="Reviewer confidence level"
    )
    parser.add_argument(
        "--notes",
        help="Optional approval notes"
    )
    
    args = parser.parse_args()
    
    # Submit approval
    success, error, review = submit_review(
        db_path=args.db,
        trade_idea_id=args.idea_id,
        reviewer=args.reviewer,
        decision="approve",
        confidence=args.confidence,
        notes=args.notes
    )
    
    if not success:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Trade idea approved")
    print(f"  Trade Idea: {args.idea_id}")
    print(f"  Reviewer: {args.reviewer}")
    print(f"  Confidence: {args.confidence}")


if __name__ == "__main__":
    main()
