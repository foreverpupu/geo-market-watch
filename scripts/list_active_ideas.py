#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — List Active Ideas CLI

List and filter active trade ideas.

Usage:
    python scripts/list_active_ideas.py --db data/geo_alpha.db
    python scripts/list_active_ideas.py --db data/geo_alpha.db --status pending_review
    python scripts/list_active_ideas.py --db data/geo_alpha.db --all
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.lifecycle_engine import get_active_ideas, get_ideas_by_status, get_lifecycle_history
from engine.idea_review_engine import get_pending_reviews, get_review_statistics
from engine.dashboard_views import (
    get_approved_trade_ideas, 
    get_pending_trade_ideas, 
    get_invalidated_trade_ideas,
    get_dashboard_snapshot
)


def format_idea(idea: dict) -> str:
    """Format a trade idea for display."""
    lines = [
        f"  Trade ID: {idea.get('trade_idea_id', 'N/A')}",
        f"  Company: {idea.get('company_name', 'N/A')} ({idea.get('ticker', 'N/A')})",
        f"  Sector: {idea.get('sector', 'N/A')}",
        f"  Direction: {idea.get('direction', 'N/A')} | Conviction: {idea.get('conviction', 'N/A')}",
        f"  Status: {idea.get('analyst_status', 'N/A')} | Approval: {idea.get('approval_status', 'N/A')}",
    ]
    
    if idea.get('thesis'):
        thesis = idea['thesis'][:100] + "..." if len(idea['thesis']) > 100 else idea['thesis']
        lines.append(f"  Thesis: {thesis}")
    
    lines.append(f"  Created: {idea.get('created_at', 'N/A')}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List active trade ideas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all active ideas
    python scripts/list_active_ideas.py --db data/geo_alpha.db

    # List pending reviews
    python scripts/list_active_ideas.py --db data/geo_alpha.db --status pending_review

    # List approved ideas
    python scripts/list_active_ideas.py --db data/geo_alpha.db --status approved

    # Show statistics
    python scripts/list_active_ideas.py --db data/geo_alpha.db --stats

    # Output as JSON
    python scripts/list_active_ideas.py --db data/geo_alpha.db --json
        """
    )
    
    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database"
    )
    parser.add_argument(
        "--status",
        choices=["pending_review", "approved", "rejected", "invalidated", "closed"],
        help="Filter by analyst status"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="List all ideas including closed/invalidated"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show review statistics"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--history",
        help="Show lifecycle history for a specific trade idea ID"
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Export full dashboard snapshot as JSON"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Show statistics
    if args.stats:
        stats = get_review_statistics(str(db_path))
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("Review Statistics")
            print("=" * 50)
            print("\nBy Analyst Status:")
            for status, count in stats.get("by_analyst_status", {}).items():
                print(f"  {status}: {count}")
            print("\nBy Approval Status:")
            for status, count in stats.get("by_approval_status", {}).items():
                print(f"  {status}: {count}")
            print(f"\nTotal Reviews Submitted: {stats.get('total_reviews_submitted', 0)}")
            print("\nReviews by Decision:")
            for decision, count in stats.get("reviews_by_decision", {}).items():
                print(f"  {decision}: {count}")
        sys.exit(0)
    
    # Show lifecycle history
    if args.history:
        history = get_lifecycle_history(str(db_path), args.history)
        if args.json:
            print(json.dumps(history, indent=2))
        else:
            print(f"Lifecycle History: {args.history}")
            print("=" * 50)
            if not history:
                print("No lifecycle events found.")
            else:
                for event in history:
                    print(f"\n  [{event.get('created_at', 'N/A')}]")
                    print(f"  Event: {event.get('event_type', 'N/A')}")
                    if event.get('event_reason'):
                        print(f"  Reason: {event.get('event_reason')}")
        sys.exit(0)
    
    # Export dashboard snapshot
    if args.snapshot:
        snapshot = get_dashboard_snapshot(str(db_path))
        print(json.dumps(snapshot, indent=2))
        sys.exit(0)
    
    # Get ideas
    if args.status:
        ideas = get_ideas_by_status(str(db_path), args.status)
        title = f"Trade Ideas: {args.status}"
    elif args.all:
        # Get all ideas - would need a new function, for now get active + rejected
        ideas = get_active_ideas(str(db_path))
        rejected = get_ideas_by_status(str(db_path), "rejected")
        invalidated = get_ideas_by_status(str(db_path), "invalidated")
        closed = get_ideas_by_status(str(db_path), "closed")
        ideas = ideas + rejected + invalidated + closed
        title = "All Trade Ideas"
    else:
        ideas = get_active_ideas(str(db_path))
        title = "Active Trade Ideas"
    
    # Output
    if args.json:
        print(json.dumps(ideas, indent=2))
    else:
        print(title)
        print("=" * 50)
        
        if not ideas:
            print("\nNo trade ideas found.")
        else:
            for i, idea in enumerate(ideas, 1):
                print(f"\n[{i}]")
                print(format_idea(idea))
        
        print(f"\nTotal: {len(ideas)} ideas")


if __name__ == "__main__":
    main()
