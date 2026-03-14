# Geo Market Watch 🌍📈

> **Structured geopolitical intelligence for market observation**

[![Schema Validation](https://github.com/foreverpupu/geo-market-watch/actions/workflows/schema-validation.yml/badge.svg)](https://github.com/foreverpupu/geo-market-watch/actions/workflows/schema-validation.yml)
[![License](https://img.shields.io/badge/license-Non--Commercial-blue.svg)](LICENSE.md)

---

## What is Geo Market Watch?

Geo Market Watch is an **LLM-native intelligence framework** that transforms
geopolitical events into structured market observation signals.

Instead of producing narrative commentary, the system generates:

- **Confirmed facts** with source attribution
- **Market interpretation** with propagation logic
- **Scenario analysis** with escalation triggers
- **Structured watchlists** with observable signals and invalidation conditions

---

## Why this approach?

Most geopolitical analysis suffers from:

| Problem | Geo Market Watch Solution |
|---------|---------------------------|
| Mixed facts and speculation | Explicit **fact / interpretation / scenario** separation |
| Vague market calls | **Physical node mapping** to actual infrastructure |
| No exit discipline | **Mandatory invalidation conditions** for every position |
| Inconsistent outputs | **JSON Schema contracts** for machine-readable structure |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT LAYER                                                │
│  News Links / Feeds / Government Announcements             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SCOUT MODE (Discovery)                                     │
│  • Rapid scanning and escalation decisions                  │
│  • Source tier assessment                                   │
│  • Fog-of-War detection                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  ANALYSIS ENGINE (SKILL.md)                                 │
│  • Confirmed facts extraction                               │
│  • Market interpretation                                    │
│  • Scenario analysis (A/B/C framework)                      │
│  • Propagation chain mapping                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  MARKET MAPPING FRAMEWORK                                   │
│  • Physical bottleneck identification                       │
│  • Asset-to-node exposure mapping                           │
│  • Trigger signal definition                                │
│  • Invalidation condition specification                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  STRUCTURED OUTPUT                                          │
│  • JSON Schema-compliant analysis                           │
│  • Machine-readable watchlists                              │
│  • Observable monitoring points                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/foreverpupu/geo-market-watch.git
cd geo-market-watch
```

### 2. Install validation dependencies

```bash
pip install -r tests/schema_validation/requirements.txt
```

### 3. Run schema validation

```bash
python tests/schema_validation/validate_examples.py
```

Expected output:

```
Geo Market Watch Schema Validation
========================================

Validating: examples/schema-examples/event-object.sample.json
Against:    schemas/event-object.json
[PASS]

Validating: examples/schema-examples/watchlist-item.sample.json
Against:    schemas/watchlist-item.json
[PASS]

Validating: examples/schema-examples/analysis-output.sample.json
Against:    schemas/analysis-output.json
[PASS]

========================================
Passed: 3/3
Failed: 0/3
```

---

## Example Analysis

### Input

News link about Red Sea shipping disruption.

### Output Structure

```json
{
  "analysis_id": "analysis-2026-0001",
  "event": {
    "event_type": "shipping_disruption",
    "fog_of_war": true,
    "market_relevance_score": 0.84
  },
  "confirmed_facts": [
    {
      "statement": "Commercial shipping risk in the Red Sea has risen",
      "confidence_level": "high"
    }
  ],
  "scenario_analysis": [
    {
      "scenario_name": "Persistent disruption",
      "probability_band": "medium",
      "market_implication": "Shipping-linked names remain in focus"
    }
  ],
  "watchlist": [
    {
      "ticker": "MAERSK-B.CO",
      "direction_bias": "two_way",
      "trigger_signal": [...],
      "invalidation_condition": [...]
    }
  ],
  "propagation_chain": [
    {"step": 1, "from": "Red Sea incidents", "to": "Transit confidence", "relationship": "disrupts"},
    {"step": 2, "from": "Transit confidence", "to": "Longer routes", "relationship": "reroutes"},
    {"step": 3, "from": "Longer routes", "to": "Freight costs", "relationship": "raises_cost"}
  ]
}
```

See full example: [`examples/schema-examples/analysis-output.sample.json`](examples/schema-examples/analysis-output.sample.json)

---

## Core Methodology

The Geo Market Watch methodology is based on several analytical principles:

### Event-Driven Analysis

The system centers analysis around **events**, not articles.

---

### Fact vs Interpretation Separation

Outputs explicitly separate:
- **confirmed facts**
- **interpretation**
- **scenarios**

---

### Propagation Mapping

Geopolitical shocks are translated into economic propagation chains.

**Example:**

```
Red Sea disruption
        ↓
Longer shipping routes
        ↓
Higher freight costs
        ↓
Logistics equity exposure
```

---

### Trigger-Based Monitoring

Each watchlist item must include:
- **observable trigger signals**
- **explicit invalidation conditions**

This prevents vague analysis and encourages disciplined monitoring.

---

## Validation

The repository includes schema validation tooling.

**Validation script:**

```
tests/schema_validation/validate_examples.py
```

**Validation checks:**
- schema correctness
- example JSON compatibility
- cross-schema references

CI automatically runs validation on every pull request.

---

## Contributing

Contributions are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

**Typical contributions include:**
- documentation improvements
- schema improvements
- example scenarios
- tooling enhancements

---

## Roadmap

See [docs/roadmap-v6.md](docs/roadmap-v6.md)

**Future directions include:**
- multi-agent intelligence pipeline
- propagation graph modeling
- event memory and review
- signal quality evaluation
- automated monitoring integration

---

## License

This repository is released under a **Non-Commercial License**.

**Permitted:**
- personal research use
- non-commercial modification

**Not permitted:**
- commercial redistribution
- commercial integration without permission

See [LICENSE.md](LICENSE.md) for full details.

---

## Acknowledgment

Geo Market Watch is an experimental framework exploring how LLMs can support structured geopolitical intelligence.

The project aims to bridge the gap between:
- **narrative geopolitical analysis**
- **structured market monitoring systems**
