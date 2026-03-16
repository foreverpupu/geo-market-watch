# Changelog

All notable changes to Geo Market Watch will be documented in this file.
For a deep dive into the AI design philosophy and research logic behind these updates, please refer to our [Design Notes](docs/design-notes.md).

## [v6.5] - 2026-03-16
### Package Refactor Closure

This release completes the engineering closure of the package refactor. No new features were added; this is purely architectural hygiene and consistency work.

#### Package Structure
- **Official Namespace** — All code now uses `geo_market_watch.*` namespace exclusively
- **CLI Entry Points** — 5 official CLI commands added:
  - `gmw-init-db` — Initialize database
  - `gmw-query` — Query database
  - `gmw-agent` — Run agent loop
  - `gmw-seed-db` — Seed database with sample events
  - `gmw-benchmark` — Run performance benchmark
- **Clean Imports** — Removed all `sys.path.insert()` hacks and `from engine.*` imports

#### Legacy Script Deprecation
- All top-level scripts in `scripts/` directory are now deprecated
- Scripts show deprecation warnings and redirect to official CLI
- Legacy wrappers will be removed in a future version

#### Documentation Updates
- Root README.md updated to promote package-based workflow
- CLI usage examples added
- Python API examples added
- Installation instructions updated to use `pip install -e .`

#### Version Unification
- Single version source: `geo_market_watch.__version__`
- CLI and all outputs report consistent version

#### Technical Debt Reduction
- Removed 16 legacy script files with path manipulation
- Consolidated CLI logic into `geo_market_watch/scripts/` package
- All tests pass (37/37)

#### Migration Guide
**Old (deprecated):**
```bash
python scripts/init_database.py --db data/geo_alpha.db
python scripts/query_database.py --db data/geo_alpha.db --list
python scripts/run_agent_loop.py --input data/intake.json
```

**New (official):**
```bash
pip install -e .
gmw-init-db --db data/geo_alpha.db
gmw-query --db data/geo_alpha.db --list
gmw-agent --input data/intake.json --memory data/dedupe.json
```

---

## [v6.4] - 2026-03-15
### Idea Performance Tracking

This release introduces the first **paper-performance tracking layer** for approved trade ideas.

#### New Engine Components
- **Performance Engine** — `engine/performance_engine.py` — Tracks paper trading performance
- **Export Layer** — `engine/export_layer.py` — JSON/CSV export functionality
- **Dashboard Views** — `engine/dashboard_views.py` — Extended with performance views

#### New Scripts
- `scripts/start_idea_tracking.py` — Start tracking with entry price
- `scripts/close_trade_idea.py` — Close tracking and compute returns
- `scripts/update_idea_price_reference.py` — Correct price references
- `scripts/list_tracked_ideas.py` — List tracked ideas with performance
- `scripts/export_dashboard_data.py` — Export performance data

#### New Database Table
- **trade_idea_performance** — Performance tracking records with MUE/MFE metrics

#### New Documentation
- `docs/idea-performance-spec.md` — Performance tracking specification
- `docs/performance-methodology.md` — Calculation methodology
- `docs/idea-outcome-classification.md` — Outcome classification
- `docs/benchmark-v6.4.md` — Validation benchmark

#### New Examples & Data
- `examples/idea-performance.example.json`
- `examples/idea-performance-output.example.md`
- `data/idea-performance-sample.json`

#### Improvements
- Tracks entry and close reference prices for approved ideas
- Calculates virtual return and holding period
- Classifies idea outcomes deterministically
- Extends dashboard exports with performance-aware research views
- Supports benchmark hints and alpha spread calculation
- Includes MUE/MFE risk metrics

#### Notes
This release adds **paper tracking only**.
It does not provide live trading, execution integration, or real portfolio accounting.

---

## [v6.3] - 2026-03-15
### Analyst Review Workflow

This release introduces **analyst review and lifecycle management** for trade ideas.

#### New Engine Components
- **Status Rules Engine** — `engine/status_rules.py` — Validates status transitions
- **Idea Review Engine** — `engine/idea_review_engine.py` — Processes analyst reviews
- **Lifecycle Engine** — `engine/lifecycle_engine.py` — Tracks lifecycle events

