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
    
    def compute_base_score(self, event: NormalizedEvent) -> tuple[float, dict]:
        """
        Compute base score from category and severity.
        
        Args:
            event: Normalized event
            
        Returns:
            Tuple of (base_score, breakdown_dict)
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
        
        return float(raw_score), breakdown
    
    def apply_adjustments(self, base_score: float, event: NormalizedEvent) -> tuple[float, float]:
        """
        Apply policy-based adjustments to base score.
        
        Args:
            base_score: Raw score from compute_base_score
            event: Normalized event for context
            
        Returns:
            Tuple of (adjusted_score, adjustment_amount)
        """
        adjustment = self._apply_policy_adjustments(event)
        adjusted_score = base_score + adjustment
        return adjusted_score, adjustment
    
    def finalize_score(self, adjusted_score: float, breakdown: dict) -> ScoreResult:
        """
        Finalize score by clamping, determining band, and generating reasoning.
        
        Args:
            adjusted_score: Score after adjustments
            breakdown: Score breakdown dictionary
            
        Returns:
            Final ScoreResult
        """
        # Clamp to valid range
        final_score = max(0, min(10, adjusted_score))
        breakdown["final_score"] = final_score
        
        # Determine band
        band = self._score_to_band(final_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning_from_breakdown(breakdown)
        
        return ScoreResult(
            value=final_score,
            band=band,
            breakdown=breakdown,
            reasoning=reasoning
        )
    
    def compute_score(self, event: NormalizedEvent) -> ScoreResult:
        """
        Compute score for normalized event.
        
        Orchestrates the three-step process:
        1. compute_base_score()
        2. apply_adjustments()
        3. finalize_score()
        
        Args:
            event: Normalized event
            
        Returns:
            ScoreResult with value, band, and breakdown
        """
        # Step 1: Compute base score
        base_score, breakdown = self.compute_base_score(event)
        
        # Step 2: Apply adjustments
        adjusted_score, adjustment = self.apply_adjustments(base_score, event)
        breakdown["policy_adjustment"] = adjustment
        
        # Step 3: Finalize
        return self.finalize_score(adjusted_score, breakdown)
    
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
        return self._generate_reasoning_from_breakdown(breakdown, event.category, event.severity)
    
    def _generate_reasoning_from_breakdown(
        self,
        breakdown: Dict[str, float],
        category: str = "",
        severity: str = ""
    ) -> str:
        """Generate human-readable reasoning from breakdown."""
        parts = []
        
        if "category_base" in breakdown:
            cat = category or "unknown"
            parts.append(f"Category '{cat}' base score: {breakdown['category_base']}")
        
        if "severity_modifier" in breakdown:
            sev = severity or "unknown"
            parts.append(f"Severity '{sev}' modifier: {breakdown['severity_modifier']}")
        
        if breakdown.get("policy_adjustment", 0) != 0:
            parts.append(f"Policy adjustment: {breakdown['policy_adjustment']}")
        
        if "final_score" in breakdown:
            parts.append(f"Final score: {breakdown['final_score']}")
        
        return "; ".join(parts)
    
    def get_band_thresholds(self) -> Dict[str, tuple]:
        """Get current band thresholds."""
        return {
            band.value: (low, high)
            for band, (low, high) in self.bands.items()
        }
