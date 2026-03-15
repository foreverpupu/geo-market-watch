# Postmortem Workflow

## Overview

Systematic review of event analysis quality to improve methodology and reduce false positives/negatives.

---

## Review Schedule

| Review | Timing | Focus |
|--------|--------|-------|
| **48-hour** | 2 days after event | Initial accuracy check |
| **7-day** | 1 week after | Medium-term validation |
| **30-day** | 1 month after | Full outcome assessment |

---

## Postmortem Template

### Event Summary

```yaml
event_id: evt_001
event_date: 2026-03-15
event_headline: "Red Sea shipping disruption escalates"
analyst: amy
review_date: 2026-04-15  # 30-day review
```

### Initial Hypothesis

**What we predicted:**
- Supply chain disruption lasting 2-4 weeks
- LNG carrier rates to rise 30-50%
- Container shipping costs to increase

**Confidence:** High (8/10)

**Key assumptions:**
- No quick resolution
- Alternative routes insufficient
- Demand remains stable

### Watchlist

| Asset | Initial Level | Trigger | Status |
|-------|--------------|---------|--------|
| Baltic Dry Index | 1800 | >2000 | ✅ Hit 2200 on day 3 |
| LNG Spot Rates | $50k/day | +30% | ✅ Hit $70k on day 5 |
| Flex LNG (FLNG) | $95 | Target $110 | ✅ Hit $115 on day 10 |
| Container Freight | $2000 | +50% | ⚠️ Only +30% |

### Trigger Assessment

**Escalation Decision:** Full analysis (correct)

**Trigger Hit/Miss:**
- ✅ Sector exposure correct (shipping, energy)
- ✅ Trade idea direction correct (long LNG)
- ⚠️ Magnitude underestimated (expected +30%, got +50%)
- ❌ Container impact overestimated

### Invalidation Status

**Original invalidation condition:** "Ceasefire or route reopening"

**Actual outcome:** Route remained closed through review period

**Invalidation triggered:** No

### Market Outcome

| Metric | Predicted | Actual | Variance |
|--------|-----------|--------|----------|
| LNG rates | +30% | +50% | +20pp |
| Container rates | +50% | +30% | -20pp |
| FLNG return | +15% | +21% | +6pp |
| Holding period | 14 days | 21 days | +7 days |

### Accuracy Assessment

**Correct:**
- Direction (long LNG)
- Sector identification
- Escalation decision

**Partially Correct:**
- Magnitude (underestimated LNG, overestimated containers)
- Timeline (extended vs predicted)

**Incorrect:**
- Container shipping impact

### False Positives / Negatives

**False Positives:**
- Container shipping exposure (overweighted)

**False Negatives:**
- Insurance sector impact (missed)
- Alternative route congestion (missed)

### Lessons Learned

**What worked:**
- High score (8/10) appropriate for disruption magnitude
- LNG thesis validated
- Watchlist construction effective

**What didn't:**
- Container exposure overestimated
- Insurance sector missed
- Timeline too optimistic

**Improvements for next time:**
1. Add insurance sector to shipping disruption template
2. Consider alternative route second-order effects
3. Extend default timeline assumptions

### Methodology Updates

**Changes to implement:**
- Update shipping disruption sector list
- Revise magnitude estimation heuristics
- Add 30-day as default review period

**Benchmark updates:**
- Add case_001_shipping to benchmark suite
- Update expected outputs based on actual results

---

## Postmortem Workflow

### Step 1: Schedule Reviews

```python
# After event analysis, schedule reviews
schedule_postmortem(event_id, days=[2, 7, 30])
```

### Step 2: Conduct Review

1. **Gather data** — Market prices, news, outcomes
2. **Fill template** — Document predictions vs actual
3. **Assess accuracy** — What was right/wrong
4. **Identify lessons** — What to improve
5. **Update methodology** — Implement changes

### Step 3: Feed Back to System

**Update benchmark cases:**
```bash
# Update expected outputs based on learnings
python scripts/update_benchmark.py --case case_001 --review postmortem_001.md
```

**Update methodology:**
```bash
# Revise sector lists, scoring weights
python scripts/update_methodology.py --from postmortem_001.md
```

**Update watchlist templates:**
```bash
# Add missing assets, adjust triggers
python scripts/update_templates.py --from postmortem_001.md
```

---

## Sample Postmortem Cases

### Case 1: Shipping Disruption (Success)

**Event:** Red Sea closure  
**Prediction:** LNG rates +30%  
**Actual:** LNG rates +50%  
**Verdict:** Direction correct, magnitude underestimated  
**Action:** Update magnitude heuristics

### Case 2: Sanctions (Partial)

**Event:** Tech export controls  
**Prediction:** Domestic chip makers +20%  
**Actual:** +10% (slower than expected)  
**Verdict:** Direction correct, timeline too aggressive  
**Action:** Extend timeline assumptions for policy impacts

### Case 3: Military Escalation (Miss)

**Event:** Border tension  
**Prediction:** Defense stocks +15%  
**Actual:** No significant move  
**Verdict:** False positive — tension de-escalated quickly  
**Action:** Improve fog-of-war detection, require more confirmation

---

## Integration with Database

### Schema Extension

```sql
-- Add postmortem tracking to events table
ALTER TABLE events ADD COLUMN postmortem_48h TEXT;
ALTER TABLE events ADD COLUMN postmortem_7d TEXT;
ALTER TABLE events ADD COLUMN postmortem_30d TEXT;
ALTER TABLE events ADD COLUMN accuracy_score REAL;
```

### Query Examples

```sql
-- Find events needing 30-day review
SELECT event_id, headline, created_at
FROM events
WHERE postmortem_30d IS NULL
  AND created_at < datetime('now', '-30 days');

-- Calculate analyst accuracy
SELECT analyst, AVG(accuracy_score)
FROM events
WHERE postmortem_30d IS NOT NULL
GROUP BY analyst;
```

---

## Best Practices

1. **Schedule immediately** — Don't wait to schedule postmortems
2. **Be honest** — Document misses, not just hits
3. **Update system** — Feed learnings back to methodology
4. **Track trends** — Look for systematic biases
5. **Share learnings** — Team reviews of postmortems

---

## Metrics

**Track over time:**
- Direction accuracy (% correct long/short)
- Magnitude accuracy (average variance)
- Timeline accuracy (% within expected window)
- False positive rate
- False negative rate

**Goal:** Continuous improvement in all metrics
