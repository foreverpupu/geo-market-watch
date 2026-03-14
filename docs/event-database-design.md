# Event Database Design

This document outlines the core database schema for storing Geo Market Watch events.

Designed for SQL databases (PostgreSQL, MySQL) or document stores (MongoDB).

---

# Core Tables

## Events

Stores core geopolitical events.

| Field | Type | Description |
|-------|------|-------------|
| event_id | string | unique identifier (GMW-YYYY-NNNN) |
| title | string | event name |
| date_detected | date | detection date |
| region | string | affected region |
| category | string | event type |
| signal_score | integer | 0–10 score |
| escalation_status | string | scout / full_analysis / resolved |
| summary | text | brief description |
| created_at | timestamp | record creation |
| updated_at | timestamp | last update |

**Example:**
```
event_id: GMW-2024-001
title: Red Sea Shipping Disruption
date_detected: 2024-01-12
region: Middle East
category: Maritime disruption
signal_score: 6
escalation_status: scout
```

---

## Sources

Tracks news sources used to detect events.

| Field | Type | Description |
|-------|------|-------------|
| source_id | string | unique identifier |
| event_id | string | linked event (foreign key) |
| source_name | string | publisher (Reuters, Bloomberg, etc.) |
| url | string | article link |
| date_published | date | publication date |
| tier | integer | 1/2/3 source tier |
| reliability_score | integer | 0-10 confidence |

---

## Market Exposure

Stores affected sectors and commodities.

| Field | Type | Description |
|-------|------|-------------|
| exposure_id | string | unique identifier |
| event_id | string | linked event (foreign key) |
| sector | string | Energy, Shipping, Mining, etc. |
| commodity | string | Oil, LNG, Uranium, etc. |
| impact_type | string | disrupts / reroutes / raises_cost |
| confidence | string | high / medium / low |

---

## Watchlist

Potentially affected companies and assets.

| Field | Type | Description |
|-------|------|-------------|
| watchlist_id | string | unique identifier |
| event_id | string | linked event (foreign key) |
| company | string | company name |
| ticker | string | stock ticker |
| direction_bias | string | long / short / two_way |
| thesis | text | investment thesis |
| trigger_signal | array | conditions to watch |
| invalidation_condition | array | conditions to exit |
| time_horizon | string | immediate / short / medium |

---

## Signal History

Tracks signal score changes over time.

| Field | Type | Description |
|-------|------|-------------|
| history_id | string | unique identifier |
| event_id | string | linked event (foreign key) |
| timestamp | datetime | when score recorded |
| signal_score | integer | 0-10 score at time |
| reason | text | why score changed |

---

# Event Lifecycle

Events progress through defined stages.

```
┌─────────────────┐
│  Scout Detection │
└────────┬────────┘
         ↓
┌─────────────────┐
│   Monitoring    │
│  (score updates)│
└────────┬────────┘
         ↓ (score ≥ 7)
┌─────────────────┐
│  Full Analysis  │
│   (9-section)   │
└────────┬────────┘
         ↓
┌─────────────────┐
│    Resolution   │
│ (invalidation)  │
└─────────────────┘
```

**Status values:**
- `scout` - Initial detection, monitoring
- `full_analysis` - Deep analysis completed
- `monitoring` - Post-analysis watch
- `resolved` - Invalidated or concluded
- `archived` - Low priority, no longer tracked

---

# Example Event Record

**Event:**
```
event_id: GMW-2024-001
title: Red Sea Shipping Disruption
region: Middle East
category: Maritime disruption
signal_score: 6
status: Scout Monitoring
```

**Sources:**
```
source_id: SRC-001
event_id: GMW-2024-001
source_name: Reuters
url: https://www.reuters.com/...
tier: 1
```

**Market Exposure:**
```
exposure_id: EXP-001
event_id: GMW-2024-001
sector: Shipping
commodity: Container freight
impact_type: reroutes
```

**Watchlist:**
```
watchlist_id: WL-001
event_id: GMW-2024-001
company: ZIM Integrated Shipping
ticker: ZIM
direction_bias: two_way
trigger_signal: ["Freight rates elevated >2 weeks"]
invalidation_condition: ["Red Sea reopens"]
```

---

# Indexing Recommendations

For performance, create indexes on:

- `events.date_detected` (time-series queries)
- `events.signal_score` (filtering by priority)
- `events.escalation_status` (workflow queries)
- `sources.event_id` (join optimization)
- `watchlist.event_id` (join optimization)

---

# Scaling Considerations

**Small scale (100s events):**
- SQLite or JSON files sufficient

**Medium scale (1000s events):**
- PostgreSQL with proper indexing

**Large scale (10000s+ events):**
- Partition by date_detected
- Archive old events to cold storage
- Use read replicas for queries
