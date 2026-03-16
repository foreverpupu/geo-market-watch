#!/usr/bin/env python3
"""
Geo Market Watch — Agent Loop CLI Runner

Simple entry point for local execution of the agent loop.
"""

import argparse
import os
import sys

from geo_market_watch.agent_loop import print_summary, run_agent_loop


def main():
    parser = argparse.ArgumentParser(
        description='Run Geo Market Watch Agent Loop',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gmw-agent --input data/intake-sample.json --memory data/dedupe-memory.json
  gmw-agent --input data/intake-sample.json --memory data/dedupe-memory.json --output outputs/
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to intake JSON file'
    )
    
    parser.add_argument(
        '--memory', '-m',
        required=True,
        help='Path to dedupe memory JSON file'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Optional output directory for notification files'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Ensure output directory exists if specified
    if args.output:
        os.makedirs(args.output, exist_ok=True)
    
    try:
        # Run agent loop
        summary = run_agent_loop(
            intake_path=args.input,
            dedupe_memory_path=args.memory,
            output_dir=args.output
        )
        
        # Print summary
        print_summary(summary)
        
        # Success
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
