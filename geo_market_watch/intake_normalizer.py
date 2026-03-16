"""
Refactored intake normalizer with clear parse/validate/materialize steps.
"""

import hashlib
import re
from datetime import datetime
from typing import Any

from geo_market_watch.models import NormalizedEvent, RawIntakeItem


class ParseError(Exception):
    """Raised when raw input cannot be parsed."""
    pass


class ValidationError(Exception):
    """Raised when required fields are missing or invalid."""
    pass


class IntakeNormalizer:
    """Three-step normalizer: parse → validate → materialize."""
    
    # Region keywords for classification
    REGION_KEYWORDS = {
        "Middle East": ["middle east", "gulf", "saudi", "iran", "israel", "red sea"],
        "Asia-Pacific": ["china", "japan", "korea", "taiwan", "australia", "india"],
        "Europe": ["europe", "eu", "germany", "france", "uk", "russia", "ukraine"],
        "North America": ["us", "usa", "canada", "america"],
        "Latin America": ["brazil", "mexico", "argentina", "venezuela"],
        "Africa": ["africa", "nigeria", "south africa", "egypt"],
    }
    
    # Category keywords
    CATEGORY_KEYWORDS = {
        "shipping": ["shipping", "vessel", "cargo", "port", "maritime", "container"],
        "energy": ["oil", "gas", "lng", "pipeline", "energy", "petroleum"],
        "sanctions": ["sanction", "export control", "embargo", "ban"],
        "conflict": ["war", "conflict", "attack", "military", "invasion"],
        "election": ["election", "vote", "poll", "political"],
    }
    
    def __init__(self, current_time: datetime | None = None):
        """
        Initialize normalizer.
        
        Args:
            current_time: Injectable time for reproducibility. Defaults to datetime.now().
        """
        self.current_time = current_time or datetime.now()
    
    def normalize(self, raw: dict[str, Any]) -> NormalizedEvent:
        """
        Main entry: parse → validate → materialize.
        
        Args:
            raw: Raw input dictionary
            
        Returns:
            NormalizedEvent
            
        Raises:
            ParseError: If input cannot be parsed
            ValidationError: If required fields are missing
        """
        # Step 1: Parse
        parsed = self._parse(raw)
        
        # Step 2: Validate
        self._validate(parsed)
        
        # Step 3: Materialize
        return self._materialize(parsed)
    
    def _parse(self, raw: dict[str, Any]) -> RawIntakeItem:
        """Parse raw dict into RawIntakeItem."""
        try:
            # Parse timestamp
            ts = raw.get("timestamp")
            if isinstance(ts, str):
                timestamp = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            elif isinstance(ts, datetime):
                timestamp = ts
            else:
                timestamp = self.current_time
            
            return RawIntakeItem(
                headline=raw.get("headline", "").strip(),
                timestamp=timestamp,
                source=raw.get("source"),
                summary=raw.get("summary"),
                region=raw.get("region"),
                category=raw.get("category"),
                urls=raw.get("urls", []),
                raw_metadata={k: v for k, v in raw.items() if k not in [
                    "headline", "timestamp", "source", "summary", "region", "category", "urls"
                ]}
            )
        except Exception as e:
            raise ParseError(f"Failed to parse raw input: {e}") from e
    
    def _validate(self, item: RawIntakeItem) -> None:
        """Validate required fields."""
        errors = []
        
        if not item.headline:
            errors.append("headline is required")
        elif len(item.headline) < 10:
            errors.append(f"headline too short (min 10 chars): {item.headline[:50]}...")
        
        if not item.timestamp:
            errors.append("timestamp is required")
        
        if errors:
            raise ValidationError("; ".join(errors))
    
    def _materialize(self, item: RawIntakeItem) -> NormalizedEvent:
        """Create NormalizedEvent from validated RawIntakeItem."""
        # Generate event ID
        event_id = self._generate_event_id(item)
        
        # Infer region if not provided
        region = item.region or self._infer_region(item.headline)
        
        # Infer category if not provided
        category = item.category or self._infer_category(item.headline)
        
        # Infer severity
        severity = self._infer_severity(item.headline)
        
        # Generate canonical key for dedupe
        canonical_key = self._generate_canonical_key(item)
        
        return NormalizedEvent(
            event_id=event_id,
            headline=item.headline,
            timestamp=item.timestamp,
            region=region,
            category=category,
            severity=severity,
            summary=item.summary,
            source=item.source,
            urls=item.urls,
            canonical_key=canonical_key,
            source_url_hash=self._hash_urls(item.urls)
        )
    
    def _generate_event_id(self, item: RawIntakeItem) -> str:
        """Generate unique event ID."""
        content = f"{item.headline}:{item.timestamp.isoformat()}"
        return f"evt_{hashlib.md5(content.encode()).hexdigest()[:12]}"
    
    def _generate_canonical_key(self, item: RawIntakeItem) -> str:
        """Generate canonical key for deduplication."""
        # Normalize headline: lowercase, remove punctuation
        normalized = re.sub(r'[^\w\s]', '', item.headline.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Take first 10 words
        words = normalized.split()[:10]
        return " ".join(words)
    
    def _hash_urls(self, urls: list) -> str | None:
        """Hash URLs for dedupe."""
        if not urls:
            return None
        return hashlib.md5("|".join(sorted(urls)).encode()).hexdigest()[:16]
    
    def _infer_region(self, headline: str) -> str:
        """Infer region from headline keywords."""
        headline_lower = headline.lower()
        for region, keywords in self.REGION_KEYWORDS.items():
            if any(kw in headline_lower for kw in keywords):
                return region
        return "Global"
    
    def _infer_category(self, headline: str) -> str:
        """Infer category from headline keywords."""
        headline_lower = headline.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in headline_lower for kw in keywords):
                return category
        return "general"
    
    def _infer_severity(self, headline: str) -> str:
        """Infer severity from headline language."""
        headline_lower = headline.lower()
        
        critical_indicators = ["escalates", "crisis", "war", "invasion", "collapse"]
        high_indicators = ["disruption", "surge", "plunge", "sanctions", "attack"]
        
        if any(w in headline_lower for w in critical_indicators):
            return "critical"
        elif any(w in headline_lower for w in high_indicators):
            return "high"
        else:
            return "medium"
