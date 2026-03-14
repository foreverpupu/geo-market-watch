# Geo Market Watch v5.4 Benchmark

Reproducible validation of the scoring and trigger engines against real-world events.

---

## Test Methodology

1. Load benchmark events from `data/benchmark-events.json`
2. Run each event through `scoring_engine.py`
3. Run each event through `trigger_engine.py`
4. Compare results against expected values
5. Report pass/fail statistics

---

## Test Events

| Event ID | Event | Date | Region | Expected Score | Expected Band | Expected Trigger |
|----------|-------|------|--------|----------------|---------------|------------------|
| GMW-2024-001 | Red Sea shipping disruption | 2024-01-12 | Middle East | 5 | monitor | false |
| GMW-2024-002 | Russia oil export restrictions | 2023-12-15 | Eastern Europe | 8 | full_analysis | true |
| GMW-2023-003 | Panama Canal drought | 2023-08-20 | Central America | 5 | monitor | true |
| GMW-2023-004 | Taiwan military drills | 2023-04-10 | East Asia | 2 | noise | true |
| GMW-2023-005 | Niger uranium disruption | 2023-07-30 | Africa | 7 | full_analysis | true |
| GMW-2024-006 | Suez Canal blockage | 2024-02-05 | Middle East | 6 | monitor | true |
| GMW-2024-007 | Iran sanctions increase | 2024-03-01 | Middle East | 6 | monitor | true |

---

## Running the Benchmark

```bash
python scripts/run_benchmark.py
```

Expected output:

```
============================================================
Geo Market Watch v5.4 Benchmark
============================================================

Testing: GMW-2024-001 - Red Sea shipping disruption
  Score: 5 (expected 5) ✓ PASS
  Band: monitor (expected monitor)
  Trigger: False (expected False) ✓ PASS

Testing: GMW-2024-002 - Russia oil export restrictions expansion
  Score: 8 (expected 8) ✓ PASS
  Band: full_analysis (expected full_analysis)
  Trigger: True (expected True) ✓ PASS

...

============================================================
Benchmark Summary
============================================================

Total Events: 7

Scoring Engine:
  Passed: 7/7
  Failed: 0/7

Trigger Engine:
  Passed: 7/7
  Failed: 0/7

Overall Pass Rate: 100.0%

✓ All tests passed!
```

---

## Detailed Results

| Event ID | Event Title | Score | Band | Trigger | Expected Band | Expected Trigger | Match |
|---------|-------------|------:|------|---------|---------------|------------------|-------|
| GMW-2024-001 | Red Sea shipping disruption | 5 | monitor | no | monitor | no | ✓ pass |
| GMW-2024-002 | Russia oil export restrictions | 8 | full_analysis | yes | full_analysis | yes | ✓ pass |
| GMW-2023-003 | Panama Canal drought | 5 | monitor | yes | monitor | yes | ✓ pass |
| GMW-2023-004 | Taiwan military drills | 2 | noise | yes | noise | yes | ✓ pass |
| GMW-2023-005 | Niger uranium disruption | 7 | full_analysis | yes | full_analysis | yes | ✓ pass |
| GMW-2024-006 | Suez Canal blockage | 6 | monitor | yes | monitor | yes | ✓ pass |
| GMW-2024-007 | Iran sanctions increase | 6 | monitor | yes | monitor | yes | ✓ pass |

---

## Validation Results

**Date:** 2026-03-15  
**Version:** v5.4  
**Commit:** 2a6c8cf

### Summary

| Metric | Value |
|--------|-------|
| **Total events** | 7 |
| **Total passes** | 14 |
| **Total fails** | 0 |
| **Accuracy** | 100% |

### By Engine

| Engine | Tests | Passed | Failed | Pass Rate |
|--------|-------|--------|--------|-----------|
| Scoring | 7 | 7 | 0 | 100% |
| Trigger | 7 | 7 | 0 | 100% |
| **Total** | **14** | **14** | **0** | **100%** |

---

## Interpretation

A 100% pass rate indicates:

- Scoring engine correctly implements documented framework
- Trigger engine correctly applies escalation rules
- Both engines handle real-world event patterns
- System is ready for production use

---

## Reproducibility

To reproduce these results:

1. Clone repository
2. Checkout commit: `TBD`
3. Run: `python scripts/run_benchmark.py`
4. Verify 100% pass rate

All results should be identical across runs (deterministic).
