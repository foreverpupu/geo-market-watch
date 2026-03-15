# Case 001: Shipping Disruption

## Scenario

Red Sea route closure forces major carriers to reroute around Africa, adding 10-14 days to Asia-Europe transit times.

## Why This Case

**Classic supply chain disruption with clear market transmission:**
- Immediate impact on shipping rates
- Secondary effects on energy (LNG) and retail (inventory)
- Well-defined invalidation conditions

## Expected Behavior

### Normalization
- Event should be categorized as "shipping"
- Region: "Middle East" or "Global"
- Severity: "high" (not "critical" as no casualties)

### Scoring (8/10)
**Rationale for high score:**
- ✅ Major trade route affected
- ✅ Multiple sectors impacted
- ✅ Clear market transmission mechanism
- ✅ Observable metrics (freight rates)
- ❌ Not permanent (can be resolved)
- ❌ Not systemic (specific route only)

Score band: 7-9 (high)

### Escalation
**Should trigger full analysis because:**
- Score >= 7 (above threshold)
- Clear sector exposure mapping possible
- Actionable trade ideas identifiable

### Watchlist Style
- **Primary metrics:** Freight indices, carrier rates
- **Secondary metrics:** Inventory levels, energy prices
- **Invalidation:** Route reopening, ceasefire, alternative solutions

## Edge Cases

1. **If score < 7:** Would indicate insufficient market impact detection
2. **If no LNG exposure:** Would miss secondary energy market effects
3. **If no invalidation:** Would indicate incomplete analysis

## Version History

- v6.4: Initial case