#### New Scripts
- `scripts/review_trade_ideas.py` — Submit analyst reviews
- `scripts/approve_trade_idea.py` — Quick approval
- `scripts/invalidate_trade_idea.py` — Invalidate ideas when conditions change
- `scripts/list_active_ideas.py` — List approved active ideas

#### New Database Tables
- **trade_ideas** — Trade idea records with analyst_status
- **idea_reviews** — Review decisions and notes
- **idea_lifecycle** — Lifecycle event log

#### New Documentation
- `docs/analyst-workflow.md` — Complete workflow guide
- `docs/idea-lifecycle-spec.md` — Lifecycle state specification
- `docs/analyst-review-guidelines.md` — Review quality guidelines
- `docs/benchmark-v6.3.md` — Validation benchmark

#### New Examples
- `examples/analyst-review.example.json` — Review record example
- `examples/idea-lifecycle.example.md` — Lifecycle timeline example

#### Improvements
- Human review layer for generated trade ideas
- Required notes for reject/needs_revision decisions (enforced at engine level)
- Dashboard prioritization (approved + high conviction first, then by created_at)
- Complete audit trail via lifecycle events
- Status transition validation prevents invalid moves

---

## [v6.4] - 2026-03-15
### Performance Tracking

This release adds **paper trading performance tracking** for approved trade ideas.

#### New Engine Components
- **Performance Engine** — `engine/performance_engine.py` — Tracks paper trading performance
- **Export Layer** — `engine/export_layer.py` — JSON/CSV export functionality

#### New Scripts
- `scripts/start_idea_tracking.py` — Start tracking with entry price
- `scripts/close_trade_idea.py` — Close tracking and compute returns
- `scripts/update_idea_price_reference.py` — Correct price references
- `scripts/list_tracked_ideas.py` — List tracked ideas with performance
- `scripts/export_dashboard_data.py` — Export performance data

#### New Database Table
- **trade_idea_performance** — Performance tracking records

#### New Documentation
- `docs/idea-performance-spec.md` — Performance tracking specification
- `docs/performance-methodology.md` — Calculation methodology
- `docs/idea-outcome-classification.md` — Outcome classification
- `docs/benchmark-v6.4.md` — Validation benchmark

#### New Examples
- `examples/idea-performance.example.json` — Performance record example
- `examples/idea-performance-output.example.md` — Output example
- `data/idea-performance-sample.json` — Sample data for testing

#### Features
- Entry/close price tracking with ISO timestamps
- Automatic return calculation (long and short)
- Outcome classification (strong_positive/positive/flat/negative/strong_negative)
- Holding period calculation
- Benchmark return and alpha spread support
- Price reference corrections with audit trail
- Approval-gated tracking (only approved ideas)
- Dashboard views for tracked and closed ideas
- JSON/CSV export with sanitized fields

#### Validation
- Entry/close prices must be positive
- Close time must not be earlier than entry time
- Only approved ideas can be tracked
- Notes required for price corrections

#### Query Script Updates
- `--idea-performance` — Show idea performance data
- `--performance-summary` — Show performance statistics
- `--tracked-ideas` — Show currently tracked ideas
- `--closed-ideas` — Show closed ideas with performance

#### Notes
This release adds quantitative performance measurement to the research workflow.

**Important:** This is paper (hypothetical) tracking only — no actual trades are executed.

---

## [v6.3] - 2026-03-15
### Analyst Review Workflow

This release introduces **analyst review and lifecycle management** for trade ideas.

#### New Engine Components
- **Status Rules Engine** — `engine/status_rules.py` — Validates status transitions
- **Idea Review Engine** — `engine/idea_review_engine.py` — Processes analyst reviews
- **Lifecycle Engine** — `engine/lifecycle_engine.py` — Tracks lifecycle events

#### New Scripts
- `scripts/review_trade_ideas.py` — Submit analyst reviews
- `scripts/approve_trade_idea.py` — Quick approval
- `scripts/invalidate_trade_idea.py` — Invalidate ideas when conditions change
- `scripts/list_active_ideas.py` — List approved active ideas

