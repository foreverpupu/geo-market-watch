#!/usr/bin/env python3
"""
Geo Market Watch v6.4 — Export Dashboard Data CLI

Export dashboard and performance data to JSON and CSV files.

Usage:
    python scripts/export_dashboard_data.py --db data/geo_alpha.db --output exports/
    python scripts/export_dashboard_data.py --db data/geo_alpha.db --output exports/ --timestamp 20260315
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.export_layer import export_dashboard_data


def main():
    parser = argparse.ArgumentParser(
        description="Export dashboard data to JSON and CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Export with auto timestamp
    python scripts/export_dashboard_data.py --db data/geo_alpha.db --output exports/

    # Export with specific timestamp
    python scripts/export_dashboard_data.py --db data/geo_alpha.db \\
        --output exports/ --timestamp 20260315

    # Export to current directory
    python scripts/export_dashboard_data.py --db data/geo_alpha.db --output .
        """
    )
    
    parser.add_argument(
        "--db",
        required=True,
        help="Path to the SQLite database"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for exported files"
    )
    parser.add_argument(
        "--timestamp",
        help="Optional timestamp for filenames (default: auto-generated)"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {args.db}")
        sys.exit(1)
    
    # Export data
    results = export_dashboard_data(
        db_path=str(db_path),
        output_dir=args.output,
        timestamp=args.timestamp
    )
    
    # Report results
    print("Export Results")
    print("=" * 50)
    
    all_success = all(results.values())
    
    for name, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
    
    print()
    if all_success:
        print(f"✓ All exports successful to: {args.output}")
        print("\nGenerated files:")
        print("  • idea_performance_latest.json")
        print("  • idea_performance_latest.csv")
        print("  • idea_performance_summary.json")
        print("  • Timestamped versions")
        sys.exit(0)
    else:
        print("✗ Some exports failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
