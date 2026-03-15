# Geo Market Watch v6.4 — Performance Methodology

## Overview

This document defines the methodology for calculating paper trading performance in Geo Market Watch v6.4.

## Return Formulas

### Long Ideas

For long positions, return is calculated as:

```
return_pct = ((close_price - entry_price) / entry_price) * 100
```

**Example:**
- Entry Price: $100.00
- Close Price: $115.00
- Return: ((115 - 100) / 100) * 100 = **15.00%**

### Short Ideas

For short positions, return is calculated as:

```
return_pct = ((entry_price - close_price) / entry_price) * 100
```

**Example:**
- Entry Price: $100.00
- Close Price: $85.00
- Return: ((100 - 85) / 100) * 100 = **15.00%**

## Monitor Idea Treatment

Monitor ideas are tracked but treated differently:

- Returns are calculated using the **long formula** (for consistency)
- Outcome may be classified as "unclassified" or "flat"
- No directional bias is assumed
- Used for tracking ideas that don't fit long/short classification

**Example:**
- Entry Price: $100.00
- Close Price: $102.00
- Return: **2.00%**
- Outcome: "flat" (within -5% to +5% range)

## Holding Period Calculation

Holding period is calculated as the whole-day difference between entry and close timestamps:

```
holding_period_days = (close_date - entry_date).days
```

**Example:**
- Entry Time: 2026-03-15T09:30:00Z
- Close Time: 2026-03-29T16:00:00Z
- Holding Period: **14 days**

## Benchmark Comparison Logic

### Recording Benchmark Return

An optional benchmark return can be recorded:

```python
update_benchmark_return(db_path, trade_idea_id, benchmark_return_pct=5.0)
```

### Alpha Spread Calculation

If benchmark is present, alpha is calculated as:

```
alpha_spread_pct = return_pct - benchmark_return_pct
```

**Example:**
- Trade Return: 15.00%
- Benchmark Return: 5.00%
- Alpha Spread: **10.00%**

If no benchmark is recorded, `alpha_spread_pct` remains null.

## Correction Workflow

### When to Correct

Price references should be corrected when:
- Data entry error discovered
- Price source revised
- Timestamp inaccuracy found

### How to Correct

Use the update script:

```bash
python scripts/update_idea_price_reference.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --field entry \
  --price 73.00 \
  --time 2026-03-15T09:30:00Z \
  --notes "Corrected entry price from 72.50"
```

### Correction Rules

1. **Notes Required** — All corrections must include explanation
2. **Price Validation** — New price must be positive
3. **Time Validation** — Close time must not be earlier than entry time
4. **Auto-Recompute** — Performance is automatically recalculated after correction
5. **Audit Trail** — Correction is logged in lifecycle events

## Example Scenarios

### Long Idea Example

**Setup:**
- Direction: long
- Entry: $100.00 on 2026-03-15
- Close: $115.00 on 2026-03-29

**Results:**
- Return: 15.00%
- Outcome: strong_positive (>10%)
- Holding Period: 14 days

### Short Idea Example

**Setup:**
- Direction: short
- Entry: $100.00 on 2026-03-15
- Close: $85.00 on 2026-03-29

**Results:**
- Return: 15.00%
- Outcome: strong_positive (>10%)
- Holding Period: 14 days

### Monitor Idea Example

**Setup:**
- Direction: monitor
- Entry: $100.00 on 2026-03-15
- Close: $98.00 on 2026-03-29

**Results:**
- Return: -2.00%
- Outcome: flat (-5% to +5%)
- Holding Period: 14 days

### Benchmark-Adjusted Result

**Setup:**
- Direction: long
- Entry: $100.00 on 2026-03-15
- Close: $110.00 on 2026-03-29
- Benchmark Return: 3.00%

**Results:**
- Return: 10.00%
- Outcome: positive (5-10%)
- Alpha Spread: 7.00%
- Holding Period: 14 days

## Validation Rules

### Entry Validation
- Price must be positive
- Time must be valid ISO format
- Idea must be approved

### Close Validation
- Price must be positive
- Time must not be earlier than entry time
- Tracking must be active

### Correction Validation
- Notes are required
- Price must be positive
- Time constraints must be maintained

## Maximum Excursion Metrics

### Maximum Unfavorable Excursion (MUE)

The maximum price move **against** the trade direction during the holding period.

**For Long Ideas:**
```
MUE = ((lowest_price - entry_price) / entry_price) * 100
```

**For Short Ideas:**
```
MUE = ((highest_price - entry_price) / entry_price) * 100
```

Example (Long):
- Entry: $100.00
- Lowest price during tracking: $92.00
- MUE: -8.00%

### Maximum Favorable Excursion (MFE)

The maximum price move **in favor** of the trade direction during the holding period.

**For Long Ideas:**
```
MFE = ((highest_price - entry_price) / entry_price) * 100
```

**For Short Ideas:**
```
MFE = ((entry_price - lowest_price) / entry_price) * 100
```

Example (Long):
- Entry: $100.00
- Highest price during tracking: $118.00
- MFE: +18.00%

### Usage Notes

- MUE/MFE are **optional** fields
- Initially entered manually
- Future versions may support automatic calculation
- Useful for evaluating trade management quality
- Helps identify premature exits or missed opportunities

## Benchmark Hints

### Purpose

The `benchmark_hint` field suggests an appropriate benchmark for performance comparison.

### Common Hints

| Sector | Benchmark Hint | Description |
|--------|----------------|-------------|
| Energy | XLE | Energy Select Sector SPDR |
| Defense | ITA | iShares U.S. Aerospace & Defense |
| Agriculture | DBA | Invesco DB Agriculture Fund |
| Shipping | BDRY | Breakwave Dry Bulk Shipping |
| Technology | XLK | Technology Select Sector SPDR |
| Financial | XLF | Financial Select Sector SPDR |

### Usage

- Hints are **suggestions only**
- Analyst can override with preferred benchmark
- Used for alpha calculation when benchmark_return is provided
- Helps standardize comparisons within sectors

## Limitations

1. **No Transaction Costs** — Commissions, slippage not included
2. **No Dividends** — Dividend adjustments not made
3. **Manual Prices** — Requires manual price entry
4. **Single Currency** — No currency conversion
5. **Paper Only** — Hypothetical results only
6. **Manual MUE/MFE** — Excursion metrics require manual entry
