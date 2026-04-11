# Geo Market Watch v6.4 — RELEASED

**Date:** 2026-03-15  
**Version:** v6.4 — Idea Performance Tracking  
**Status:** ✅ RELEASED

---

## What v6.4 Delivers

**Paper-Performance Tracking for Approved Trade Ideas**

v6.4 completes the research workflow loop:

```
Idea Generated
    ↓
Analyst Reviewed
    ↓
Approved
    ↓
Tracked (entry price)
    ↓
Closed (close price)
    ↓
Measured (return %, outcome)
```

This upgrades Geo Market Watch from a **research workflow system** to a **performance-aware research platform**.

---

## Key Features

### Performance Tracking
- Entry/close reference prices with timestamps
- Automatic return calculation (long/short)
- Holding period tracking
- Outcome classification (5 buckets)

### Risk Metrics
- Maximum Unfavorable Excursion (MUE)
- Maximum Favorable Excursion (MFE)
- Benchmark comparison with alpha spread

### Data Export
- JSON export for analysis
- CSV export with sanitized fields
- Performance summary statistics

### Audit Trail
- Lifecycle event integration
- Price correction tracking
- Full history preservation

---

## File Manifest

### Core Engine
- `engine/performance_engine.py` — Performance tracking
- `engine/export_layer.py` — Data export
- `engine/dashboard_views.py` — Dashboard views

### CLI Scripts
- `scripts/start_idea_tracking.py`
- `scripts/close_trade_idea.py`
- `scripts/update_idea_price_reference.py`
- `scripts/list_tracked_ideas.py`
- `scripts/export_dashboard_data.py`

### Documentation
- `docs/idea-performance-spec.md`
- `docs/performance-methodology.md`
- `docs/idea-outcome-classification.md`
- `docs/benchmark-v6.4.md`

### Examples & Data
- `examples/idea-performance.example.json`
- `examples/idea-performance-output.example.md`
- `data/idea-performance-sample.json`

---

## Quick Start

```bash
# Start tracking
python scripts/start_idea_tracking.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --entry-price 72.50 \
  --entry-time 2026-03-15T09:30:00Z

# Close tracking
python scripts/close_trade_idea.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --close-price 79.10 \
  --close-time 2026-03-29T16:00:00Z

# View performance
python scripts/list_tracked_ideas.py --db data/geo_alpha.db

# Export data
python scripts/export_dashboard_data.py \
  --db data/geo_alpha.db \
  --output exports/
```

---

## Important Notes

**Paper Tracking Only:**
- No live trading
- No broker integration
- Hypothetical returns only
- For research evaluation

**Manual Data Entry:**
- Price references entered manually
- MUE/MFE initially manual
- Future versions may add automation

---

## System Evolution

**v6.4 completes the platform:**

```
Prompt framework
→ Structured monitoring
→ Executable scoring
→ Local agent loop
→ Event database
→ Dashboard layer
→ Exposure engine
→ Analyst workflow
→ Performance tracking ← v6.4
```

**Not yet:**
- Live execution
- Broker connectivity
- Portfolio management
- Automated trading

---

## Validation Results

✅ All 15 required files exist  
✅ Database schema correct  
✅ Engine imports working  
✅ Outcome classification accurate  
✅ Export functionality verified  
✅ Query scripts tested  
✅ Documentation complete  

---

## Git Tag

```bash
git tag -a v6.4 -m "Geo Market Watch v6.4 — Idea Performance Tracking"
git push origin v6.4
```

---

**v6.4 RELEASED** ✅

*Performance-aware research platform ready for use.*
