# Geo Market Watch v6.4 — Idea Performance Specification

## Purpose

v6.4 introduces **paper trading performance tracking** for approved trade ideas. This allows analysts to track the hypothetical performance of trade ideas from entry to close, enabling quantitative evaluation of the research workflow.

## Paper Tracking vs Live Trading

**Important:** This system tracks **paper (hypothetical) performance only**.

- No actual trades are executed
- No real money is at risk
- Prices are manually entered reference points
- Results are for research evaluation only

This is a **research tool**, not a trading system.

## Entry/Close Reference Methodology

### Entry Reference
- Captures the price at which tracking begins
- Should represent the price when the idea is approved for tracking
- Stored with ISO timestamp for audit trail

### Close Reference
- Captures the price at which tracking ends
- Should represent the price when the thesis is realized or invalidated
- Stored with ISO timestamp for audit trail

### Corrections
- Price references can be corrected if errors are discovered
- All corrections require notes explaining the reason
- Correction history is preserved in lifecycle events

## Performance Calculation Logic

### Long Ideas
```
return_pct = ((close_price - entry_price) / entry_price) * 100
```

Example:
- Entry: $100.00
- Close: $115.00
- Return: ((115 - 100) / 100) * 100 = 15.00%

### Short Ideas
```
return_pct = ((entry_price - close_price) / entry_price) * 100
```

Example:
- Entry: $100.00
- Close: $85.00
- Return: ((100 - 85) / 100) * 100 = 15.00%

### Monitor Ideas
- Monitor ideas are tracked but not classified as directional trades
- Returns are calculated as if long (for consistency)
- Outcome classification may be "unclassified" or "flat"
- No directional bias is assumed

## Benchmark Comparison Support

### Benchmark Return
- Optional benchmark return can be recorded (e.g., S&P 500 return over same period)
- Allows calculation of alpha (excess return)

### Alpha Spread
```
alpha_spread_pct = return_pct - benchmark_return_pct
```

Example:
- Trade return: 15.00%
- Benchmark return: 5.00%
- Alpha spread: 10.00%

## Current Limitations

1. **No Transaction Costs** — Does not account for commissions, slippage, or fees
2. **No Position Sizing** — All trades treated as equal weight
3. **Manual Price Entry** — Requires manual input of prices
4. **No Real-time Data** — No integration with live market data feeds
5. **Paper Only** — No actual trade execution
6. **Single Benchmark** — Only one benchmark can be recorded per trade
7. **Manual MUE/MFE** — Maximum excursion metrics require manual entry

## Maximum Excursion Metrics (MUE/MFE)

### Maximum Unfavorable Excursion (MUE)
- Maximum price move **against** the trade direction
- Expressed as percentage relative to entry price
- Helps evaluate risk management
- Initially entered manually

### Maximum Favorable Excursion (MFE)
- Maximum price move **in favor** of the trade direction
- Expressed as percentage relative to entry price
- Helps identify profit potential
- Initially entered manually

### Future Enhancement
Automatic calculation from price data may be added in future versions.

## Benchmark Hints

The `benchmark_hint` field provides a suggested benchmark index or ETF for performance comparison.

Examples:
- Energy → XLE
- Defense → ITA
- Agriculture → DBA
- Shipping → BDRY

Benchmark hints are suggestions only. Actual benchmark comparison remains optional.

## Paper Tracking Principles

### Local-First
- All data stored locally in SQLite database
- No cloud dependencies
- Full data ownership

### Deterministic
- Same inputs always produce same outputs
- No randomness in calculations
- Reproducible results

### Manually Auditable
- Every price reference has a timestamp
- All corrections are logged
- Full lifecycle trail preserved

### No Execution Assumption
- System assumes hypothetical execution at reference prices
- No guarantee of real-world fill prices
- Results are illustrative

### No Transaction Cost Model
- Current version ignores trading costs
- Future versions may add cost modeling

## Usage Workflow

1. **Idea Approved** → Analyst approves trade idea
2. **Start Tracking** → Record entry price and time
3. **Monitor** → Track idea over time
4. **Close Tracking** → Record close price and time
5. **Review Performance** → Analyze return and outcome

## Data Schema

See `engine/database_models.py` for full schema.

Key fields:
- `entry_price` / `entry_time` — Entry reference
- `close_price` / `close_time` — Close reference
- `return_pct` — Calculated return
- `benchmark_return_pct` — Optional benchmark
- `alpha_spread_pct` — Calculated alpha
- `outcome` — Classification result
- `holding_period_days` — Days held

## Integration

Performance data integrates with:
- Dashboard views
- Lifecycle events
- Export layer (JSON/CSV)
- Query scripts

## Future Enhancements

- Transaction cost modeling
- Multiple benchmark support
- Real-time price feeds
- Position sizing rules
- Portfolio-level analytics
