#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — Review Trade Ideas CLI

Submit analyst reviews for trade ideas.
"""

import argparse
import sys
from engine.idea_review_engine import submit_review


def main():
    parser = argparse.ArgumentParser(
        description="Review trade ideas in Geo Market Watch"
    )
    parser.add_argument(
        "--db",
        default="data/geo_alpha.db",
        help="Path to SQLite database"
    )
    parser.add_argument(
        "--idea-id",
        required=True,
        help="Trade idea ID to review"
    )
    parser.add_argument(
        "--reviewer",
        required=True,
        help="Reviewer name/ID"
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
        help="Reviewer confidence level"
    )
    parser.add_argument(
        "--notes",
        help="Review notes (required for reject/needs_revision)"
    )
    
    args = parser.parse_args()
    
    # Submit review
    success, error, review = submit_review(
        db_path=args.db,
        trade_idea_id=args.idea_id,
        reviewer=args.reviewer,
        decision=args.decision,
        confidence=args.confidence,
        notes=args.notes
    )
    
    if not success:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Review submitted successfully")
    print(f"  Review ID: {review['review_id']}")
    print(f"  Trade Idea: {review['trade_idea_id']}")
    print(f"  Decision: {review['decision']}")
    print(f"  Reviewer: {review['reviewer']}")
    if review['confidence']:
        print(f"  Confidence: {review['confidence']}")
    if review['notes']:
        print(f"  Notes: {review['notes'][:100]}...")


if __name__ == "__main__":
    main()
