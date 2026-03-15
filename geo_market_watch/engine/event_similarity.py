"""
Event similarity calculation module.

Provides functions for computing similarity between events,
primarily for deduplication purposes.
"""

from typing import Set
from difflib import SequenceMatcher
from geo_market_watch.models import NormalizedEvent


def headline_similarity(a: str, b: str) -> float:
    """
    Calculate similarity between two headlines.
    
    Uses token-based Jaccard similarity combined with
    sequence matching for robust comparison.
    
    Args:
        a: First headline
        b: Second headline
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not a or not b:
        return 0.0
    
    # Normalize: lowercase, strip whitespace
    a_norm = a.lower().strip()
    b_norm = b.lower().strip()
    
    if a_norm == b_norm:
        return 1.0
    
    # Token-based Jaccard similarity
    tokens_a = _tokenize(a_norm)
    tokens_b = _tokenize(b_norm)
    
    jaccard = _jaccard_similarity(tokens_a, tokens_b)
    
    # Sequence similarity for word order
    sequence = SequenceMatcher(None, a_norm, b_norm).ratio()
    
    # Weighted combination: 60% Jaccard (content) + 40% sequence (structure)
    return 0.6 * jaccard + 0.4 * sequence


def event_similarity_score(event_a: NormalizedEvent, event_b: NormalizedEvent) -> float:
    """
    Calculate comprehensive similarity between two events.
    
    Considers:
    - Headline similarity (primary)
    - Region match (boosts similarity if same)
    - Category match (boosts similarity if same)
    
    Args:
        event_a: First event
        event_b: Second event
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Base headline similarity
    headline_sim = headline_similarity(event_a.headline, event_b.headline)
    
    # Region match bonus (10% boost if same region)
    region_bonus = 0.1 if event_a.region == event_b.region else 0.0
    
    # Category match bonus (10% boost if same category)
    category_bonus = 0.1 if event_a.category == event_b.category else 0.0
    
    # Combined score (capped at 1.0)
    combined = min(1.0, headline_sim + region_bonus + category_bonus)
    
    return combined


def is_soft_duplicate(
    event_a: NormalizedEvent,
    event_b: NormalizedEvent,
    similarity_threshold: float = 0.7,
    days_window: int = 7
) -> bool:
    """
    Determine if two events are soft duplicates.
    
    Soft duplicate criteria:
    - Same region
    - Same category
    - Headline similarity > threshold
    - Within time window
    
    Args:
        event_a: First event
        event_b: Second event
        similarity_threshold: Minimum similarity (default 0.7)
        days_window: Maximum days between events (default 7)
        
    Returns:
        True if events are considered soft duplicates
    """
    from datetime import timedelta
    
    # Check region match
    if event_a.region != event_b.region:
        return False
    
    # Check category match
    if event_a.category != event_b.category:
        return False
    
    # Check time window
    time_diff = abs((event_a.timestamp - event_b.timestamp).total_seconds())
    if time_diff > timedelta(days=days_window).total_seconds():
        return False
    
    # Check headline similarity
    similarity = headline_similarity(event_a.headline, event_b.headline)
    return similarity >= similarity_threshold


def _tokenize(text: str) -> Set[str]:
    """
    Tokenize text into a set of words.
    
    Removes common stop words and punctuation.
    """
    # Simple stop words list
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Extract words (alphanumeric only)
    import re
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter out stop words and short words
    return {w for w in words if w not in stop_words and len(w) > 2}


def _jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """
    Calculate Jaccard similarity between two sets.
    
    Jaccard = |A ∩ B| / |A ∪ B|
    """
    if not set_a and not set_b:
        return 1.0  # Both empty = identical
    
    if not set_a or not set_b:
        return 0.0  # One empty, one not = no similarity
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    return intersection / union if union > 0 else 0.0
