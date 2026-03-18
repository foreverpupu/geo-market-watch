"""
Wire real RSS input to canonical signal chain.

Demonstrates: RSS → NormalizedEvent → Selector → Registry → Canonical Chain → Signal

JSONL Artifact Schema:
----------------------
Each line is a JSON object representing one event processing result:

{
    "event_id": str,              # Unique event identifier
    "status": str,                # "processed" | "skipped" | "error"
    "reason": str,                # Present if status != "processed"
    "pack": str,                  # Selected pack name (geo/tech/crypto)
    "category": str,              # Event category
    "region": str,                # Event region
    "score": float,               # Signal score (0-10)
    "triggered": bool,            # Whether signal triggered analysis
    "signal_class": str,          # Signal classification
    "queue": str,                 # Assigned queue
    "title": str,                 # Truncated event title
    "canonical_key": str,         # Dedupe key (first 10 normalized words)
    "dedupe_hash": str,           # 16-char MD5 hash for fast lookup
    "normalization_explain": {    # Metadata about inference decisions
        "region": {
            "region": str,
            "source": "provided" | "inferred" | "default",
            "matched_keywords": [str],
            "rule": str
        },
        "category": {             # Same structure as region
            "category": str,
            "source": str,
            "matched_keywords": [str],
            "rule": str
        },
        "severity": {
            "value": str,
            "inferred": bool
        }
    }
}
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

from geo_market_watch.intake.adapter import RSSIntakeAdapter
from geo_market_watch.packs import get_selector, get_registry, reset_selector, reset_registry
from geo_market_watch.packs.geo import geo_pack
from geo_market_watch.packs.tech import tech_pack
from geo_market_watch.packs.crypto import crypto_pack
from geo_market_watch.core.services.scoring_engine import ScoringEngine
from geo_market_watch.core.services.signal_workflow import (
    CanonicalSignalEngine,
    CanonicalWorkflowRouter,
)


def setup_packs():
    """Register all packs to registry and selector."""
    reset_registry()
    reset_selector()
    
    registry = get_registry()
    selector = get_selector()
    
    # Register packs
    registry.register("geo", geo_pack)
    registry.register("tech", tech_pack)
    registry.register("crypto", crypto_pack)
    
    # Register categories
    # Geo categories
    for cat in geo_pack.list_supported_categories():
        selector.add_mapping(cat, "geo")
    
    # Tech categories
    for cat in tech_pack.list_supported_categories():
        selector.add_mapping(cat, "tech")
    
    # Crypto categories
    for cat in crypto_pack.list_supported_categories():
        selector.add_mapping(cat, "crypto")
    
    print(f"Registered packs: {registry.list()}")
    print(f"Registered categories: {selector.list_categories()}")
    print()


def process_event(normalized_event) -> Dict[str, Any]:
    """
    Process a single normalized event through canonical chain.
    
    Returns dict with processing results or None if skipped.
    """
    from geo_market_watch.packs.selector import SelectionResult
    
    selector = get_selector()
    registry = get_registry()
    
    # Step 1: Select pack
    selection = selector.select(normalized_event.category)
    
    if selection.result != SelectionResult.SUCCESS:
        # Unknown category - still write to artifact with full metadata
        raw_features = getattr(normalized_event, 'raw_features', {})
        return {
            "event_id": normalized_event.event_id,
            "status": "unknown_category",
            "reason": f"Unknown category: {normalized_event.category}",
            "selection": selection,
            "category": normalized_event.category,
            "region": normalized_event.region,
            "title": normalized_event.title[:60] if hasattr(normalized_event, 'title') else "",
            "raw_features": raw_features,
            "normalization_explain": getattr(normalized_event, 'normalization_explain', {}),
        }
    
    # Step 2: Get pack
    pack = registry.get(selection.pack_name)
    if not pack:
        return {
            "event_id": normalized_event.event_id,
            "status": "error",
            "reason": f"Pack not found: {selection.pack_name}",
            "normalization_explain": getattr(normalized_event, 'normalization_explain', {}),
        }
    
    # Step 3: Score (simplified - use default features)
    # In production, would extract real features from content
    scoring_engine = ScoringEngine(profile=pack.get_scoring_profile())
    
    # Build minimal features based on category
    features = build_minimal_features(normalized_event.category, pack.name)
    
    # Step 4: Generate signal
    signal_engine = CanonicalSignalEngine(
        scoring_engine=scoring_engine,
        signal_policy=pack.get_signal_policy(),
        policy_name=pack.name,
    )
    
    signal = signal_engine.generate(
        event_id=normalized_event.event_id,
        features=features,
        category=normalized_event.category,
        region=normalized_event.region,
    )
    
    # Step 5: Route
    router = CanonicalWorkflowRouter(pack.get_signal_policy())
    decision = router.route(signal)
    
    return {
        "event_id": normalized_event.event_id,
        "status": "processed",
        "pack": pack.name,
        "category": normalized_event.category,
        "region": normalized_event.region,
        "score": signal.score,
        "triggered": signal.triggered,
        "signal_class": signal.signal_class,
        "queue": decision.queue,
        "title": normalized_event.title[:60],
        "canonical_key": getattr(normalized_event, 'canonical_key', None),
        "dedupe_hash": getattr(normalized_event, 'dedupe_hash', None),
        "normalization_explain": getattr(normalized_event, 'normalization_explain', {}),
    }


def build_minimal_features(category: str, pack_name: str) -> Dict[str, float]:
    """
    Build minimal feature dict for demo purposes.
    
    In production, this would use NLP to extract real features from content.
    For demo, we use category-based defaults.
    """
    if pack_name == "geo":
        return {
            "severity": 7.0,
            "market_relevance": 7.0,
            "novelty": 6.0,
            "confidence": 8.0,
            "breadth": 6.0,
            "urgency": 6.0,
            "watchlist_match": 5.0,
        }
    elif pack_name == "tech":
        return {
            "product_impact": 7.0,
            "market_relevance": 7.0,
            "competitive_dynamic": 6.0,
            "confidence": 8.0,
            "supply_chain_risk": 6.0,
            "regulatory_risk": 5.0,
        }
    else:  # crypto
        return {
            "regulatory_risk": 7.0,
            "market_impact": 7.0,
            "liquidity_impact": 6.0,
            "confidence": 8.0,
            "novelty": 6.0,
        }


def write_jsonl_artifact(results: List[Dict[str, Any]], output_dir: str = "artifacts") -> str:
    """Write results to replayable JSONL artifact."""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"intake_output_{timestamp}.jsonl"
    filepath = os.path.join(output_dir, filename)
    
    # Write JSONL
    with open(filepath, 'w', encoding='utf-8') as f:
        for result in results:
            # Convert datetime objects to ISO strings for JSON serialization
            json_result = serialize_for_json(result)
            f.write(json.dumps(json_result, ensure_ascii=False) + '\n')
    
    return filepath


def serialize_for_json(obj: Any) -> Any:
    """Recursively serialize objects for JSON output.
    
    Raises:
        ValueError: If object cannot be serialized to JSON.
    """
    from enum import Enum
    
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif hasattr(obj, '__dict__'):
        # Only serialize known dataclass-like objects, reject arbitrary objects
        obj_class = obj.__class__.__name__
        if obj_class in ('SelectionResult', 'Signal', 'NormalizedEvent', 'PackSelection'):
            return serialize_for_json(obj.__dict__)
        raise ValueError(f"Cannot serialize object of type {obj_class}")
    else:
        raise ValueError(f"Cannot serialize object of type {type(obj).__name__}")


def main():
    """
    Main entry point: fetch RSS and process through canonical chain.
    """
    print("=" * 60)
    print("Intake to Canonical Chain Demo")
    print("=" * 60)
    print()
    
    # Setup
    setup_packs()
    
    # Fetch RSS
    print("Fetching RSS feed...")
    adapter = RSSIntakeAdapter()
    events = adapter.fetch_and_normalize(limit=10)
    print(f"Fetched {len(events)} events\n")
    
    # Process each event
    print("Processing events through canonical chain...")
    print("-" * 60)
    
    processed = 0
    unknown_category = 0
    skipped = 0
    results = []
    
    for event in events:
        result = process_event(event)
        results.append(result)
        
        if result["status"] == "processed":
            processed += 1
            print(f"✓ {result['title'][:50]}...")
            print(f"  Pack: {result['pack']} | Category: {result['category']}")
            print(f"  Score: {result['score']:.2f} | Triggered: {result['triggered']}")
            print(f"  Queue: {result['queue']}")
            print()
        elif result["status"] == "unknown_category":
            unknown_category += 1
            print(f"? {result['title'][:50]}...")
            print(f"  Unknown category: {result['category']}")
            # Show detection metadata if available
            raw_features = result.get('raw_features', {})
            cat_detection = raw_features.get('category_detection', {})
            if cat_detection.get('total_matches', 0) > 0:
                print(f"  Candidate categories: {cat_detection.get('candidate_categories', [])}")
            else:
                print(f"  No category keywords matched")
            print()
        else:
            skipped += 1
            print(f"✗ {event.title[:50]}...")
            print(f"  Skipped: {result['reason']}")
            print()
    
    # Write JSONL artifact
    artifact_path = write_jsonl_artifact(results)
    print(f"Artifact written: {artifact_path}")
    
    # Summary
    print("-" * 60)
    print(f"\nSummary: {processed} processed, {unknown_category} unknown_category, {skipped} skipped")
    print(f"Artifact: {artifact_path}")
    print()
    
    return processed > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)