#### New Database Tables
- **trade_ideas** — Trade idea records with analyst_status
- **idea_reviews** — Review decisions and notes
- **idea_lifecycle** — Lifecycle event log

#### New Documentation
- `docs/analyst-workflow.md` — Complete workflow guide
- `docs/idea-lifecycle-spec.md` — Lifecycle state specification
- `docs/analyst-review-guidelines.md` — Review quality guidelines
- `docs/benchmark-v6.3.md` — Validation benchmark

#### New Examples
- `examples/analyst-review.example.json` — Review record example
- `examples/idea-lifecycle.example.md` — Lifecycle timeline example

#### Improvements
- Human review layer for generated trade ideas
- Required notes for reject/needs_revision decisions (enforced at engine level)
- Dashboard prioritization (approved + high conviction first, then by created_at)
- Complete audit trail via lifecycle events
- Status transition validation prevents invalid moves

#### Notes
This release upgrades Geo Market Watch from an **idea generation engine** into a **structured research workflow system**.

It does not yet include:
- ~~Performance tracking~~ (added in v6.4)
- Automated invalidation triggers
- Multi-analyst consensus
- Execution system integration

---

## [v6.0] - 2026-03-15
### Geo Alpha Database

This release introduces the first **minimal event database layer** for Geo Market Watch.

#### New Database Components
- **SQLite database** — Local-first, zero infrastructure storage
- **6 tables** — events, sources, indicators, flags, notifications, watchlist
- **CRUD operations** — Full create, read, update, delete support
- **Query engine** — Search by region, category, band, date
- **Statistics** — Event counts, distributions, metrics

#### New Engine Files
- `engine/database_models.py` — Schema definitions
- `engine/database.py` — Database operations
- `engine/artifact_ingest.py` — Ingest v5.5 outputs into DB

#### New Scripts
- `scripts/init_database.py` — Initialize database
- `scripts/seed_database.py` — Seed with sample events
- `scripts/query_database.py` — Query and display events
- `scripts/ingest_artifacts.py` — Ingest agent loop outputs

#### New Data
- `data/db-seed-events.json` — 5 sample events for testing
- `data/geo_alpha.db` — SQLite database file

#### New Documentation
- `docs/geo-alpha-database-spec.md`
- `docs/database-query-examples.md`
- `docs/benchmark-v6.md`

#### Improvements
- Persistent event storage
- Historical event tracking
- Searchable event archive
- Foundation for future dashboard

#### Notes
This release is **intentionally minimal**.
It does not include a production database service, web dashboard, or hosted API.

---

## [v5.5] - 2026-03-15
### Minimal Agent Loop

This release introduces the **first end-to-end runnable agent loop** in Geo Market Watch.

#### New Engine Components
- **Intake normalizer** — converts raw items to Event Card format
- **Deduplication memory** — JSON-based duplicate filtering
- **Notifier** — generates monitor/handoff notifications
- **Agent loop orchestrator** — runs complete 4-node pipeline

#### New Scripts
- `scripts/run_agent_loop.py` — CLI entry point

#### New Data
- `data/intake-sample.json` — 8 sample events with duplicates

#### New Documentation
- `docs/minimal-agent-architecture.md`
- `docs/notification-spec.md`
- `docs/benchmark-v5.5.md`

#### Improvements
- Connects intake, dedupe, scoring, trigger, and notification into one local workflow
- Enables repeatable local runs without external services
- Establishes the first minimal agent handoff path into Full Analysis Mode

#### Notes
This release is **intentionally narrow**.
It does not yet include live ingestion, fuzzy dedupe, persistence, or hosted automation.

---

## [v5.4] - 2026-03-15
### Automated Signal Scoring

This release introduces the **first executable layer** of Geo Market Watch.

#### New Engine Components
- **Minimal scoring engine** — Converts event indicators into deterministic signal scores (0-10)
- **Minimal trigger engine** — Decides whether to escalate to Full Analysis Mode
- **Benchmark dataset** — 7 real-world geopolitical events for validation
- **Benchmark runner** — Automated test and validation script

