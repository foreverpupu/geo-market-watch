#!/usr/bin/env python3
"""
Geo Market Watch v6.3 — List Active Ideas CLI

List approved and active trade ideas.
"""

import argparse
import sqlite3
from typing import List, Dict, Any


def get_active_ideas(db_path: str) -> List[Dict[str, Any]]:
    """Get approved active trade ideas."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute(
            """
            SELECT 
                ti.trade_idea_id,
                ti.event_id,
                e.event_title,
                ti.company_name,
                ti.ticker,
                ti.sector,
                ti.direction,
                ti.conviction,
                ti.analyst_status,
                ti.created_at
            FROM trade_ideas ti
            JOIN events e ON ti.event_id = e.event_id
            WHERE ti.analyst_status = 'approved'
            ORDER BY 
                CASE ti.conviction 
                    WHEN 'high' THEN 1 
                    WHEN 'medium' THEN 2 
                    WHEN 'low' THEN 3 
                    ELSE 4 
                END,
                ti.created_at DESC
            """
        )
        
        return [dict(row) for row in cursor.fetchall()]
        
    finally:
        conn.close()


def format_table(ideas: List[Dict[str, Any]]) -> str:
    """Format ideas as markdown table."""
    if not ideas:
        return "No active approved trade ideas."
    
    lines = [
        "| Event | Company | Ticker | Direction | Conviction | Status |",
        "|-------|---------|--------|-----------|------------|--------|"
    ]
    
    for idea in ideas:
        event = idea.get('event_title', 'Unknown')[:30]
        company = idea.get('company_name', 'Unknown')
        ticker = idea.get('ticker', '-')
        direction = idea.get('direction', '-')
        conviction = idea.get('conviction', '-')
        status = idea.get('analyst_status', '-')
        
        lines.append(f"| {event}... | {company} | {ticker} | {direction} | {conviction} | {status} |")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List active approved trade ideas"
    )
    parser.add_argument(
        "--db",
        default="data/geo_alpha.db",
        help="Path to SQLite database"
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    ideas = get_active_ideas(args.db)
    
    if args.format == "json":
        import json
        print(json.dumps(ideas, indent=2))
    else:
        print(f"Active Approved Trade Ideas: {len(ideas)}")
        print()
        print(format_table(ideas))


if __name__ == "__main__":
    main()
