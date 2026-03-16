#!/usr/bin/env python3
"""
Geo Market Watch — Example Run

Simple example of running the agent loop.
"""

import sys
from pathlib import Path

from geo_market_watch.agent_loop import run_agent_loop, print_summary


def main():
    """Run a simple example."""
    intake_path = Path("data/intake-sample.json")
    memory_path = Path("data/dedupe-memory.json")
    
    if not intake_path.exists():
        print(f"Error: Intake file not found: {intake_path}")
        print("Please create sample data first.")
        return 1
    
    print("Running Geo Market Watch Agent Loop...")
    print(f"  Intake: {intake_path}")
    print(f"  Memory: {memory_path}")
    
    try:
        summary = run_agent_loop(
            intake_path=str(intake_path),
            dedupe_memory_path=str(memory_path),
            output_dir="outputs"
        )
        
        print_summary(summary)
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
