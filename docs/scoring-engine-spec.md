# Scoring Engine Specification

This document specifies the minimal scoring engine for Geo Market Watch v5.4.

---

## Purpose

Convert Event Card indicators into a deterministic signal score (0-10).

---

## Scoring Dimensions

| Dimension | Max Score | Description |
|-----------|-----------|-------------|
| physical_disruption | 3 | Actual supply or production disruption |
| transport_impact | 2 | Shipping routes, logistics, pipelines |
| policy_sanctions | 2 | Government or regulatory changes |
| market_transmission | 2 | Immediate observable market effects |
| escalation_risk | 1 | Potential for rapid deterioration |

**Total maximum: 10**

---

## Input Format

```json
{
  "event_title": "Red Sea shipping disruption",
  "date_detected": "2024-01-12",
  "region": "Middle East",
  "category": "Maritime disruption",
  "indicators": {
    "physical_disruption": 1,
    "transport_impact": 2,
    "policy_sanctions": 0,
    "market_transmission": 1,
    "escalation_risk": 1
  }
}
```

---

## Output Format

```json
{
  "event_title": "Red Sea shipping disruption",
  "score": 5,
  "band": "monitor"
}
```

---

## Band Mapping

| Score Range | Band | Action |
|-------------|------|--------|
| 0–3 | noise | Archive event |
| 4–6 | monitor | Continue Scout Mode |
| 7–8 | full_analysis | Trigger Full Analysis Mode |
| 9–10 | major_shock | Immediate full analysis + alerts |

---

## Validation Rules

- All 5 indicators must be present
- Each indicator must be an integer
- No indicator may exceed its maximum
- No indicator may be negative

---

## Implementation

See: `engine/scoring_engine.py`

The implementation:
- Is deterministic (same input → same output)
- Has no external dependencies
- Validates inputs strictly
- Returns clear error messages

---

## Example Calculation

**Event:** Red Sea shipping disruption

| Indicator | Value | Max | Weight |
|-----------|-------|-----|--------|
| physical_disruption | 1 | 3 | 1/3 |
| transport_impact | 2 | 2 | 2/2 |
| policy_sanctions | 0 | 2 | 0/2 |
| market_transmission | 1 | 2 | 1/2 |
| escalation_risk | 1 | 1 | 1/1 |
| **Total** | **5** | **10** | **50%** |

**Result:** Score = 5, Band = "monitor"

---

## Testing

Run benchmark:

```bash
python scripts/run_benchmark.py
```

Expected: 100% pass rate on all test events.

---

## Current Limitations

**This is v5.4 — the first executable layer, not a complete autonomous system.**

### What is NOT yet implemented:

- **Automatic extraction from raw articles** — The engine requires pre-structured Event Card inputs. It cannot parse news articles or extract indicators automatically.

- **Event deduplication** — Multiple reports of the same event are treated as separate inputs. No merging or duplicate detection.

- **Ingestion pipeline** — No live connection to news feeds, RSS, or APIs. Events must be provided manually or by external systems.

- **Persistence layer** — No database storage. All data exists in memory during execution.

- **Multi-agent orchestration** — Single-threaded execution. No coordination between multiple analysis agents.

### What IS implemented:

- ✅ Deterministic scoring from structured inputs
- ✅ Explicit trigger rules with clear escalation criteria
- ✅ Input validation with descriptive error messages
- ✅ Reproducible benchmark testing with 100% pass rate
- ✅ Zero external dependencies (no APIs, no LLM calls)

### Roadmap:

Future releases will address these limitations:
- v5.5+: Article parsing and automatic indicator extraction
- v5.6+: Event deduplication and entity resolution
- v6.0+: Live ingestion pipeline and database persistence
- v6.5+: Multi-agent orchestration and autonomous monitoring

**Status:** The engine is ready for integration into larger systems, but remains a focused, reliable component rather than a complete end-to-end solution.
