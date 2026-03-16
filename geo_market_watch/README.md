# Geo Market Watch Package

The `geo_market_watch` package contains the core logic for processing geopolitical events into structured intelligence artifacts.

It powers the event → analysis → monitoring pipeline used by Geo Market Watch.

---

## Responsibilities

The package currently implements:

- **Event normalization** — Convert raw inputs to structured event cards
- **Event deduplication** — Detect and filter duplicate events
- **Event scoring** — Calculate impact scores (0-10)
- **Escalation triggers** — Decide monitor vs full analysis
- **Notification generation** — Create analyst handoff artifacts
- **Database persistence** — SQLite storage for events and analysis
- **Lifecycle management** — Track idea states from creation to closure
- **Performance tracking** — Paper-trade evaluation

---

## What the Package Does NOT Do

The package intentionally does not include:

- External news ingestion (RSS/API feeds)
- Continuous scheduling (cron/background jobs)
- External data pipelines (market data feeds)
- UI dashboards (web interfaces)
- Multi-user coordination

These responsibilities are handled by external automation, CLI scripts, or orchestration layers.

---

## Module Overview

| Module | Responsibility | Key Functions |
|--------|----------------|---------------|
| `intake_normalizer.py` | Event normalization | `normalize_event()`, `validate_event()` |
| `dedupe_memory.py` | Deduplication | `check_duplicate()`, `add_to_memory()` |
| `scoring_engine.py` | Impact scoring | `compute_score()`, `get_score_band()` |
| `trigger_engine.py` | Escalation logic | `should_escalate()`, `get_trigger_reason()` |
| `database.py` | Persistence | `connect_db()`, `execute_query()` |
| `database_models.py` | Schema definitions | Table schemas, validation |
| `lifecycle_engine.py` | State management | `record_event()`, `invalidate_idea()` |
| `performance_engine.py` | Paper tracking | `start_tracking()`, `close_tracking()` |
| `idea_review_engine.py` | Analyst workflow | `submit_review()`, `get_pending_reviews()` |
| `exposure_engine.py` | Market mapping | `map_to_sectors()`, `map_to_companies()` |
| `agent_loop.py` | Orchestration | `run_agent_loop()`, `process_event()` |
| `notifier.py` | Output generation | `generate_notification()`, `format_output()` |
| `scripts/` | CLI entry points | `gmw-init-db`, `gmw-query`, `gmw-agent`, etc. |

---

## Design Philosophy

The package focuses on **deterministic processing and structured outputs**, allowing higher-level automation or analyst workflows to build on top.

### Key Principles

1. **Pure Functions** — Minimize side effects, maximize testability
2. **Explicit Dependencies** — Pass dependencies as parameters
3. **Structured Data** — Return objects, not print statements
4. **Error Handling** — Raise exceptions, don't exit
5. **Local-First** — SQLite, no external service dependencies

---

## CLI Usage

After installing the package (`pip install -e .`), use the official CLI commands:

```bash
# Initialize database
gmw-init-db --db data/geo_alpha.db

# Query database
gmw-query --db data/geo_alpha.db --list
gmw-query --db data/geo_alpha.db --stats
gmw-query --db data/geo_alpha.db --high-signal

# Run agent loop
gmw-agent --input data/intake.json --memory data/dedupe.json --output outputs/

# Seed database
gmw-seed-db --db data/geo_alpha.db --seed data/seed-events.json

# Run benchmark
gmw-benchmark --input data/intake.json --memory data/dedupe.json
```

---

## Python API Usage

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

### Processing a Single Event

```python
from geo_market_watch.intake_normalizer import normalize_event
from geo_market_watch.scoring_engine import compute_score
from geo_market_watch.trigger_engine import should_escalate

# Process an event
raw_event = {"headline": "Red Sea shipping disruption..."}
event = normalize_event(raw_event)
score = compute_score(event)
escalate = should_escalate(score)

if escalate:
    # Generate full analysis
    pass
```

---

## Testing

Package modules are designed for unit testing:

```python
# test_scoring.py
from geo_market_watch.scoring_engine import compute_score

def test_shipping_disruption_score():
    event = {"category": "shipping", "severity": "high"}
    score = compute_score(event)
    assert 7 <= score <= 9  # Should be high
```

Run all tests:
```bash
pytest tests/
```

---

## Version

```python
import geo_market_watch
print(geo_market_watch.__version__)  # "0.1.0"
```

---

See [docs/architecture/code-structure.md](../docs/architecture/code-structure.md) for full architecture details.
