"""
Refactored trigger engine with extended decision structure.
"""

from typing import List, Dict, Any, Optional
from geo_market_watch.models import ScoreResult, TriggerResult, TriggerDecision, EscalationPriority


class TriggerEngine:
    """
    Escalation trigger with configurable thresholds and extended output.
    """
    
    # Default thresholds
    DEFAULT_TRIGGER_THRESHOLD = 7.0
    DEFAULT_PRIORITY_THRESHOLDS = {
        EscalationPriority.LOW: (0, 5),
        EscalationPriority.MEDIUM: (6, 7),
        EscalationPriority.HIGH: (8, 8),
        EscalationPriority.CRITICAL: (9, 10)
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize trigger engine.
        
        Args:
            config: Optional configuration overrides
        """
        self.config = config or {}
        self.trigger_threshold = self.config.get("trigger_threshold", self.DEFAULT_TRIGGER_THRESHOLD)
        self.priority_thresholds = self.config.get("priority_thresholds", self.DEFAULT_PRIORITY_THRESHOLDS)
    
    def should_escalate(
        self,
        score_result: ScoreResult,
        context: Optional[Dict[str, Any]] = None
    ) -> TriggerResult:
        """
        Determine if event should trigger full analysis.
        
        Args:
            score_result: Score result from scoring engine
            context: Optional additional context
            
        Returns:
            TriggerResult with full decision details
        """
        context = context or {}
        reasons = []
        
        # Base decision on score
        score = score_result.value
        should_trigger = score >= self.trigger_threshold
        
        if should_trigger:
            reasons.append(f"Score {score:.1f} >= threshold {self.trigger_threshold}")
        
        # Additional context-based triggers
        if context.get("severity") == "critical":
            should_trigger = True
            reasons.append("Critical severity context")
        
        if context.get("breaking_news"):
            should_trigger = True
            reasons.append("Breaking news flag")
        
        # Determine priority
        priority = self._score_to_priority(score)
        
        # Determine trigger class
        trigger_class = self._determine_trigger_class(score_result, context)
        
        return TriggerResult(
            trigger_full_analysis=should_trigger,
            trigger_reasons=reasons if reasons else ["Below threshold, monitoring only"],
            trigger_class=trigger_class,
            escalation_priority=priority
        )
    
    def _score_to_priority(self, score: float) -> EscalationPriority:
        """Convert score to escalation priority."""
        for priority, (low, high) in self.priority_thresholds.items():
            if low <= score <= high:
                return priority
        return EscalationPriority.LOW
    
    def _determine_trigger_class(
        self,
        score_result: ScoreResult,
        context: Dict[str, Any]
    ) -> str:
        """Determine trigger classification."""
        category = context.get("category", "general")
        
        if score_result.value >= 9:
            return f"{category}_critical"
        elif score_result.value >= 7:
            return f"{category}_high"
        elif score_result.value >= 5:
            return f"{category}_medium"
        else:
            return f"{category}_monitor"
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return {
            "trigger_threshold": self.trigger_threshold,
            "priority_thresholds": {
                p.value: (low, high)
                for p, (low, high) in self.priority_thresholds.items()
            }
        }
