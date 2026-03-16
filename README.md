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

## System Status & Project Scope

### Current State

Geo Market Watch is a **local-first research framework** with a functional, runnable pipeline. It is not a hosted service or turnkey product.

**Core Capabilities (Implemented):**
| Component | Status | Description |
|-----------|--------|-------------|
| Event Normalization | ✅ Stable | Convert raw inputs to structured event cards |
| Signal Scoring | ✅ Stable | Deterministic 0-10 impact scoring |
| Database Layer | ✅ Stable | SQLite persistence with query interface |
| Exposure Mapping | ✅ Beta | Event → sector → company mapping |
| Analyst Review | ✅ Beta | Human-in-the-loop approval workflow |
| Performance Tracking | ✅ Beta | Paper-trade evaluation |
| Benchmark Suite | ✅ Beta | 5 test cases with deterministic validation |

**Not in Scope (Current):**
| Feature | Reason | Future |
|---------|--------|--------|
| Live RSS/API ingestion | Requires external service integration | v7.0 (extensible) |
| Persistent scheduler | No daemon/background process | User's cron/systemd |
| Hosted API | No cloud infrastructure | Self-hosted option |
| Multi-user backend | Single-user SQLite design | PostgreSQL migration path |

### Design Philosophy

**Local-First:** All data stays on your machine. No external dependencies required for core functionality.

**Explicit Over Implicit:** Every transformation is logged, scored, and reviewable. No black-box algorithms.

**Composable:** Use only the layers you need. Database without agent loop. Scoring without exposure mapping.

**Deterministic:** Same input → same output. Enables testing, benchmarking, and reproducible research.

### Maturity Assessment

| Layer | Maturity | Notes |
|-------|----------|-------|
| Data (v6.0) | Production | Stable schema, tested migrations |
| Agent (v5.5) | Production | Deterministic scoring, reliable triggers |
| Intelligence (v6.2) | Beta | Exposure mappings need domain tuning |
| Research (v6.4) | Beta | Review workflows functional, UI minimal |
| Observability (v6.6) | Beta | Logging complete, automated insights pending |

**Recommendation:** Use for research and prototyping. Production deployment requires additional hardening (monitoring, backup, access control).

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

# 3. Install package
pip install -e .

# 4. Verify installation
gmw-init-db --help
```

**Dependency Notes:**
- **Core package**: Only needs Python standard library + jsonschema + python-dateutil
- **Schema validation**: Additional test dependencies in `tests/schema_validation/requirements.txt`
- **LLM features**: Optional, install `openai` or `anthropic` packages as needed

---

## Quick Start / How to Run

The CLI is the only supported execution model for routine usage.

Install the package:

```bash
pip install -e .
```

Initialize the database:

```bash
gmw-init-db --db data/geo_alpha.db
```

Run the main workflow:

```bash
gmw-agent --input data/intake.json
```

Query results:

```bash
gmw-query --stats
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
gmw-agent --input examples/minimal_event.json --memory data/dedupe-memory.json
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
pytest tests/
# or
gmw-benchmark --input data/intake-sample.json --memory data/dedupe-memory.json
```

**Coverage:** 5 event categories, 20+ test assertions, deterministic validation

### Case Study: Red Sea Shipping Disruption

**Input:** "Major carriers announce rerouting around Africa due to Red Sea security concerns"

**Processing Pipeline:**
```
Raw Event → Normalized (Category: shipping, Region: Middle East)
    ↓ [Scoring Engine]
Scored: 8/10 (High severity, global scope, immediate impact)
    ↓ [Trigger Engine]
Escalated: Full analysis triggered
    ↓ [Exposure Engine]
Sectors: Shipping, Energy, Insurance
    ↓ [Trade Idea Engine]
