"""
Refactored dedupe memory with event-level approximate deduplication.
"""

import json
import hashlib
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from difflib import SequenceMatcher
from geo_market_watch.models import NormalizedEvent, DedupeRecord


class DedupeMemory:
    """
    Event-level deduplication with hard and soft matching.
    
    Hard dedupe: Exact canonical key or URL match
    Soft dedupe: Headline similarity + region/category + time window
    """
    
    def __init__(
        self,
        memory_path: str,
        similarity_threshold: float = 0.85,
        time_window_hours: int = 24
    ):
        """
        Initialize dedupe memory.
        
        Args:
            memory_path: Path to JSON memory file
            similarity_threshold: Minimum similarity for soft match (0-1)
            time_window_hours: Time window for considering duplicates
        """
        self.memory_path = Path(memory_path)
        self.similarity_threshold = similarity_threshold
        self.time_window = timedelta(hours=time_window_hours)
        self._memory: Dict[str, DedupeRecord] = {}
        self._load()
    
    def _load(self) -> None:
        """Load memory from file with corruption handling."""
        if not self.memory_path.exists():
            self._memory = {}
            return
        
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._memory = {
                k: DedupeRecord(
                    canonical_key=v["canonical_key"],
                    first_seen_at=datetime.fromisoformat(v["first_seen_at"]),
                    last_seen_at=datetime.fromisoformat(v["last_seen_at"]),
                    occurrence_count=v["occurrence_count"],
                    headline_variants=v.get("headline_variants", []),
                    source_urls=v.get("source_urls", [])
                )
                for k, v in data.items()
            }
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Backup corrupted file
            backup_path = self.memory_path.with_suffix('.json.corrupted')
            shutil.copy2(self.memory_path, backup_path)
            print(f"WARNING: Dedupe memory corrupted, backed up to {backup_path}")
            print(f"ERROR: {e}")
            print("Starting with empty memory")
            self._memory = {}
    
    def _save(self) -> None:
        """Save memory to file."""
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            k: {
                "canonical_key": v.canonical_key,
                "first_seen_at": v.first_seen_at.isoformat(),
                "last_seen_at": v.last_seen_at.isoformat(),
                "occurrence_count": v.occurrence_count,
                "headline_variants": v.headline_variants,
                "source_urls": v.source_urls
            }
            for k, v in self._memory.items()
        }
        
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def check_duplicate(
        self,
        event: NormalizedEvent,
        current_time: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """
        Check if event is a duplicate.
        
        Args:
            event: Normalized event to check
            current_time: Reference time for time window
            
        Returns:
            (is_duplicate, reason)
        """
        current_time = current_time or datetime.now()
        
        # Hard dedupe: Exact canonical key match
        if event.canonical_key and event.canonical_key in self._memory:
            record = self._memory[event.canonical_key]
            if self._is_within_time_window(record.last_seen_at, current_time):
                record.add_occurrence(event.headline, current_time)
                self._save()
                return True, f"Exact canonical key match (seen {record.occurrence_count}x)"
        
        # Hard dedupe: URL match
        if event.source_url_hash:
            for record in self._memory.values():
                if event.source_url_hash in record.source_urls:
                    if self._is_within_time_window(record.last_seen_at, current_time):
                        record.add_occurrence(event.headline, current_time)
                        self._save()
                        return True, "URL match"
        
        # Soft dedupe: Similar headline + same region/category + time window
        for record in self._memory.values():
            if not self._is_within_time_window(record.last_seen_at, current_time):
                continue
            
            # Check similarity with all variants
            for variant in record.headline_variants:
                similarity = self._calculate_similarity(event.headline, variant)
                if similarity >= self.similarity_threshold:
                    record.add_occurrence(event.headline, current_time)
                    self._save()
                    return True, f"Similar headline ({similarity:.2f} match)"
        
        # Not a duplicate - add to memory
        self._add_new_event(event, current_time)
        return False, "New event"
    
    def _add_new_event(self, event: NormalizedEvent, timestamp: datetime) -> None:
        """Add new event to memory."""
        key = event.canonical_key or self._generate_key(event)
        
        self._memory[key] = DedupeRecord(
            canonical_key=key,
            first_seen_at=timestamp,
            last_seen_at=timestamp,
            occurrence_count=1,
            headline_variants=[event.headline],
            source_urls=[u for u in (event.urls or []) if u]
        )
        self._save()
    
    def _is_within_time_window(self, last_seen: datetime, current: datetime) -> bool:
        """Check if last_seen is within time window of current."""
        return (current - last_seen) <= self.time_window
    
    def _calculate_similarity(self, a: str, b: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def _generate_key(self, event: NormalizedEvent) -> str:
        """Generate key for events without canonical_key."""
        content = f"{event.headline}:{event.timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "total_events": len(self._memory),
            "total_occurrences": sum(r.occurrence_count for r in self._memory.values()),
            "multi_occurrence_events": sum(1 for r in self._memory.values() if r.occurrence_count > 1)
        }
