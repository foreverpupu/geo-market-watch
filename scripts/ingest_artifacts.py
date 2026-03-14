#!/usr/bin/env python3
"""
Geo Market Watch v6 — Ingest Artifacts

Ingest v5.5 agent loop outputs into the Geo Alpha Database.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from artifact_ingest import ingest_agent_loop_output


def load_agent_output(output_path: str) -> dict:
    """Load agent loop output from JSON file."""
    with open(output_path, 'r') as f:
        return json.load(f)


def find_notification_files(output_dir: str) -> dict:
    """Find notification files in output directory."""
    notifications = {}
    output_path = Path(output_dir)
    
    if not output_path.exists():
        return notifications
    
    for file in output_path.glob('*.md'):
        # Extract event key from filename
        # Format: monitor_{band}_{event_key}.md or full_analysis_{event_key}.md
        parts = file.stem.split('_')
        if len(parts) >= 2:
            if parts[0] == 'monitor':
                event_key = '_'.join(parts[2:]) if len(parts) > 2 else parts[1]
            elif parts[0] == 'full' and parts[1] == 'analysis':
                event_key = '_'.join(parts[2:])
            else:
                continue
            notifications[event_key] = str(file)
    
    return notifications


def main():
    parser = argparse.ArgumentParser(
        description='Ingest v5.5 artifacts into Geo Alpha Database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ingest_artifacts.py --db data/geo_alpha.db --output agent_output.json
  python scripts/ingest_artifacts.py --db data/geo_alpha.db --output agent_output.json --notifications outputs/
        """
    )
    
    parser.add_argument(
        '--db', '-d',
        default='data/geo_alpha.db',
        help='Path to database file (default: data/geo_alpha.db)'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Path to agent loop output JSON file'
    )
    
    parser.add_argument(
        '--notifications', '-n',
        help='Path to notifications output directory'
    )
    
    args = parser.parse_args()
    
    # Check output file exists
    if not Path(args.output).exists():
        print(f"✗ Agent output file not found: {args.output}", file=sys.stderr)
        return 1
    
    try:
        # Load agent output
        agent_output = load_agent_output(args.output)
        
        # Find notification files
        notification_files = None
        if args.notifications:
            notification_files = find_notification_files(args.notifications)
            print(f"Found {len(notification_files)} notification files")
        
        # Ingest
        inserted = ingest_agent_loop_output(args.db, agent_output, notification_files)
        
        print(f"✓ Ingested {len(inserted)} events into {args.db}")
        for event_id in inserted:
            print(f"  - {event_id}")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
