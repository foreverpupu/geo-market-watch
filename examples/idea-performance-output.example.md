# Example: Closed Tracked Idea Output

## Trade Details

- **Company:** Flex LNG Ltd
- **Ticker:** FLNG
- **Direction:** Long
- **Conviction:** High

## Tracking Record

| Field | Value |
|-------|-------|
| Tracking Status | closed |
| Entry Price | $100.00 |
| Entry Time | 2026-03-15T09:30:00Z |
| Close Price | $115.00 |
| Close Time | 2026-03-29T16:00:00Z |
| Return | +15.00% |
| Benchmark Return | +5.00% |
| Alpha Spread | +10.00% |
| Outcome | strong_positive |
| Holding Period | 14 days |

## Performance Summary

```
Return Calculation:
  (Close - Entry) / Entry * 100
  = (115 - 100) / 100 * 100
  = 15.00%

Alpha Calculation:
  Return - Benchmark
  = 15.00% - 5.00%
  = 10.00%
```

## Outcome Classification

**strong_positive** — Return exceeded 10% threshold

## Notes

"Strong momentum play on Red Sea disruption. Target reached after two weeks of sustained price appreciation. Thesis validated."

## Lifecycle Events

1. **2026-03-15T09:30:00Z** — tracking_started
   - Entry price: $100.00
   - Notes: Tracking started after analyst approval

2. **2026-03-29T16:00:00Z** — tracking_closed
   - Close price: $115.00
   - Return: 15.00%
   - Outcome: strong_positive
   - Notes: Target reached

## Export Data

### JSON
```json
{
  "trade_idea_id": "idea-6f2g3h4i...",
  "company_name": "Flex LNG Ltd",
  "ticker": "FLNG",
  "direction": "long",
  "entry_price": 100.0,
  "close_price": 115.0,
  "return_pct": 15.0,
  "outcome": "strong_positive",
  "holding_period_days": 14
}
```

### CSV
```csv
company_name,ticker,direction,entry_price,close_price,return_pct,outcome,holding_period_days
Flex LNG Ltd,FLNG,long,100.0,115.0,15.0,strong_positive,14
```