#### New Documentation
- `docs/scoring-engine-spec.md`
- `docs/benchmark-v5.4.md`
- `engine/README.md`

#### Data
- `data/benchmark-events.json`

#### Scripts
- `scripts/run_benchmark.py`

#### Improvements
- Converts documented signal scoring rules into executable logic
- Converts trigger conditions into deterministic escalation rules
- Upgrades benchmark from descriptive review to reproducible validation

#### Notes
This release is the first step from a **research framework** toward an **executable geopolitical monitoring system**.

---

## [v5.3] - 2026-03-15
### Scout Mode Edition

Major framework expansion introducing early-signal detection and structured event tracking.

#### New Components
- **Scout Mode workflow** — Lightweight early detection system
- **Event Card schema** — Standardized event summary format
- **Signal scoring framework** — 5-dimension numerical scoring (0-10)
- **Full analysis trigger rules** — Clear escalation criteria
- **Event database design** — SQL/document store schema
- **Benchmark comparison framework** — v3 vs v5 quality validation

#### Documentation
Added:
- `docs/event-card-schema.md`
- `docs/signal-scoring.md`
- `docs/full-analysis-trigger.md`
- `docs/event-database-design.md`
- `docs/benchmark-v5.md`

#### Prompts
Added:
- `prompts/scout-mode.md`

#### Improvements
- Clarified monitoring workflow
- Structured early event detection
- Prepared system for automated scoring

> **Note:** This release transitions the project from a **prompt-only framework** to a **structured geopolitical monitoring system**.

## [v5.2.1] - 2026-03-15
### Added
- **Documentation**: Added `scheduled-monitoring.md` (Scout Mode) to provide guidance on pairing the skill with automated scheduling tasks.
### Fixed
- **Encoding Compatibility**: Fixed potential UTF-8 encoding issues when the main prompt calls external templates by enforcing bilingual tags (e.g., `[已确认事实 / Confirmed Facts]`).
- **Workflow Logic**: Fixed a workflow breakpoint at Step 10 to ensure the model strictly outputs all 9 required modules.
> *Why it matters: Improves packaging reliability, output completeness, and compatibility with scheduled monitoring workflows.*

## [v5.2] - 2026-03-14
### Added
- **Fog of War Rule**: Explicitly integrated contested-fact handling into the `[已确认事实 / Confirmed Facts]` module.
### Changed
- **Data Fallback**: Specified concrete public proxies (e.g., relative strength of shipping equities, sector ETFs) when high-frequency logistics or insurance data is paywalled.
> *Why it matters: Prevents LLMs from hallucinating false certainties or fabricating data during the chaotic first 48 hours of a geopolitical event.*

## [v5.1] - 2026-03-10
### Added
- **Source Authentication & Anti-Hype Filter**: Established strict Tier 1 (facts) and Tier 2 (analysis) isolation.
- **Source-Level Tags**: Mandated visual source tags (e.g., `[官方]`, `[通讯社]`) in the output.
### Changed
- **Rhetoric Isolation**: Explicitly instructed the model to separate official political rhetoric/threats from actual market facts.
> *Why it matters: Protects the output analysis from being skewed by emotional media reporting, viral tone, or political posturing.*

## [v4.0] - 2026-02-20
### Added
- **Node-Specific Targeting**: Prioritized mapping events to specific physical bottlenecks (e.g., VLCC terminals, specific pipelines) rather than broad industry ETFs.
- **Physical Bottleneck Logic**: Expanded the requirement to translate political events into quantifiable market exposure (e.g., export volumes, supply share).
> *Why it matters: Moves the workflow closer to physical-system analysis rather than broad thematic storytelling.*

## [v3.0] - 2026-01-15
### Added
- **Mandatory Invalidation**: Required every ticker in the watchlist to include a concrete invalidation condition.
- **Trigger Signals**: Standardized the inclusion of observable, event-linked trigger signals.
- **Three-Market Standardization**: Formalized the asymmetric watchlist construction across US, A-shares, and HK markets.
> *Why it matters: Enforces strict trading discipline, ensuring users know exactly what conditions invalidate the current base case so they are not trapped by outdated narratives.*
