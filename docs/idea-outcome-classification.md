# Geo Market Watch v6.4 — Idea Outcome Classification

## Overview

This document defines the outcome classification system for tracked trade ideas in Geo Market Watch v6.4.

## Classification Buckets

Outcomes are classified into the following buckets based on return percentage:

| Classification | Return Range | Description |
|----------------|--------------|-------------|
| **strong_positive** | > 10% | Significant gain |
| **positive** | > 5% to 10% | Moderate gain |
| **flat** | -5% to 5% | Near breakeven |
| **negative** | -10% to -5% | Moderate loss |
| **strong_negative** | < -10% | Significant loss |
| **unclassified** | N/A | No return data available |

## Classification Logic

```python
def classify_outcome(return_pct: float) -> str:
    if return_pct > 10:
        return 'strong_positive'
    elif return_pct > 5:
        return 'positive'
    elif return_pct < -10:
        return 'strong_negative'
    elif return_pct < -5:
        return 'negative'
    else:
        return 'flat'
```

## Classification Examples

### Strong Positive
- Return: +15.00%
- Classification: **strong_positive**
- Interpretation: Trade significantly outperformed

### Positive
- Return: +7.50%
- Classification: **positive**
- Interpretation: Trade moderately outperformed

### Flat
- Return: +2.00%
- Classification: **flat**
- Interpretation: Trade roughly broke even

### Negative
- Return: -7.50%
- Classification: **negative**
- Interpretation: Trade underperformed moderately

### Strong Negative
- Return: -15.00%
- Classification: **strong_negative**
- Interpretation: Trade significantly underperformed

### Unclassified
- Return: N/A (tracking not closed)
- Classification: **unclassified**
- Interpretation: Outcome not yet determined

## Important Disclaimer

**These classifications are paper evaluation buckets only.**

They are:
- **Not investment advice**
- **Not performance guarantees**
- **For research evaluation only**
- **Based on hypothetical (paper) trades**

## Usage Context

### Research Evaluation
- Track research workflow effectiveness
- Compare analyst conviction levels vs outcomes
- Identify patterns in successful/unsuccessful ideas

### Portfolio Analysis
- Aggregate outcomes across multiple ideas
- Calculate win rates by sector/direction
- Evaluate risk/reward profiles

### Not For
- Live trading decisions
- Investment recommendations
- Regulatory reporting
- Client communications

## Aggregation Examples

### Win Rate Calculation
```
win_rate = (strong_positive_count + positive_count) / total_closed_count
```

### Loss Rate Calculation
```
loss_rate = (strong_negative_count + negative_count) / total_closed_count
```

### Flat Rate
```
flat_rate = flat_count / total_closed_count
```

## Dashboard Integration

Outcome classifications appear in:
- Performance summary statistics
- Closed idea performance views
- Export files (JSON/CSV)
- Dashboard snapshots

## Future Enhancements

Potential future additions:
- Risk-adjusted classifications (Sharpe, Sortino)
- Sector-specific benchmarks
- Time-based outcome analysis
- Conviction-outcome correlation tracking
