<p align="center">
  <h1 align="center">Geo Market Watch 🌍📈</h1>
</p>

<p align="center">
  <strong>Structured framework for turning geopolitical events into market-relevant intelligence, watchlists, and analyst workflows.</strong>
</p>

---

## What This Project Does

Geo Market Watch converts complex geopolitical developments into **structured market intelligence** through a deterministic pipeline:

```
Raw Event → Normalization → Scoring → Escalation → Analysis → Review → Tracking
```

**Key capabilities:**
- **Event Normalization** — Convert news into structured event cards
- **Signal Scoring** — Deterministic 0-10 scoring for escalation decisions  
- **Exposure Mapping** — Map events to sectors, companies, supply chains
- **Trade Ideas** — Generate thesis-driven ideas with invalidation conditions
- **Analyst Review** — Human-in-the-loop approval and lifecycle tracking
- **Performance Tracking** — Paper-trade evaluation of approved ideas

---

## Who This Is For

- **Macro Researchers** — Systematic geopolitical event tracking
- **Quant Analysts** — Event-driven signal systems
- **Asset Managers** — Research workflow for idea generation
- **Developers** — Building custom intelligence tools

**Not for:** Traders seeking one-click execution, teams needing managed cloud infrastructure, or users requiring real-time streaming data.

---

## What This Repository Is / Is Not

| ✅ This Is | ❌ This Is Not |
|-----------|----------------|
| Research framework with runnable local pipeline | Hosted production service |
| Local SQLite-based event database | Real-time ingestion backend |
| CLI tools for analysis workflow | Managed API with SLA |
| Foundation for building intelligence systems | Turnkey investment product |

---

## Repository Status

Geo Market Watch is currently a **research framework with a runnable local pipeline**, not a hosted production system.

**It includes:**
- A structured event → analysis → monitoring workflow
- A local agent loop for event processing
- A lightweight SQLite-based Geo Alpha database
- An analyst review and lifecycle tracking layer
- Paper performance tracking for idea evaluation

**It does NOT currently include:**
- Live RSS/API ingestion pipelines
- A persistent background scheduler
- Hosted APIs or dashboards
- Multi-user orchestration services

The project is designed as a **foundation for building geopolitical event intelligence systems**, not a turnkey investment product.

---

## Environment Setup

**Prerequisites:** Python 3.10+

```bash
# 1. Clone repository
git clone https://github.com/foreverpupu/geo-market-watch.git
cd geo-market-watch

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python --version  # Should show 3.10+
python scripts/init_database.py --help
```

**Dependency Notes:**
- **Core scripts** (database, query, agent loop): Only need Python standard library + click
- **Schema validation**: Additional test dependencies in `tests/schema_validation/requirements.txt`
- **LLM features**: Optional, install `openai` or `anthropic` packages as needed

---

## Quick Start (10-minute run)

```bash
# 1. Initialize database
python scripts/init_database.py --db data/geo_alpha.db

# 2. Seed with sample data
python scripts/seed_database.py \
  --db data/geo_alpha.db \
  --seed data/db-seed-events.json

# 3. Query to verify
python scripts/query_database.py --db data/geo_alpha.db --list

# 4. Run minimal example
python scripts/run_agent_loop.py \
  --input examples/minimal_event.json \
  --output outputs/

# 5. View results
cat outputs/notification.md
```

---

## Minimal End-to-End Example

**Input:** `examples/minimal_event.json`

```json
{
  "headline": "Red Sea shipping disruption escalates",
  "region": "Middle East",
  "category": "shipping"
}
```

**Run:**
```bash
python scripts/run_agent_loop.py --input examples/minimal_event.json
```

**Outputs generated:**
```
outputs/
├── normalized_event.json     # Structured event card
├── event_score.json          # Score: 8/10
├── escalation_decision.json  # Full analysis triggered
└── analyst_handoff.md        # Trade ideas and watchlist
```

---

## Benchmark & Case Study

### Evaluation Framework

Geo Market Watch includes a deterministic benchmark suite for validating analysis quality:

| Case | Category | Input → Output | Key Test |
|------|----------|----------------|----------|
| [Case 001](benchmarks/cases/case_001_shipping_disruption/) | Shipping Disruption | News headline → Trade ideas | Score: 8/10, Escalate: Yes |
| [Case 002](benchmarks/cases/case_002_sanctions/) | Sanctions | Export controls → Sector exposure | Score: 7/10, Sectors: Tech |
| [Case 003](benchmarks/cases/case_003_commodity_shock/) | Commodity Shock | Oil outage → Price impact | Score: 9/10, Return: +15% |
| [Case 004](benchmarks/cases/case_004_military_escalation/) | Fog of War | Unverified reports → Monitor | Score: 5/10, Escalate: No |
| [Case 005](benchmarks/cases/case_005_election_shock/) | Election Shock | Policy shift → Nationalization risk | Score: 8/10, Short: State-owned |

**Run benchmarks:**
```bash
python tests/engine/test_engine_core.py
```

**Coverage:** 5 event categories, 20+ test assertions, deterministic validation

