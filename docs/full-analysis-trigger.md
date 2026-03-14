# Full Analysis Trigger Rules

Full Analysis Mode performs the complete Geo Market Watch framework.

It includes:

1. Confirmed Facts
2. Market Interpretation
3. Scenario Analysis
4. Supply Chain Translation
5. Sector Exposure
6. Watchlist
7. Trigger Signals
8. Invalidation Conditions
9. Monitoring Plan

Because Full Analysis is resource intensive, it should only be triggered when events meet predefined criteria.

---

# Trigger Conditions

Full analysis should be triggered if **any of the following conditions are met**.

---

## Condition 1 — Signal Score Threshold

**Signal Score ≥ 7**

This indicates a high probability of market relevance.

---

## Condition 2 — Confirmed Supply Disruption

Examples:

- oil exports halted 
- mining production stopped 
- LNG terminal shutdown

Physical supply disruptions always require full analysis.

---

## Condition 3 — Strategic Transport Disruption

Examples:

- Suez Canal closure 
- Panama Canal restrictions 
- Strait of Hormuz blockade risk

Major logistics routes impact global markets.

---

## Condition 4 — Major Sanctions Escalation

Examples:

- energy export bans 
- financial system sanctions 
- technology export restrictions

These events often produce cross-sector impacts.

---

## Condition 5 — Military Escalation

Examples:

- direct conflict between states 
- naval blockade 
- strategic strikes

Military escalation introduces extreme uncertainty.

---

# Trigger Logic

Scout Mode evaluates events first.

If triggers are met:

```
Scout Mode → Full Analysis Mode
```

---

# Example

**Event:** Russia expands oil export restrictions

**Signal score:** 7

**Trigger condition:** Signal Score Threshold

**Result:** Full Analysis Mode initiated
