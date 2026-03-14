"""
Geo Market Watch v5.5 — Deduplication Memory

Simple JSON-based memory for tracking seen events.
"""

import json
import os
from typing import Dict, Any, Set
from datetime import datetime


class DedupeMemory:
    """
    Simple file-based deduplication memory.
    
    Stores event keys with timestamps to track which events have been processed.
    """
    
    def __init__(self, memory_path: str):
        """
        Initialize deduplication memory.
        
        Args:
            memory_path: Path to JSON file for storing memory
        """
        self.memory_path = memory_path
        self.seen_keys: Dict[str, str] = {}  # event_key -> first_seen_timestamp
        self._load()
    
    def _load(self):
        """Load memory from file if it exists."""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r') as f:
                    data = json.load(f)
                    self.seen_keys = data.get("seen_keys", {})
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                self.seen_keys = {}
    
    def save(self):
        """Save memory to file."""
        data = {
            "seen_keys": self.seen_keys,
            "updated_at": datetime.now().isoformat(),
            "version": "5.5"
        }
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def has_seen(self, event_key: str) -> bool:
        """
        Check if an event key has been seen before.
        
        Args:
            event_key: Unique event identifier
            
        Returns:
            True if event has been processed, False otherwise
        """
        return event_key in self.seen_keys
    
    def mark_seen(self, event_key: str):
        """
        Mark an event key as seen.
        
        Args:
            event_key: Unique event identifier
        """
        if event_key not in self.seen_keys:
            self.seen_keys[event_key] = datetime.now().isoformat()
    
    def split_events(self, events: list) -> tuple:
        """
        Split events into new and duplicate sets.
        
        Args:
            events: List of normalized event dicts (must have 'event_key' field)
            
        Returns:
            Tuple of (new_events, duplicate_events)
        """
        new_events = []
        duplicate_events = []
        
        for event in events:
            event_key = event.get("event_key")
            if not event_key:
                # If no key, treat as new (shouldn't happen with proper normalization)
                new_events.append(event)
                continue
            
            if self.has_seen(event_key):
                duplicate_events.append(event)
            else:
                new_events.append(event)
                self.mark_seen(event_key)
        
        return new_events, duplicate_events
    
    def get_stats(self) -> Dict[str, Any]:
        """Return memory statistics."""
        return {
            "total_seen": len(self.seen_keys),
            "memory_path": self.memory_path
        }


def load_dedupe_memory(memory_path: str) -> DedupeMemory:
    """
    Load or create deduplication memory.
    
    Args:
        memory_path: Path to memory file
        
    Returns:
        DedupeMemory instance
    """
    return DedupeMemory(memory_path)


if __name__ == "__main__":
    # Example usage
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        memory = DedupeMemory(temp_path)
        
        # Mark some events as seen
        memory.mark_seen("abc123")
        memory.mark_seen("def456")
        memory.save()
        
        # Check if seen
        print(f"Has seen abc123: {memory.has_seen('abc123')}")
        print(f"Has seen xyz999: {memory.has_seen('xyz999')}")
        print(f"Stats: {memory.get_stats()}")
        
    finally:
        os.unlink(temp_path)
