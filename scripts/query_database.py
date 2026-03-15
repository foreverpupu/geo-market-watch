#!/usr/bin/env python3
"""
Geo Market Watch v6 — Query Database

Query and display events from the Geo Alpha Database.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.database import connect_db, list_events, search_events, get_stats
from engine.dashboard_views import (
    get_tracked_ideas, get_closed_ideas, get_performance_summary
)
from engine.export_layer import build_idea_performance_view, build_performance_summary_view


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
    
    # Performance tracking flags
    parser.add_argument(
        '--idea-performance',
        action='store_true',
        help='Show idea performance data'
    )
    
    parser.add_argument(
        '--performance-summary',
        action='store_true',
        help='Show performance summary statistics'
    )
    
    parser.add_argument(
        '--tracked-ideas',
        action='store_true',
        help='Show currently tracked ideas'
    )
    
    parser.add_argument(
        '--closed-ideas',
        action='store_true',
        help='Show closed ideas with performance'
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
        
        elif args.idea_performance:
            conn_db = connect_db(args.db)
            data = build_idea_performance_view(conn_db, args.limit)
            conn_db.close()
            
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("=" * 120)
                print("Idea Performance")
                print("=" * 120)
                print(f"\nTotal: {len(data)} records\n")
                
                if data:
                    print(f"{'Company':<20} {'Ticker':<10} {'Dir':<6} {'Status':<10} {'Entry':<10} {'Close':<10} {'Return %':<10} {'Outcome':<12} {'Days':<5}")
                    print("-" * 120)
                    
                    for item in data:
                        company = item.get('company_name', 'N/A')[:18]
                        ticker = item.get('ticker', 'N/A')[:8]
                        direction = item.get('direction', 'N/A')[:4]
                        status = item.get('tracking_status', 'N/A')[:8]
                        entry = f"{item['entry_price']:.2f}" if item.get('entry_price') else "-"
                        close = f"{item['close_price']:.2f}" if item.get('close_price') else "-"
                        ret = f"{item['return_pct']:.2f}%" if item.get('return_pct') is not None else "-"
                        outcome = (item.get('outcome') or '-').upper()[:10]
                        days = str(item['holding_period_days']) if item.get('holding_period_days') is not None else "-"
                        
                        print(f"{company:<20} {ticker:<10} {direction:<6} {status:<10} {entry:<10} {close:<10} {ret:<10} {outcome:<12} {days:<5}")
                else:
                    print("No performance records found.")
                print()
        
        elif args.performance_summary:
            conn_db = connect_db(args.db)
            summary = build_performance_summary_view(conn_db)
            conn_db.close()
            
            if args.json:
                print(json.dumps(summary, indent=2))
            else:
                print("=" * 60)
                print("Performance Summary")
                print("=" * 60)
                print(f"Tracked Count: {summary.get('tracked_count', 0)}")
                print(f"Closed Count: {summary.get('closed_count', 0)}")
                print(f"Positive Count: {summary.get('positive_count', 0)}")
                print(f"Negative Count: {summary.get('negative_count', 0)}")
                print(f"Average Return: {summary.get('average_return_pct', 0):.2f}%")
                print(f"Average Alpha: {summary.get('average_alpha_spread_pct') or 'N/A'}")
                
                if summary.get('outcome_distribution'):
                    print("\nOutcome Distribution:")
                    for outcome, count in summary['outcome_distribution'].items():
                        print(f"  {outcome}: {count}")
                
                if summary.get('by_direction'):
                    print("\nBy Direction:")
                    for item in summary['by_direction']:
                        print(f"  {item['direction']}: {item['count']} trades, avg {item['avg_return']:.2f}%")
                print()
        
        elif args.tracked_ideas:
            data = get_tracked_ideas(args.db)
            
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("=" * 100)
                print("Tracked Ideas")
                print("=" * 100)
                print(f"\nTotal: {len(data)} ideas\n")
                
                if data:
                    print(f"{'Company':<20} {'Ticker':<10} {'Dir':<6} {'Status':<10} {'Entry':<10} {'Close':<10} {'Return %':<10} {'Outcome':<10}")
                    print("-" * 100)
                    
                    for item in data:
                        company = item.get('company_name', 'N/A')[:18]
                        ticker = item.get('ticker', 'N/A')[:8]
                        direction = item.get('direction', 'N/A')[:4]
                        status = item.get('tracking_status', 'N/A')[:8]
                        entry = f"{item['entry_price']:.2f}" if item.get('entry_price') else "-"
                        close = f"{item['close_price']:.2f}" if item.get('close_price') else "-"
                        ret = f"{item['return_pct']:.2f}%" if item.get('return_pct') is not None else "-"
                        outcome = (item.get('outcome') or '-').upper()[:8]
                        
                        print(f"{company:<20} {ticker:<10} {direction:<6} {status:<10} {entry:<10} {close:<10} {ret:<10} {outcome:<10}")
                else:
                    print("No tracked ideas found.")
                print()
        
        elif args.closed_ideas:
            data = get_closed_ideas(args.db)
            
            if args.json:
                print(json.dumps(data, indent=2))
            else:
                print("=" * 120)
                print("Closed Ideas")
                print("=" * 120)
                print(f"\nTotal: {len(data)} ideas\n")
                
                if data:
                    print(f"{'Company':<20} {'Ticker':<10} {'Dir':<6} {'Entry':<10} {'Close':<10} {'Return %':<10} {'Benchmark':<10} {'Alpha':<10} {'Outcome':<10} {'Days':<5}")
                    print("-" * 120)
                    
                    for item in data:
                        company = item.get('company_name', 'N/A')[:18]
                        ticker = item.get('ticker', 'N/A')[:8]
                        direction = item.get('direction', 'N/A')[:4]
                        entry = f"{item['entry_price']:.2f}" if item.get('entry_price') else "-"
                        close = f"{item['close_price']:.2f}" if item.get('close_price') else "-"
                        ret = f"{item['return_pct']:.2f}%" if item.get('return_pct') is not None else "-"
                        benchmark = f"{item['benchmark_return_pct']:.2f}%" if item.get('benchmark_return_pct') is not None else "-"
                        alpha = f"{item['alpha_spread_pct']:.2f}%" if item.get('alpha_spread_pct') is not None else "-"
                        outcome = (item.get('outcome') or '-').upper()[:8]
                        days = str(item['holding_period_days']) if item.get('holding_period_days') is not None else "-"
                        
                        print(f"{company:<20} {ticker:<10} {direction:<6} {entry:<10} {close:<10} {ret:<10} {benchmark:<10} {alpha:<10} {outcome:<10} {days:<5}")
                else:
                    print("No closed ideas found.")
                print()
        
        else:
            parser.print_help()
        
        conn.close()
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