Output: LNG carrier long thesis, +15% return tracked
```

**Key Results:**

| Metric | Predicted | Actual | Status |
|--------|-----------|--------|--------|
| LNG Rates | +30% | +50% | ✅ Direction correct, magnitude underestimated |
| Flex LNG Return | +15% | +21% | ✅ Within expected range |
| Container Impact | +50% | +30% | ⚠️ Overestimated |
| Timeline | 14 days | 21 days | ⚠️ Extended |

**Analyst Review:**
- ✅ Approved for tracking (High conviction)
- ✅ Entry: $100.00, Exit: $115.00 (+15%)
- 📊 Full postmortem: [docs/operations/postmortem.md](docs/operations/postmortem.md)

**Lessons Applied:**
- Updated shipping disruption sector weights
- Adjusted timeline assumptions for route closures
- Added insurance sector to exposure mapping

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
- [Code Structure](docs/architecture/code-structure.md) — Package structure
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

## Architecture / The Engine

`geo-market-watch` is a **local-first, deterministic, auditable intelligence workflow** for converting geopolitical events into structured market intelligence.

### Core Pipeline

> **Raw Event → Normalization → Scoring → Trigger → Review → Performance Tracking**

This pipeline represents a shift from black-box prediction to **auditable workflow**. Every transformation is logged, scored, and reviewable. LLMs are not autonomous decision-makers in this system; they are tools within a structured process that maintains human oversight at critical decision points.

### Key Design Principles

- **Local-First** — Data, state, and artifacts remain inspectable and under operator control
- **Deterministic** — Core pipeline stages produce reproducible outputs given the same inputs, enabling testing and benchmarking
- **Auditable** — Every judgment is traceable, inspectable, and replayable
- **Human-in-the-Loop** — Analyst review gates critical decisions; no fully automated deployment
- **Composable** — Use only the layers you need. Database without agent loop. Scoring without exposure mapping.

### Typed Model Architecture

Strongly typed dataclass models provide **unified contracts** across the pipeline:

- **Testability**: Typed models enable unit testing without mocking complex dependencies
- **Explainability**: Explicit field names and types make data flow transparent
- **Multi-Agent Protocol**: Typed models serve as the communication protocol for future multi-agent workflows (v7.0)

Example models:
- `RawIntakeItem` → `NormalizedEvent` → `ScoreResult` → `TriggerResult` → `NotificationArtifact`

### v7.0 Preview

The next major version will introduce:
- **Source Confidence** — Evidence quality assessment attached to intake items
- **Fog of War** — Uncertainty state tracking for contested or evolving situations
- **Mandatory Invalidation** — Explicit invalidation workflows with audit trails

These features extend the typed model architecture to support more nuanced intelligence workflows while maintaining the core principles of auditability and human oversight.

**Full architecture:** [docs/architecture/institutional-framework.md](docs/architecture/institutional-framework.md)

---

## Database Layer

Local SQLite database for event storage and analysis:

```bash
# Initialize
gmw-init-db --db data/geo_alpha.db

# Query
gmw-query --db data/geo_alpha.db --list

# Schema: [docs/architecture/database-spec.md](docs/architecture/database-spec.md)
```

---

## CLI Reference

**Core Commands:**

| Command | Purpose | Example |
|---------|---------|---------|
| `gmw-init-db` | Initialize database | `gmw-init-db --db data/geo_alpha.db` |
| `gmw-query` | Query database | `gmw-query --db data/geo_alpha.db --stats` |
| `gmw-agent` | Run agent loop | `gmw-agent --input data/intake.json --memory data/dedupe.json` |
| `gmw-seed-db` | Seed database | `gmw-seed-db --db data/geo_alpha.db --seed data/seed.json` |
| `gmw-benchmark` | Run benchmark | `gmw-benchmark --input data/intake.json --memory data/dedupe.json` |

**Query Options:**
```bash
# List all events
gmw-query --db data/geo_alpha.db --list

# Show statistics
gmw-query --db data/geo_alpha.db --stats

# High-signal events only
gmw-query --db data/geo_alpha.db --high-signal

# Filter by region
gmw-query --db data/geo_alpha.db --region "Middle East"

# Performance data
gmw-query --db data/geo_alpha.db --idea-performance
```

---

## Python API

Import and use programmatically:

```python
from geo_market_watch.agent_loop import run_agent_loop
from geo_market_watch.database import connect_db, get_stats
from geo_market_watch.models import RawIntakeItem

# Run agent loop
summary = run_agent_loop(
    intake_path="data/intake.json",
    dedupe_memory_path="data/dedupe.json",
    output_dir="outputs"
)

# Query database
conn = connect_db("data/geo_alpha.db")
stats = get_stats(conn)
print(f"Total events: {stats['total_events']}")
```

---

## Analyst Review Workflow

Human-in-the-loop for quality control:

```python
# Review pending ideas (Python API)
from geo_market_watch.dashboard_views import get_tracked_ideas
from geo_market_watch.lifecycle_engine import get_active_ideas

# Get ideas for review
ideas = get_active_ideas("data/geo_alpha.db", status="pending_review")

# Approve and track (Python API)
from geo_market_watch.idea_review_engine import approve_idea
from geo_market_watch.performance_engine import start_tracking
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
| Core package | 3.10+ | `pyproject.toml` | `geo_market_watch/` |
| Schema validation | 3.10+ | `tests/schema_validation/requirements.txt` | Test subdirectory |
| Engine tests | 3.10+ | Same as core | N/A |
| LLM features | 3.10+ | Optional: `openai`, `anthropic` | Install as needed |

**Minimal setup for core functionality:**
```bash
pip install -e .
```

**Full setup for development:**
```bash
pip install -e .
pip install -r tests/schema_validation/requirements.txt
```

---

## Local Validation

Before submitting changes, run the same checks as CI:

```bash
# Install package
pip install -e .

# Run tests
pytest tests/ -v

# CLI smoke checks
gmw-init-db --help
gmw-query --help
gmw-agent --help

# Check for forbidden legacy patterns (should return no matches)
grep -r "sys.path.insert" --include="*.py" . | grep -v __pycache__
grep -r "from engine\." --include="*.py" . | grep -v __pycache__
grep -r "^import engine" --include="*.py" . | grep -v __pycache__
grep -r "geo_market_watch\.engine" --include="*.py" . | grep -v __pycache__
```

如果本地运行无输出，即为正常；CI 管道会对这些模式进行严格的硬失败检查。

All checks should pass before submitting a PR.

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
