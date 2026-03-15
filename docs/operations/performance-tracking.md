# Geo Market Watch v6.4 — Performance Tracking

**Release Date:** 2026-03-15  
**Version:** v6.4 — Performance Tracking  
**Status:** ✅ Complete

---

## Overview

v6.4 adds **paper trading performance tracking** to the Geo Market Watch research workflow. Approved trade ideas can now be tracked with entry/close prices, returns calculated, and performance analyzed.

---

## New Components

### Database Schema

**New Table:** `trade_idea_performance`

| Column | Type | Description |
|--------|------|-------------|
| performance_id | TEXT PRIMARY KEY | Unique ID |
| trade_idea_id | TEXT UNIQUE | Linked trade idea |
| tracking_status | TEXT | not_started / tracking / closed |
| entry_price | REAL | Entry price |
| entry_time | TEXT | Entry timestamp (ISO) |
| close_price | REAL | Close price |
| close_time | TEXT | Close timestamp (ISO) |
| return_pct | REAL | Calculated return % |
| benchmark_return_pct | REAL | Benchmark return % |
| alpha_spread_pct | REAL | Return - Benchmark |
| outcome | TEXT | win / loss / breakeven |
| holding_period_days | INTEGER | Days held |
| notes | TEXT | Tracking notes |

### Performance Engine

**File:** `engine/performance_engine.py`

**Functions:**
- `start_tracking()` — Start tracking an approved idea
- `close_tracking()` — Close tracking and compute performance
- `update_benchmark_return()` — Update benchmark for alpha calculation
- `recompute_performance()` — Recalculate metrics
- `list_tracked_ideas()` — List all tracked ideas

### CLI Scripts

| Script | Purpose |
|--------|---------|
| `scripts/start_idea_tracking.py` | Start tracking with entry price |
| `scripts/close_trade_idea.py` | Close with close price, compute return |
| `scripts/update_idea_price_reference.py` | Correct entry/close prices |
| `scripts/list_tracked_ideas.py` | List tracked ideas with performance |

---

## Workflow

```
Trade Idea Approved
        ↓
Start Tracking (entry price, time)
        ↓
Monitor / Hold
        ↓
Close Tracking (close price, time)
        ↓
Auto-compute:
  • Return %
  • Outcome (win/loss/breakeven)
  • Holding period
  • Alpha spread (if benchmark set)
```

---

## Return Calculation

### Long Ideas
```
return_pct = ((close_price - entry_price) / entry_price) * 100
```

### Short Ideas
```
return_pct = ((entry_price - close_price) / entry_price) * 100
```

### Outcome Classification
- **win** — return > 5%
- **loss** — return < -5%
- **breakeven** — -5% ≤ return ≤ 5%

---

## Usage Examples

### Start Tracking
```bash
python scripts/start_idea_tracking.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --entry-price 72.50 \
  --entry-time 2026-03-15T09:30:00Z \
  --notes "Strong momentum confirmed"
```

### Close Tracking
```bash
python scripts/close_trade_idea.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --close-price 79.10 \
  --close-time 2026-03-29T16:00:00Z \
  --notes "Target reached"
```

### Update Price Reference
```bash
# Correct entry
python scripts/update_idea_price_reference.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --field entry \
  --price 73.00 \
  --time 2026-03-15T09:30:00Z \
  --notes "Corrected entry price"

# Correct close
python scripts/update_idea_price_reference.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --field close \
  --price 78.80 \
  --time 2026-03-29T16:00:00Z \
  --notes "Corrected close price"
```

### List Tracked Ideas
```bash
# All tracked ideas
python scripts/list_tracked_ideas.py --db data/geo_alpha.db

# Only currently tracking
python scripts/list_tracked_ideas.py --db data/geo_alpha.db --status tracking

# Only closed
python scripts/list_tracked_ideas.py --db data/geo_alpha.db --status closed
```

---

## Validation Rules

### Start Tracking Rules
- ✅ Idea must be approved (analyst_status = approved OR approval_status = approved)
- ✅ Entry price must be positive
- ✅ Entry time must be valid ISO format

### Close Tracking Rules
- ✅ Tracking must be active (status = tracking)
- ✅ Close price must be positive
- ✅ Close time must not be earlier than entry time

### Update Price Rules
- ✅ Notes required for any correction
- ✅ Price must be positive
- ✅ Time validation (close >= entry)

---

## Integration with Dashboard

Performance data is included in dashboard views:

```python
from engine.dashboard_views import get_idea_summary

summary = get_idea_summary(db_path, trade_idea_id)
# Includes: idea + reviews + lifecycle + performance
```

---

## Test Results

| Test | Expected | Result |
|------|----------|--------|
| Start tracking approved idea | Success | ✅ PASS |
| Start tracking pending idea | Rejected | ✅ PASS |
| Negative entry price | Rejected | ✅ PASS |
| Close tracking | Computes return | ✅ PASS |
| Close time < entry time | Rejected | ✅ PASS |
| Long return calculation | Correct % | ✅ PASS |
| Short return calculation | Correct % | ✅ PASS |
| Update price with notes | Success | ✅ PASS |
| Update price without notes | Rejected | ✅ PASS |

---

## System Evolution

Geo Market Watch now supports:

```
Event Detection
    ↓
Event Database
    ↓
Exposure Mapping
    ↓
Trade Idea Generation
    ↓
Analyst Review Workflow
    ↓
Lifecycle Management
    ↓
Performance Tracking ← NEW
```

**Result:** A complete Geo Macro Research Platform with paper trading analytics.

---

## Next Steps (v6.5+)

- [ ] Performance analytics dashboard
- [ ] Win rate by sector/direction
- [ ] Alpha attribution analysis
- [ ] Benchmark integration (SPY, sector ETFs)
- [ ] Performance reporting (monthly/quarterly)
- [ ] Trade journaling notes

---

**v6.4 STATUS: COMPLETE ✅**