### Case Study: Red Sea Shipping Disruption

**Input:** "Major carriers announce rerouting around Africa due to Red Sea security concerns"

**Processing:**
```
Raw Event → Normalized (Category: shipping, Region: Middle East)
    ↓
Scored: 8/10 (High severity, global scope, immediate impact)
    ↓
Escalated: Full analysis triggered
    ↓
Output: LNG carrier long thesis, +15% return tracked
```

**Result:**
- ✅ Correctly identified supply constraint thesis
- ✅ Recommended LNG carriers (Flex LNG +21% actual)
- ⚠️ Underestimated container impact (+30% vs +50% expected)
- 📊 Postmortem: [docs/operations/postmortem.md](docs/operations/postmortem.md)

---

## Documentation Map

**Product Overview**
- [Positioning](docs/product/positioning.md) — What this is and isn't
- [Adoption Paths](docs/product/adoption-paths.md) — Choose your integration path
- [Commercial Use](docs/product/commercial-use.md) — License and usage guidelines
- [v6.x Roadmap](docs/product/roadmap-v6.md) — Continuous evolution plan

**System Architecture**
- [Overview](docs/architecture/system-overview.md) — Four-layer framework
- [Institutional Framework](docs/architecture/institutional-framework.md) — Enterprise architecture
- [Code Structure](docs/architecture/code-structure.md) — Engine vs scripts
- [State Machine](docs/architecture/state-machine.md) — Event lifecycle

**Evaluation & Benchmarks**
- [Benchmark Design](docs/evaluation/benchmark-design.md) — Quality evaluation
- [Benchmark Cases](benchmarks/README.md) — 5 test cases
- [Pipeline Tests](tests/pipeline/) — Regression testing

**Operational Workflows**
- [Quick Start](docs/operations/quickstart.md) — Detailed walkthrough
- [Analyst Workflow](docs/operations/analyst-workflow.md) — Review process
- [Observability](docs/operations/observability.md) — Logging and metrics
- [Postmortem](docs/operations/postmortem.md) — Review and improve

**Research Methodology**
- [Methodology](docs/research/methodology.md) — Research approach
- [Source Tiering](docs/research/source-tiering.md) — Information hierarchy
- [Skill Evolution](docs/research/skill-evolution-notes.md) — Development journey

---

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│      GEO MARKET WATCH ARCHITECTURE           │
└──────────────────────────────────────────────┘

DATA LAYER
  Raw Signals → Event Cards → Database → Exports

AGENT LAYER
  News Intake → Dedupe → Scoring → Trigger → Output

INTELLIGENCE LAYER
  Event Understanding → Sector Exposure → Trade Ideas

RESEARCH LAYER
  Analyst Review → Approval Workflow → Performance Tracking
```

**Full architecture:** [docs/architecture/institutional-framework.md](docs/architecture/institutional-framework.md)

---

## Database Layer

Local SQLite database for event storage and analysis:

```bash
# Initialize
python scripts/init_database.py --db data/geo_alpha.db

# Query
python scripts/query_database.py --db data/geo_alpha.db --list

# Schema: [docs/architecture/database-spec.md](docs/architecture/database-spec.md)
```

---

## Analyst Review Workflow

Human-in-the-loop for quality control:

```bash
# Review pending ideas
python scripts/list_active_ideas.py --db data/geo_alpha.db --status pending_review

# Approve idea
python scripts/approve_trade_idea.py --db data/geo_alpha.db --idea-id TRADE_ID

# Track performance
python scripts/start_idea_tracking.py --db data/geo_alpha.db --idea-id TRADE_ID
```

**Full workflow:** [docs/operations/analyst-workflow.md](docs/operations/analyst-workflow.md)

---

## Roadmap

**Current: v6.6 — Observability & Learning Loop**

| Version | Theme | Status |
|---------|-------|--------|
| v6.1 | Onboarding | ✅ Complete |
| v6.2 | Positioning | ✅ Complete |
| v6.3 | Docs Architecture | ✅ Complete |
| v6.4 | Evaluation Framework | ✅ Complete |
| v6.5 | Engine Refactor | ✅ Complete |
| v6.6 | Observability Loop | ✅ Complete |

**Next: v7.0 — Multi-Agent Intelligence**

See [v6.x Roadmap](docs/product/roadmap-v6.md) for details.

---

## Environment Reference

| Component | Python Version | Dependencies | Location |
|-----------|---------------|--------------|----------|
| Core scripts | 3.10+ | `requirements.txt` | Root directory |
| Schema validation | 3.10+ | `tests/schema_validation/requirements.txt` | Test subdirectory |
| Engine tests | 3.10+ | Same as core | N/A |
| LLM features | 3.10+ | Optional: `openai`, `anthropic` | Install as needed |

**Minimal setup for core functionality:**
```bash
pip install -r requirements.txt
```

**Full setup for development:**
```bash
pip install -r requirements.txt
pip install -r tests/schema_validation/requirements.txt
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Contribution guidelines
- Code style
- Testing requirements

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built for researchers who need structured geopolitical intelligence.</strong>
</p>
