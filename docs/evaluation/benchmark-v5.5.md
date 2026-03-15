# Geo Market Watch v5.5 Benchmark

Validation of the complete agent loop from intake to notification.

---

## Test Objective

Verify that all 4 nodes of the agent loop work correctly:
1. Intake normalization
2. Deduplication
3. Scoring & trigger
4. Notification generation

---

## Test Data

**File:** `data/intake-sample.json`

| # | Event | Expected Outcome |
|---|-------|------------------|
| 1 | Red Sea shipping disruption | Full Analysis (transport disruption) |
| 2 | Red Sea shipping disruption (duplicate) | Filtered (duplicate) |
| 3 | Russia oil export restrictions | Full Analysis (score + sanctions) |
| 4 | Panama Canal drought | Full Analysis (transport disruption) |
| 5 | Taiwan military drills | Full Analysis (military escalation) |
| 6 | Niger uranium disruption | Full Analysis (score + supply disruption) |
| 7 | Suez Canal blockage | Full Analysis (transport disruption) |
| 8 | Iran sanctions increase | Full Analysis (sanctions escalation) |

**Expected Results:**
- Total intake: 8 events
- Duplicates: 1 (Red Sea #2)
- New events processed: 7
- Full Analysis notifications: 7
- Monitor notifications: 0

---

## Running the Benchmark

```bash
python scripts/run_agent_loop.py \
  --input data/intake-sample.json \
  --memory data/dedupe-memory.json \
  --output outputs/
```

---

## Expected Output

```
============================================================
Geo Market Watch v5.5 — Agent Loop Summary
============================================================

Intake items: 8
Normalized events: 8

New events: 7
Duplicate events: 1

Monitor outcomes: 0
Full Analysis outcomes: 7

Processed Events:
  • Red Sea shipping disruption... (Score: 5) → Full Analysis
  • Russia expands oil export restrictions... (Score: 8) → Full Analysis
  • Panama Canal drought shipping restrictions... (Score: 5) → Full Analysis
  • Taiwan military drills escalation... (Score: 2) → Full Analysis
  • Niger uranium export disruption... (Score: 7) → Full Analysis
  • Suez Canal temporary blockage... (Score: 6) → Full Analysis
  • Iran sanctions enforcement increase... (Score: 6) → Full Analysis

============================================================
```

---

## File Outputs

**Generated files in `outputs/`:**

```
full_analysis_093fa8450fab.md  # Russia oil
full_analysis_299303745565.md  # Suez Canal
full_analysis_310290c28f97.md  # Panama Canal
full_analysis_3d0a3f401f47.md  # Taiwan drills
full_analysis_5f91c016c755.md  # Red Sea
full_analysis_a02550cd8955.md  # Iran sanctions
full_analysis_a135a9a01e73.md  # Niger uranium
```

**Each file contains:**
- Event metadata
- Score and band
- Trigger decision
- Reasons (for handoff)
- Summary
- Next action

---

## Validation Results

**Date:** 2026-03-15  
**Version:** v5.5  
**Commit:** f862159

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Intake loaded | 8 items | 8 items | ✓ PASS |
| Normalized | 8 events | 8 events | ✓ PASS |
| Duplicates filtered | 1 | 1 | ✓ PASS |
| New events processed | 7 | 7 | ✓ PASS |
| Scores computed | 7 | 7 | ✓ PASS |
| Triggers evaluated | 7 | 7 | ✓ PASS |
| Notifications written | 7 | 7 | ✓ PASS |
| Dedupe memory updated | Yes | Yes | ✓ PASS |

**Overall:** 8/8 checks passed (100%)

---

## Interpretation

A successful benchmark run indicates:

- ✓ All 4 nodes execute correctly
- ✓ Deduplication prevents duplicate processing
- ✓ Scoring engine produces correct scores
- ✓ Trigger engine identifies escalation conditions
- ✓ Notifier generates valid markdown
- ✓ File I/O works correctly
- ✓ Agent loop is ready for use

---

## Reproducibility

To reproduce:

1. Clone repository
2. Checkout: `git checkout v5.5`
3. Run: `python scripts/run_agent_loop.py --input data/intake-sample.json --memory data/dedupe-memory.json --output outputs/`
4. Verify output matches expected results

Results should be identical across runs (deterministic).

---

## Limitations

This benchmark validates:
- ✓ The agent loop workflow
- ✓ Component integration
- ✓ File-based I/O

This benchmark does NOT validate:
- ✗ Live news ingestion
- ✗ Fuzzy deduplication
- ✗ Database persistence
- ✗ Scheduled execution
- ✗ Multi-agent orchestration

See `docs/minimal-agent-architecture.md` for scope details.
