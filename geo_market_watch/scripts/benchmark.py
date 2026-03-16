#!/usr/bin/env python3
"""
Geo Market Watch — Run Benchmark CLI

Run performance benchmark on the agent loop.
"""

import argparse
import json
import sys
import time
from pathlib import Path

from geo_market_watch.agent_loop import run_agent_loop


def main():
    parser = argparse.ArgumentParser(
        description='Run Geo Market Watch Benchmark',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gmw-benchmark --input data/intake-sample.json --memory data/dedupe-memory.json
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
        help='Optional output file for benchmark results'
    )
    
    parser.add_argument(
        '--runs', '-n',
        type=int,
        default=1,
        help='Number of benchmark runs (default: 1)'
    )
    
    args = parser.parse_args()
    
    # Validate input files exist
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if not Path(args.memory).exists():
        print(f"Error: Memory file not found: {args.memory}", file=sys.stderr)
        sys.exit(1)
    
    results = []
    
    for run in range(args.runs):
        print(f"Run {run + 1}/{args.runs}...")
        
        start_time = time.time()
        
        try:
            summary = run_agent_loop(
                intake_path=args.input,
                dedupe_memory_path=args.memory,
                output_dir=None
            )
            
            elapsed = time.time() - start_time
            
            result = {
                'run': run + 1,
                'elapsed_seconds': elapsed,
                'events_processed': summary.get('total', 0),
                'notifications': summary.get('notifications', 0),
                'errors': summary.get('errors', 0)
            }
            results.append(result)
            
            print(f"  Processed {result['events_processed']} events in {elapsed:.2f}s")
            
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)
            results.append({
                'run': run + 1,
                'error': str(e)
            })
    
    # Calculate summary statistics
    successful = [r for r in results if 'error' not in r]
    
    if successful:
        avg_time = sum(r['elapsed_seconds'] for r in successful) / len(successful)
        avg_events = sum(r['events_processed'] for r in successful) / len(successful)
        
        benchmark_summary = {
            'total_runs': args.runs,
            'successful_runs': len(successful),
            'average_time_seconds': avg_time,
            'average_events_processed': avg_events,
            'runs': results
        }
        
        print(f"\nBenchmark Summary:")
        print(f"  Total runs: {args.runs}")
        print(f"  Successful: {len(successful)}")
        print(f"  Average time: {avg_time:.2f}s")
        print(f"  Average events: {avg_events:.1f}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(benchmark_summary, f, indent=2)
            print(f"\nResults saved to: {args.output}")
    else:
        print("\nNo successful benchmark runs.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
