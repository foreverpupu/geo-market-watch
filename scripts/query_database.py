#!/usr/bin/env python3
"""
Geo Market Watch v6 — Query Database

Query and display events from the Geo Alpha Database.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from database import connect_db, list_events, search_events, get_stats


def format_event(event: dict) -> str:
    """Format event for display."""
    trigger = "→ Full Analysis" if event.get('trigger_full_analysis') else "→ Monitor"
    return (
        f"  [{event.get('event_id', 'N/A')[:8]}...] "
        f"{event.get('event_title', 'Unknown')[:40]:<40} "
        f"(Score: {event.get('score', 'N/A'):>2}, Band: {event.get('band', 'N/A'):<13}) {trigger}"
    )


def main():
    parser = argparse.ArgumentParser(
        description='Query Geo Alpha Database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/query_database.py --db data/geo_alpha.db --list
  python scripts/query_database.py --db data/geo_alpha.db --region "Middle East"
  python scripts/query_database.py --db data/geo_alpha.db --stats
        """
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file (default: data/geo_alpha.db)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all events'
    )
    
    parser.add_argument(
        '--region', '-r',
        help='Filter by region'
    )
    
    parser.add_argument(
        '--category', '-c',
        help='Filter by category'
    )
    
    parser.add_argument(
        '--band', '-b',
        help='Filter by band (noise/monitor/full_analysis/major_shock)'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Show database statistics'
    )
    
    parser.add_argument(
        '--high-signal',
        action='store_true',
        help='Show high-signal events (score >= 7 or trigger_full_analysis = true)'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output as JSON'
    )
    
    parser.add_argument(
        '--limit', '-n',
        type=int,
        default=50,
        help='Limit number of results (default: 50)'
    )
    
    args = parser.parse_args()
    
    # Check database exists
    if not Path(args.db).exists():
        print(f"✗ Database not found: {args.db}", file=sys.stderr)
        print("  Run: python scripts/init_database.py --db " + args.db)
        return 1
    
    try:
        conn = connect_db(args.db)
        
        if args.high_signal:
            # Query high-signal events (score >= 7 OR trigger_full_analysis = true)
            cursor = conn.execute("""
                SELECT event_id, event_title, region, category, score, band, trigger_full_analysis, status
                FROM events
                WHERE score >= 7 OR trigger_full_analysis = 1
                ORDER BY score DESC, date_detected DESC
                LIMIT ?
            """, (args.limit,))
            events = [dict(row) for row in cursor.fetchall()]
            
            if args.json:
                print(json.dumps(events, indent=2))
            else:
                print("=" * 100)
                print("High-Signal Events (Score >= 7 OR Trigger Full Analysis)")
                print("=" * 100)
                print(f"\nTotal: {len(events)} events\n")
                
                if events:
                    # Print table header
                    print(f"{'Event ID':<12} {'Title':<35} {'Region':<15} {'Category':<20} {'Score':<6} {'Band':<15} {'Trigger':<8} {'Status':<10}")
                    print("-" * 100)
                    
                    for event in events:
                        event_id_short = event['event_id'][:10] if event['event_id'] else 'N/A'
                        title = (event['event_title'][:32] + '...') if event['event_title'] and len(event['event_title']) > 35 else (event['event_title'] or 'Unknown')
                        region = (event['region'][:12] + '...') if event['region'] and len(event['region']) > 15 else (event['region'] or 'Unknown')
                        category = (event['category'][:17] + '...') if event['category'] and len(event['category']) > 20 else (event['category'] or 'Unknown')
                        score = str(event['score']) if event['score'] is not None else 'N/A'
                        band = event['band'] or 'unknown'
                        trigger = 'YES' if event['trigger_full_analysis'] else 'no'
                        status = event['status'] or 'unknown'
                        
                        print(f"{event_id_short:<12} {title:<35} {region:<15} {category:<20} {score:<6} {band:<15} {trigger:<8} {status:<10}")
                else:
                    print("No high-signal events found.")
                print()
        
        elif args.stats:
            stats = get_stats(conn)
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print("=" * 60)
                print("Geo Alpha Database Statistics")
                print("=" * 60)
                print(f"Total events: {stats['total_events']}")
                print(f"Full Analysis: {stats['full_analysis_events']}")
                print(f"Monitor: {stats['monitor_events']}")
                print(f"Notifications: {stats['total_notifications']}")
                print(f"\nRegions: {', '.join(stats['regions'])}")
                print(f"Categories: {', '.join(stats['categories'])}")
        
        elif args.list or args.region or args.category or args.band:
            events = search_events(
                conn,
                region=args.region,
                category=args.category,
                band=args.band,
                limit=args.limit
            )
            
            if args.json:
                print(json.dumps(events, indent=2))
            else:
                print("=" * 60)
                print(f"Events ({len(events)} found)")
                print("=" * 60)
                for event in events:
                    print(format_event(event))
        
        else:
            parser.print_help()
        
        conn.close()
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
