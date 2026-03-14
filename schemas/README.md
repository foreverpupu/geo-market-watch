# Geo Market Watch JSON Schemas

This directory contains the structured data schemas for the Geo Market Watch system.

All schemas follow **JSON Schema Draft 2020-12** standard.

---

## Schema Architecture Overview

The three-layer schema architecture transforms raw geopolitical inputs into structured, actionable market intelligence:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Event Input                                        │
│  schemas/event-object.json                                   │
│  "Normalize everything into a standard event format"        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Market Mapping                                     │
│  schemas/watchlist-item.json                                 │
│  "Transform events into testable investment theses"         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Analysis Output                                    │
│  schemas/analysis-output.json                                │
│  "Package everything into a complete intelligence product"  │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Event Object (`event-object.json`)

### Purpose
**Solves the "input unification" problem.**

Regardless of source—user links, Scout-discovered news, government announcements, or custom feeds—everything normalizes into a standard Event Object.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string | Unique identifier (pattern: `gmw-YYYY-NNNN`) |
| `created_at` | string (date-time) | System creation timestamp |
| `event_timestamp` | string (date-time) | When the event occurred |
| `title` | string | Event title (5-300 chars) |
| `summary` | string | Event summary (20-4000 chars) |
| `event_type` | enum | One of 19 types (military_escalation, sanctions, etc.) |
| `status` | enum | confirmed, partially_confirmed, unconfirmed, disputed, resolved |
| `source_tier` | integer | 1-4 (1 = highest quality) |
| `confidence_level` | enum | low, medium, high |
| `geographies` | array | Location objects (country, region, port, etc.) |
| `actors` | array | State/corporate/organizational actors |
| `sources` | array | Source objects with tier, type, URL |

### Key Features

- **19 Event Types**: Covers military, sanctions, shipping, infrastructure, regulatory, and more
- **Fog of War Support**: `fog_of_war` boolean + `contradictions` array for contested facts
- **Market Relevance**: `market_relevance_score` and `escalation_score` (0-1 normalized)
- **Extensible Geography**: 12 location types including chokepoints, canals, sea routes

### Relationship to SKILL.md

The Event Object is the **input contract** for the SKILL.md analysis engine. When SKILL.md processes an event, it expects data in this structure.

**Future Extensions** (planned for v6):
- Satellite imagery metadata
- Social media signal integration
- Real-time commodity price snapshots

---

## Layer 2: Watchlist Item (`watchlist-item.json`)

### Purpose
**Solves the "actionable thesis" problem.**

Captures the strongest methodological elements:
- Physical node mapping
- Trigger signals
- Invalidation conditions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `watchlist_id` | string | Unique ID (pattern: `wl-YYYY-NNNN`) |
| `event_id` | string | Reference to parent event |
| `asset_name` | string | Human-readable name |
| `asset_type` | enum | stock, etf, index, commodity, currency, bond, sector, basket, other |
| `market` | enum | US, CN, HK, EU, JP, KR, TW, IN, GLOBAL, OTHER |
| `direction_bias` | enum | bullish, bearish, two_way, monitor_only |
| `thesis` | string | Investment rationale (20-3000 chars) |
| `physical_mapping_node` | object | Node name, type, and mapping logic |
| `trigger_signal` | array | Observable conditions confirming thesis |
| `invalidation_condition` | array | Conditions breaking the thesis |
| `confidence_level` | enum | low, medium, high |
| `time_horizon` | enum | intraday, days, weeks, months, multi_quarter |
| `status` | enum | active, triggered, invalidated, resolved, archived |

### Key Features

- **Physical Node Mapping**: 10 node types (shipping_lane, refinery, substitution_path, etc.)
- **Array-Based Triggers**: Multiple trigger signals per watchlist item
- **Lifecycle Management**: Full status workflow from active → archived
- **Market Coverage**: 10 regions including Korea, Taiwan, India, Global

### Relationship to SKILL.md

Watchlist Items are the **output unit** of SKILL.md's "Watchlist Engine" layer. Each item directly implements:
- The physical bottleneck logic
- Mandatory invalidation conditions
- Trigger signal requirements

**Future Extensions**:
- Position sizing recommendations
- Correlation matrices between watchlist items
- Historical performance tracking

---

## Layer 3: Analysis Output (`analysis-output.json`)

### Purpose
**Solves the "system output contract" problem.**

Packages everything into a unified intelligence container:
- Event + confirmed facts
- Market interpretation
- Scenario analysis
- Watchlist
- Risk flags

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `analysis_id` | string | Unique ID (pattern: `analysis-YYYY-NNNN`) |
| `generated_at` | string (date-time) | Generation timestamp |
| `language` | enum | zh-CN, en, bilingual |
| `mode` | enum | link_mode, discovery_mode |
| `event` | object | Full Event Object |
| `confirmed_facts` | array | Array of fact objects |
| `market_interpretation` | array | Array of interpretation objects |
| `scenario_analysis` | array | Array of scenario objects |
| `watchlist` | array | Array of Watchlist Items |
| `risk_flags` | array | System concern flags |

### Key Features

- **Dual Mode Support**: link_mode (user input) vs discovery_mode (automated)
- **8 Risk Flags**: fog_of_war, single_source_risk, contradictory_reporting, etc.
- **Propagation Chain**: Event-to-market consequence mapping
- **Monitoring Points**: What to watch next

### Subschema Definitions ($defs)

| Definition | Purpose |
|------------|---------|
| `fact` | Confirmed fact with confidence and source IDs |
| `interpretation` | Market thesis with domain classification |
| `scenario` | A/B/C scenario with probability and signposts |
| `propagationStep` | Event-to-market propagation chain node |
| `monitoringPoint` | Next monitoring indicator with priority |

### Relationship to SKILL.md

Analysis Output is the **complete structured result** of running SKILL.md. It maps 1:1 to SKILL.md's output sections:

| SKILL.md Section | Schema Field |
|------------------|--------------|
| Event Snapshot | `event` + executive_summary |
| Confirmed Facts | `confirmed_facts` array |
| Market Interpretation | `market_interpretation` array |
| Scenario Analysis | `scenario_analysis` array |
| Watchlist | `watchlist` array |
| Risk Warning | `risk_flags` + source_notes |

**Future Extensions**:
- Machine-readable JSON-LD for knowledge graphs
- Versioned schema migration support
- Multi-language output bundles

---

## Schema Versioning

| Schema | Current Version | Status |
|--------|-----------------|--------|
| event-object.json | 2020-12 | Stable |
| watchlist-item.json | 2020-12 | Stable |
| analysis-output.json | 2020-12 | Stable |

### Version Compatibility

- All schemas use **JSON Schema Draft 2020-12**
- Breaking changes will increment major version in `$id`
- Additive changes (new optional fields) are backward compatible

### Validation

Use any JSON Schema validator:

```bash
# Example with ajv-cli
ajv validate -s event-object.json -d sample-event.json
```

---

## Integration with SKILL.md

These schemas are the **machine-readable contract** that complements SKILL.md's human-readable instructions:

- **SKILL.md** tells the model *what to do*
- **Schemas** define *what the output should look like*

Together they enable:
- Consistent structured outputs
- API integrations
- Multi-agent workflows
- Historical analysis and backtesting

---

## Contributing

When proposing schema changes:

1. Maintain backward compatibility when possible
2. Document new fields in this README
3. Update example files
4. Version major breaking changes

---

## License

See repository LICENSE.md. These schemas are provided under the same non-commercial terms as the Geo Market Watch project.
