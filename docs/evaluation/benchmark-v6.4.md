# Geo Market Watch v6.4 — Benchmark

## Purpose

This benchmark validates the **paper-performance tracking workflow** for approved trade ideas in Geo Market Watch v6.4.

## Test Coverage

### Core Functionality
- [x] Tracking start for approved ideas
- [x] Tracking start rejection for unapproved ideas
- [x] Tracking close with return calculation
- [x] Long idea return calculation
- [x] Short idea return calculation
- [x] Outcome classification
- [x] Holding period calculation
- [x] Dashboard export compatibility

### Validation Rules
- [x] Positive price validation
- [x] Time sequence validation
- [x] Approval status gating
- [x] Correction workflow with notes

### Data Export
- [x] JSON export
- [x] CSV export
- [x] Performance summary
- [x] Dashboard snapshot

## Sample Validation Results

### Test Data

Based on test executions:

| Company | Ticker | Direction | Entry | Close | Return % | Outcome | Status |
|---------|--------|-----------|-------|-------|----------|---------|--------|
| Test Company | TEST | long | 100.00 | 115.00 | 15.00% | strong_positive | closed |
| Short Test | SHORT | short | 100.00 | 85.00 | 15.00% | strong_positive | closed |
| Approved High | TEST | long | 100.00 | - | - | - | tracking |

### Performance Summary

```json
{
  "tracked_count": 3,
  "closed_count": 2,
  "positive_count": 2,
  "negative_count": 0,
  "zero_count": 0,
  "average_return_pct": 15.0,
  "average_alpha_spread_pct": null,
  "outcome_distribution": {
    "strong_positive": 2
  },
  "by_direction": [
    {"direction": "long", "count": 1, "avg_return": 15.0},
    {"direction": "short", "count": 1, "avg_return": 15.0}
  ]
}
```

## Example Scenarios

### Long Idea Example

**Setup:**
- Company: Test Company
- Direction: long
- Entry: $100.00 (2026-03-15)
- Close: $115.00 (2026-03-29)

**Results:**
- Return: 15.00%
- Outcome: strong_positive
- Holding Period: 14 days

**Validation:** ✓ PASS

### Short Idea Example

**Setup:**
- Company: Short Test
- Direction: short
- Entry: $100.00 (2026-03-15)
- Close: $85.00 (2026-03-29)

**Results:**
- Return: 15.00%
- Outcome: strong_positive
- Holding Period: 14 days

**Validation:** ✓ PASS

### Monitor Idea Handling

Monitor ideas are tracked but treated as non-directional:
- Returns calculated using long formula
- Outcome may be "flat" or "unclassified"
- No directional bias assumed

**Validation:** ✓ PASS

### Closed Tracked Idea with Return

**Setup:**
- Entry: $100.00
- Close: $115.00
- Expected Return: 15.00%

**Actual Result:** 15.00%

**Validation:** ✓ PASS

## Interpretation

This benchmark validates the repository's ability to:

1. **Track approved ideas** — Only approved ideas can be tracked
2. **Calculate returns** — Correct formulas for long/short
3. **Classify outcomes** — Proper bucket assignment
4. **Record lifecycle** — Events logged for audit
5. **Export data** — JSON/CSV formats working

### What This Validates

- ✓ Paper trading workflow
- ✓ Performance calculations
- ✓ Data integrity
- ✓ Export functionality

### What This Does NOT Validate

- ✗ Live execution quality
- ✗ Real-world portfolio performance
- ✗ Transaction cost modeling
- ✗ Slippage assumptions

## Limitations Acknowledged

1. **Paper Only** — No actual trades executed
2. **Manual Prices** — Requires manual entry
3. **No Transaction Costs** — Commissions/fees not included
4. **Single Benchmark** — Limited benchmark support
5. **No Real-time Data** — Static price references

## Conclusion

The v6.4 performance tracking layer is **functionally complete** and ready for research use.

All core features validated:
- ✅ Tracking start/close
- ✅ Return calculations
- ✅ Outcome classification
- ✅ Dashboard integration
- ✅ Data export

**Status: READY FOR USE**
