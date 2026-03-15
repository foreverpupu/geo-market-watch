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

## Quick Start (10-minute run)

```bash
# 1. Clone and setup
git clone https://github.com/foreverpupu/geo-market-watch.git
cd geo-market-watch
pip install -r requirements.txt

# 2. Initialize database
python scripts/init_database.py --db data/geo_alpha.db

# 3. Run minimal example
python scripts/run_agent_loop.py \
  --input examples/minimal_event.json \
  --output outputs/

# 4. View results
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
