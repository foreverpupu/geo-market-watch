# Benchmark Design

## Purpose

Establish a deterministic, versioned benchmark suite for evaluating Geo Market Watch's event analysis quality.

## Design Principles

### 1. Deterministic
Same input must produce same output across runs and versions (unless explicitly changed).

### 2. Categorized
Coverage across event types:
- Shipping disruption
- Sanctions / export controls
- Commodity supply shock
- Military escalation / fog of war
- Election / policy shock
- Cross-market exposure

### 3. Versioned
Benchmarks tagged to system versions. v6.4 benchmarks may differ from v7.0 benchmarks.

### 4. Documented
Each case includes rationale for expected outputs.

### 5. Extensible
Easy to add new cases without breaking existing ones.

## Case Structure

```
case_XXX_description/
├── input.json          # Raw event input
├── expected.json       # Expected outputs
└── notes.md            # Rationale and edge cases
```

### Input Format

```json
{
  "id": "case_001_shipping_disruption",
  "headline": "...",
  "summary": "...",
  "source": "...",
  "region": "...",
  "category": "...",
  "timestamp": "...",
  "urls": [...]
}
```

### Expected Output Format

```json
{
  "normalized_event": {...},
  "score": {
    "value": 8,
    "band": "high",
    "min_expected": 7,
    "max_expected": 9
  },
  "escalation": {
    "decision": "full_analysis",
    "rationale": "..."
  },
  "expected_outputs": {
    "sectors": [...],
    "watchlist_items": [...],
    "trade_ideas": [...]
  }
}
```

## Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Schema Pass Rate | 100% | JSON schema validation |
| Score Stability | ±1 band | Same input, multiple runs |
| Escalation Precision | >80% | Correct monitor/analyze decisions |
| False Escalation | <10% | Unnecessary full analysis |
| Output Completeness | 100% | All required fields present |

## Running Benchmarks

```bash
# Run all
python benchmarks/run_benchmarks.py

# Run specific case
python benchmarks/run_benchmarks.py --case case_001

# Generate report
python benchmarks/run_benchmarks.py --report
```

## Adding New Cases

1. Create directory `cases/case_XXX_description/`
2. Add `input.json` with raw event
3. Add `expected.json` with validated outputs
4. Add `notes.md` explaining rationale
5. Update `benchmarks/README.md`
6. Run benchmarks to verify

## Version History

- v6.4: Initial 5-case benchmark suite
- Future: Expand to 20 cases covering all categories
