"""
Integration tests for the full agent pipeline.

Tests the complete flow: intake → normalize → dedupe → score → trigger
"""

import json
import tempfile
import os
from datetime import datetime
from pathlib import Path

import pytest

from geo_market_watch.agent_loop import run_agent_loop
from geo_market_watch.engine.agent_pipeline import load_intake
from geo_market_watch.models import AgentRunSummary


class TestAgentLoopIntegration:
    """Integration tests for the full agent loop."""
    
    @pytest.fixture
    def sample_intake_data(self):
        """Sample intake data for testing."""
        return {
            "items": [
                {
                    "source_name": "Reuters",
                    "source_url": "https://example.com/red-sea",
                    "published_at": "2024-01-12T00:00:00",
                    "headline": "Red Sea shipping disruption escalates as Houthis target more vessels",
                    "region": "Middle East",
                    "category": "shipping",
                    "summary": "Major container lines reroute vessels due to attacks.",
                },
                {
                    "source_name": "Bloomberg",
                    "source_url": "https://example.com/russia-oil",
                    "published_at": "2023-12-15T00:00:00",
                    "headline": "Russia expands oil export restrictions amid sanctions",
                    "region": "Eastern Europe",
                    "category": "energy",
                    "summary": "Russia expands restrictions affecting energy exports.",
                },
                {
                    "source_name": "Reuters",
                    "source_url": "https://example.com/red-sea-2",
                    "published_at": "2024-01-12T01:00:00",
                    "headline": "Red Sea shipping disruption escalates as Houthis target more vessels",
                    "region": "Middle East",
                    "category": "shipping",
                    "summary": "Duplicate headline for dedupe testing.",
                }
            ]
        }
    
    @pytest.fixture
    def temp_intake_file(self, sample_intake_data):
        """Create a temporary intake file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_intake_data, f)
            f.flush()
            yield f.name
            os.unlink(f.name)
    
    @pytest.fixture
    def temp_memory_file(self):
        """Create a temporary memory file path."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{}')
            f.flush()
            yield f.name
            os.unlink(f.name)
    
    def test_full_pipeline_execution(self, temp_intake_file, temp_memory_file):
        """Test that the full pipeline runs successfully."""
        summary = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file,
            current_time=datetime(2024, 1, 15, 12, 0, 0)
        )
        
        # Verify summary structure
        assert isinstance(summary, AgentRunSummary)
        assert summary.run_id.startswith("run_")
        assert summary.started_at is not None
        assert summary.completed_at is not None
        
        # Verify counts
        assert summary.items_processed == 3  # Total items
        assert summary.items_normalized == 3  # All should normalize
        assert summary.items_deduped == 1  # One duplicate
        assert summary.items_scored == 2  # 2 new events
        assert summary.items_triggered == 2  # All triggered
        
        # Verify success
        assert summary.success is True
        assert len(summary.errors) == 0
    
    def test_events_total_count(self, temp_intake_file, temp_memory_file):
        """Test that total events count is correct."""
        summary = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file
        )
        
        # Total items processed should match input
        assert summary.items_processed == 3
        assert summary.items_normalized == 3
    
    def test_events_new_count(self, temp_intake_file, temp_memory_file):
        """Test that new events count accounts for deduplication."""
        summary = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file
        )
        
        # New events = normalized - deduped
        new_events = summary.items_normalized - summary.items_deduped
        assert new_events == 2
        assert summary.items_scored == 2
    
    def test_notifications_created(self, temp_intake_file, temp_memory_file):
        """Test that notifications are created for triggered events."""
        summary = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file
        )
        
        # Both new events should trigger full analysis (high scores)
        assert summary.notifications_generated == 2
    
    def test_dedupe_persistence(self, temp_intake_file, temp_memory_file):
        """Test that dedupe memory persists across runs."""
        # First run
        summary1 = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file,
            current_time=datetime(2024, 1, 15, 12, 0, 0)
        )
        
        assert summary1.items_deduped == 1
        
        # Second run with same data - all should be duplicates now
        summary2 = run_agent_loop(
            intake_path=temp_intake_file,
            dedupe_memory_path=temp_memory_file,
            current_time=datetime(2024, 1, 15, 13, 0, 0)
        )
        
        assert summary2.items_deduped == 3  # All are duplicates now
        assert summary2.items_scored == 0  # No new events to score
    
    def test_load_intake_file_list_format(self):
        """Test loading intake file with list format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([{"headline": "Test"}], f)
            f.flush()
            
            items = load_intake(f.name)
            assert len(items) == 1
            assert items[0]["headline"] == "Test"
            
            os.unlink(f.name)
    
    def test_load_intake_file_dict_format(self):
        """Test loading intake file with dict format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"items": [{"headline": "Test"}]}, f)
            f.flush()
            
            items = load_intake(f.name)
            assert len(items) == 1
            assert items[0]["headline"] == "Test"
            
            os.unlink(f.name)
    
    def test_error_handling_invalid_intake(self, temp_memory_file):
        """Test error handling for invalid intake file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": "format"}')  # Missing 'items' key
            f.flush()
            
            summary = run_agent_loop(
                intake_path=f.name,
                dedupe_memory_path=temp_memory_file
            )
            
            # Should complete but with 0 items
            assert summary.items_processed == 0
            
            os.unlink(f.name)
    
    def test_error_handling_missing_file(self, temp_memory_file):
        """Test error handling for missing intake file."""
        summary = run_agent_loop(
            intake_path="/nonexistent/path/intake.json",
            dedupe_memory_path=temp_memory_file
        )
        
        # Should fail gracefully
        assert summary.success is False
        assert len(summary.errors) > 0
