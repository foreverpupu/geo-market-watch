"""
Refactored scoring engine with base scoring and policy adjustments separated.
"""

from typing import Dict, Any, Optional
from geo_market_watch.models import NormalizedEvent, ScoreResult, ScoreBand


class ScoringEngine:
    """
    Deterministic scoring with configurable thresholds.
    
    Separates base scoring from policy adjustments for flexibility.
    """
    
    # Default thresholds (can be overridden via config)
    DEFAULT_BANDS = {
        ScoreBand.LOW: (0, 3),
        ScoreBand.MEDIUM: (4, 6),
        ScoreBand.HIGH: (7, 8),
        ScoreBand.CRITICAL: (9, 10)
    }
    
    # Category base scores
    CATEGORY_BASE = {
        "shipping": 6,
        "energy": 7,
        "sanctions": 6,
        "conflict": 8,
        "election": 5,
        "general": 5
    }
    
    # Severity modifiers
    SEVERITY_MODIFIERS = {
        "critical": 3,
        "high": 2,
        "medium": 0,
        "low": -1
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize scoring engine.
        
        Args:
            config: Optional configuration overrides
        """
        self.config = config or {}
        self.bands = self.config.get("bands", self.DEFAULT_BANDS)
        self.category_base = self.config.get("category_base", self.CATEGORY_BASE)
        self.severity_modifiers = self.config.get("severity_modifiers", self.SEVERITY_MODIFIERS)
    
    def compute_score(self, event: NormalizedEvent) -> ScoreResult:
        """
        Compute score for normalized event.
        
        Args:
            event: Normalized event
            
        Returns:
            ScoreResult with value, band, and breakdown
        """
        breakdown = {}
        
        # Base score from category
        base_score = self.category_base.get(event.category, 5)
        breakdown["category_base"] = float(base_score)
        
        # Severity modifier
        severity_mod = self.severity_modifiers.get(event.severity, 0)
        breakdown["severity_modifier"] = float(severity_mod)
        
        # Calculate raw score
        raw_score = base_score + severity_mod
        
        # Policy adjustments (future: config-driven rules)
        policy_adjustment = self._apply_policy_adjustments(event)
        breakdown["policy_adjustment"] = policy_adjustment
        
        # Final score (clamped 0-10)
        final_score = max(0, min(10, raw_score + policy_adjustment))
        breakdown["final_score"] = final_score
        
        # Determine band
        band = self._score_to_band(final_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(event, breakdown)
        
        return ScoreResult(
            value=final_score,
            band=band,
            breakdown=breakdown,
            reasoning=reasoning
        )
    
    def _apply_policy_adjustments(self, event: NormalizedEvent) -> float:
        """
        Apply policy-based adjustments.
        
        Future: Load from configuration file for domain-specific tuning.
        """
        adjustment = 0.0
        
        # Example policy: Shipping + Middle East = higher impact
        if event.category == "shipping" and event.region == "Middle East":
            adjustment += 1.0
        
        # Example policy: Energy + critical severity = maximum impact
        if event.category == "energy" and event.severity == "critical":
            adjustment += 1.5
        
        return adjustment
    
    def _score_to_band(self, score: float) -> ScoreBand:
        """Convert numeric score to band."""
        for band, (low, high) in self.bands.items():
            if low <= score <= high:
                return band
        return ScoreBand.LOW
    
    def _generate_reasoning(self, event: NormalizedEvent, breakdown: Dict[str, float]) -> str:
        """Generate human-readable reasoning."""
        parts = [
            f"Category '{event.category}' base score: {breakdown['category_base']}",
            f"Severity '{event.severity}' modifier: {breakdown['severity_modifier']}",
        ]
        
        if breakdown.get("policy_adjustment", 0) != 0:
            parts.append(f"Policy adjustment: {breakdown['policy_adjustment']}")
        
        parts.append(f"Final score: {breakdown['final_score']}")
        
        return "; ".join(parts)
    
    def get_band_thresholds(self) -> Dict[str, tuple]:
        """Get current band thresholds."""
        return {
            band.value: (low, high)
            for band, (low, high) in self.bands.items()
        }
