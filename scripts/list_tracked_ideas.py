#!/usr/bin/env python3
"""
Geo Market Watch v6.4 — List Tracked Ideas CLI

List tracked trade ideas with performance summary.

Usage:
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db --status tracking
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db --json
"""

import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.performance_engine import list_tracked_ideas


def format_idea(idea: dict) -> str:
    """Format a tracked idea for display."""
    lines = [
        f"  Company: {idea.get('company_name', 'N/A')} ({idea.get('ticker', 'N/A')})",
        f"  Direction: {idea.get('direction', 'N/A')}",
        f"  Status: {idea.get('tracking_status', 'N/A')}",
    ]
    
    if idea.get('entry_price'):
        lines.append(f"  Entry: {idea['entry_price']}")
    if idea.get('close_price'):
        lines.append(f"  Close: {idea['close_price']}")
    if idea.get('return_pct') is not None:
        lines.append(f"  Return: {idea['return_pct']:.2f}%")
    if idea.get('outcome'):
        lines.append(f"  Outcome: {idea['outcome'].upper()}")
    if idea.get('holding_period_days') is not None:
        lines.append(f"  Holding Days: {idea['holding_period_days']}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List tracked trade ideas with performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all tracked ideas
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db

    # List only currently tracking
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db --status tracking

    # List only closed
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db --status closed

    # Output as JSON
    python scripts/list_tracked_ideas.py --db data/geo_alpha.db --json
        """
    )
    
    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database"
    )
    parser.add_argument(
        "--status",
        choices=["tracking", "closed", "not_started"],
        help="Filter by tracking status"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Get tracked ideas
    ideas = list_tracked_ideas(str(db_path), args.status)
    
    # Output
    if args.json:
        print(json.dumps(ideas, indent=2))
    else:
        title = f"Tracked Ideas: {args.status}" if args.status else "Tracked Trade Ideas"
        print(title)
        print("=" * 70)
        
        if not ideas:
            print("\nNo tracked ideas found.")
        else:
            # Print table header
            print(f"\n{'Company':<20} {'Ticker':<10} {'Dir':<6} {'Status':<10} {'Entry':<10} {'Close':<10} {'Return %':<10} {'Outcome':<10} {'Days':<5}")
            print("-" * 95)
            
            for idea in ideas:
                company = idea.get('company_name', 'N/A')[:18]
                ticker = idea.get('ticker', 'N/A')[:8]
                direction = idea.get('direction', 'N/A')[:4]
                status = idea.get('tracking_status', 'N/A')[:8]
                entry = f"{idea['entry_price']:.2f}" if idea.get('entry_price') else "-"
                close = f"{idea['close_price']:.2f}" if idea.get('close_price') else "-"
                ret = f"{idea['return_pct']:.2f}%" if idea.get('return_pct') is not None else "-"
                outcome = (idea.get('outcome') or '-').upper()[:8]
                days = str(idea['holding_period_days']) if idea.get('holding_period_days') is not None else "-"
                
                print(f"{company:<20} {ticker:<10} {direction:<6} {status:<10} {entry:<10} {close:<10} {ret:<10} {outcome:<10} {days:<5}")
        
        print(f"\nTotal: {len(ideas)} ideas")


if __name__ == "__main__":
    main()
