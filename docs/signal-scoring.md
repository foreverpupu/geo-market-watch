# Signal Scoring Guide

This document defines the signal scoring system used in Geo Market Watch.

Signal scores help prioritize events and determine whether to escalate to Full Analysis Mode.

---

# Scoring Scale

Events are scored on a 0–10 scale.

| Score | Category | Action |
|-------|----------|--------|
| 0–3 | Noise | Archive |
| 4–6 | Watch | Scout monitoring |
| 7–8 | Strong signal | Trigger full analysis |
| 9–10 | Major shock | Immediate full analysis + alerts |

---

# Scoring Factors

## Physical Impact (40%)

Measures actual disruption to physical infrastructure or supply.

| Indicator | Weight |
|-----------|--------|
| Supply route disruption | 15% |
| Production halt | 15% |
| Infrastructure damage | 10% |

## Market Exposure (30%)

Measures potential market impact.

| Indicator | Weight |
|-----------|--------|
| Affected commodity importance | 15% |
| Global market share | 10% |
| Price volatility potential | 5% |

## Escalation Risk (20%)

Measures likelihood of event worsening.

| Indicator | Weight |
|-----------|--------|
| Conflict intensity trend | 10% |
| Policy uncertainty | 10% |

## Source Reliability (10%)

Measures confidence in information.

| Source Tier | Score |
|-------------|-------|
| Tier 1 (Reuters, Bloomberg) | 10% |
| Tier 2 (Regional wires) | 7% |
| Tier 3 (Social media) | 3% |

---

# Score Calculation Example

**Event:** Red Sea shipping disruption

| Factor | Score | Weight | Weighted |
|--------|-------|--------|----------|
| Supply route disruption | 8 | 15% | 1.2 |
| Production halt | 2 | 15% | 0.3 |
| Infrastructure damage | 1 | 10% | 0.1 |
| Commodity importance | 7 | 15% | 1.05 |
| Global market share | 6 | 10% | 0.6 |
| Price volatility | 5 | 5% | 0.25 |
| Conflict trend | 6 | 10% | 0.6 |
| Policy uncertainty | 5 | 10% | 0.5 |
| Source reliability | 10 | 10% | 1.0 |
| **Total** | | | **5.6** |

**Rounded: 6 / 10**

**Action:** Scout monitoring continues

---

# Special Cases

## Automatic Escalation (Score ≥ 7)

Events automatically escalate to Full Analysis Mode when:

- Major supply route completely blocked
- Strategic commodity export halted
- Military conflict expands to new region
- Sanctions affect global commodity markets

## Automatic Archive (Score ≤ 3)

Events are archived when:

- Purely political rhetoric
- Localized incident with no supply impact
- Already priced-in market event
- Unverified social media reports

---

# Score Review

Scores should be reviewed and updated:

- Every monitoring cycle (6h / 12h / 24h)
- When new information arrives
- When escalation triggers activate

Score changes may trigger escalation or invalidation.
