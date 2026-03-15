# Geo Market Watch Benchmark Suite

**Deterministic evaluation of event analysis quality.**

---

## Purpose

This benchmark suite evaluates Geo Market Watch's ability to:
- Normalize raw events into structured cards
- Score geopolitical signals consistently
- Make appropriate escalation decisions
- Generate actionable market intelligence

---

## Benchmark Cases

| Case ID | Category | Description | Status |
|---------|----------|-------------|--------|
| [case_001](cases/case_001_shipping_disruption/) | Shipping Disruption | Red Sea route closure | ✅ Complete |
| [case_002](cases/case_002_sanctions/) | Sanctions | Technology export controls | ✅ Complete |
| [case_003](cases/case_003_commodity_shock/) | Commodity Shock | Oil supply disruption | ✅ Complete |
| [case_004](cases/case_004_military_escalation/) | Military Escalation | Regional conflict fog | ✅ Complete |
| [case_005](cases/case_005_election_shock/) | Election Shock | Policy regime change | ✅ Complete |
| case_006 | Cross-Market | Contagion mapping | 📝 Template |
| case_007 | Supply Chain | Semiconductor shortage | 📝 Template |
| case_008 | Energy | Pipeline sabotage | 📝 Template |
| case_009 | Financial | Currency crisis | 📝 Template |
| case_010 | Trade | Tariff escalation | 📝 Template |
| case_011-020 | (Reserved) | Various scenarios | 📝 Template |

---

## Case Structure

Each benchmark case contains:

```
cases/case_XXX_name/
├── input.json          # Raw event input
├── expected.json       # Expected outputs
└── notes.md            # Rationale and edge cases
```

**Expected outputs include:**
- Normalized event structure
- Score band (0-10)
- Escalation decision (monitor/analyze)
- Expected watchlist items
- Trigger conditions
- Invalidation scenarios

---

## Running Benchmarks

```bash
# Run all benchmarks
python benchmarks/run_benchmarks.py

# Run specific case
python benchmarks/run_benchmarks.py --case case_001

# Generate report
python benchmarks/run_benchmarks.py --report
```

---

## Evaluation Criteria

| Metric | Target | Description |
|--------|--------|-------------|
| Schema Pass Rate | 100% | Output matches event card schema |
| Score Stability | ±1 band | Same input → same score band |
| Escalation Precision | >80% | Correct monitor/analyze decisions |
| False Escalation | <10% | Unnecessary full analysis triggers |
| Output Completeness | 100% | All required fields present |

---

## Design Principles

1. **Deterministic** — Same input must produce same output
2. **Versioned** — Benchmarks tagged to system versions
3. **Categorized** — Coverage across event types
4. **Documented** — Rationale for each expected output
5. **Extensible** — Easy to add new cases

---

## Contributing New Cases

1. Create directory `cases/case_XXX_description/`
2. Add `input.json` with raw event
3. Add `expected.json` with validated outputs
4. Add `notes.md` explaining rationale
5. Update this README

See [Benchmark Design](docs/evaluation/benchmark-design.md) for detailed guidelines.

---

**Current Coverage:** 5 complete cases, 15 templates  
**Last Updated:** v6.4
