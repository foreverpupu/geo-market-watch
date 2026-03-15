"""
Geo Market Watch v5.5 — Agent Loop

Runs the full 4-node processing pipeline in a single process.
This module now delegates to agent_pipeline for actual processing.
"""

from datetime import datetime
from typing import Optional

from geo_market_watch.models import AgentRunSummary
from geo_market_watch.engine.agent_pipeline import run_pipeline


def run_agent_loop(
    intake_path: str,
    dedupe_memory_path: str,
    output_dir: Optional[str] = None,
    current_time: Optional[datetime] = None
) -> AgentRunSummary:
    """
    Run the full agent loop.
    
    Delegates to agent_pipeline.run_pipeline() for actual processing.
    This function serves as the main entry point and orchestrator.
    
    Args:
        intake_path: Path to intake JSON file
        dedupe_memory_path: Path to dedupe memory JSON file
        output_dir: Optional directory to write notification files
        current_time: Optional time reference for reproducibility
        
    Returns:
        AgentRunSummary with full execution details
    """
    return run_pipeline(
        intake_path=intake_path,
        dedupe_memory_path=dedupe_memory_path,
        output_dir=output_dir,
        current_time=current_time
    )


def print_summary(summary: AgentRunSummary):
    """Print run summary to stdout."""
    print("=" * 60)
    print("Geo Market Watch v5.5 — Agent Loop Summary")
    print("=" * 60)
    print()
    print(f"Run ID: {summary.run_id}")
    print(f"Started: {summary.started_at}")
    if summary.completed_at:
        print(f"Completed: {summary.completed_at}")
        print(f"Duration: {summary.duration_seconds:.2f}s")
    print()
    print(f"Items processed: {summary.items_processed}")
    print(f"Items normalized: {summary.items_normalized}")
    print(f"Items deduped: {summary.items_deduped}")
    print(f"Items scored: {summary.items_scored}")
    print(f"Items triggered: {summary.items_triggered}")
    print(f"Items persisted: {summary.items_persisted}")
    print()
    print(f"Notifications generated: {summary.notifications_generated}")
    print(f"Success: {summary.success}")
    
    if summary.errors:
        print()
        print("Errors:")
        for error in summary.errors:
            print(f"  - {error}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    # Example usage
    import os
    import json
    import tempfile
    
    # Create sample intake file
    sample_intake = {
        "items": [
            {
                "source_name": "Reuters",
                "source_url": "https://example.com/red-sea",
                "published_at": "2024-01-12",
                "headline": "Red Sea shipping disruption escalates as Houthis target more vessels",
                "region": "Middle East",
                "category": "shipping",
                "summary": "Major container lines reroute vessels.",
            },
            {
                "source_name": "Bloomberg",
                "source_url": "https://example.com/russia-oil",
                "published_at": "2023-12-15",
                "headline": "Russia expands oil export restrictions amid sanctions",
                "region": "Eastern Europe",
                "category": "energy",
                "summary": "Russia expands restrictions affecting energy exports.",
            }
        ]
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        intake_path = os.path.join(tmpdir, "intake.json")
        memory_path = os.path.join(tmpdir, "memory.json")
        output_path = os.path.join(tmpdir, "outputs")
        
        with open(intake_path, 'w') as f:
            json.dump(sample_intake, f)
        
        # Run agent loop
        summary = run_agent_loop(intake_path, memory_path, output_path)
        print_summary(summary)
        
        print(f"\nOutput directory: {output_path}")
