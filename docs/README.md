# Geo Market Watch Documentation

**Navigate the documentation by layer.**

---

## 📋 Product Layer

Understanding what Geo Market Watch is, who it's for, and how to adopt it.

| Document | Purpose |
|----------|---------|
| [Positioning](product/positioning.md) | What this repository is and isn't |
| [Commercial Use](product/commercial-use.md) | License and usage guidelines |
| [Roadmap v6](product/roadmap-v6.md) | Version 6 development roadmap |
| [README Changes](product/readme-refactor-changes.md) | Recent README improvements |

---

## 🏗️ Architecture Layer

System design, data models, and technical specifications.

| Document | Purpose |
|----------|---------|
| [System Overview](architecture/system-overview.md) | High-level system architecture |
| [Institutional Framework](architecture/institutional-framework.md) | Four-layer institutional architecture |
| [System Evolution](architecture/system-evolution.md) | v5 → v7 roadmap and evolution |
| [Design Principles](architecture/design-principles.md) | Core design decisions and philosophy |
| [Minimal Agent](architecture/minimal-agent.md) | v5.5 agent loop architecture |
| [Database Spec](architecture/database-spec.md) | Geo Alpha database specification |
| [Event Database Design](architecture/event-database-design.md) | Event storage design |
| [Event Card Schema](architecture/event-card-schema.md) | Event card data structure |
| [Scoring Engine Spec](architecture/scoring-engine-spec.md) | Signal scoring system |
| [Notification Spec](architecture/notification-spec.md) | Output format specification |
| [Signal Scoring](architecture/signal-scoring.md) | How events become scores |
| [Full Analysis Trigger](architecture/full-analysis-trigger.md) | Escalation logic |

---

## ✅ Evaluation Layer

Benchmarks, validation, and quality assurance.

| Document | Purpose |
|----------|---------|
| [Benchmark v5](evaluation/benchmark-v5.md) | v5.0 validation |
| [Benchmark v5.4](evaluation/benchmark-v5.4.md) | v5.4 validation |
| [Benchmark v5.5](evaluation/benchmark-v5.5.md) | v5.5 validation |
| [Benchmark v6](evaluation/benchmark-v6.md) | v6.0 validation |
| [Benchmark v6.3](evaluation/benchmark-v6.3.md) | v6.3 validation |
| [Benchmark v6.4](evaluation/benchmark-v6.4.md) | v6.4 validation |
| [Validation Checklist](evaluation/validation-checklist.md) | Quality assurance checklist |

---

## ⚙️ Operations Layer

Running the system, workflows, and day-to-day usage.

| Document | Purpose |
|----------|---------|
| [Quick Start](operations/quickstart.md) | 10-minute getting started guide |
| [Scheduled Monitoring](operations/scheduled-monitoring.md) | Setting up monitoring schedules |
| [Analyst Workflow](operations/analyst-workflow.md) | Review and approval process |
| [Analyst Review Guidelines](operations/analyst-review-guidelines.md) | Quality standards for review |
| [Idea Lifecycle Spec](operations/idea-lifecycle-spec.md) | Trade idea state management |
| [Idea Performance Spec](operations/idea-performance-spec.md) | Performance tracking system |
| [Performance Methodology](operations/performance-methodology.md) | Return calculation methods |
| [Performance Tracking](operations/performance-tracking.md) | Paper-trade evaluation |
| [Idea Outcome Classification](operations/idea-outcome-classification.md) | Outcome buckets and thresholds |
| [Automation Guide](operations/automation-guide.md) | Automating workflows |
| [Database Query Examples](operations/database-query-examples.md) | Common database queries |

---

## 🔬 Research Layer

Methodology, sources, and research practices.

| Document | Purpose |
|----------|---------|
| [Methodology](research/methodology.md) | Research methodology and approach |
| [Source Tiering](research/source-tiering.md) | Information source hierarchy |
| [Scout Mode Example](research/scout-mode-example.md) | Early detection examples |

---

## 📁 Daily Artifacts

Event cards and scout scans generated during daily operations.

- `event-cards/` — Structured event cards
- `event-card-YYYY-MM-DD-NNN.md` — Daily event cards
- `scout-scan-YYYY-MM-DD.md` — Daily scout reports

---

## Quick Links

**Getting Started:**
1. Read [Product Positioning](product/positioning.md)
2. Follow [Quick Start](operations/quickstart.md)
3. Explore [System Architecture](architecture/institutional-framework.md)

**For Developers:**
- [Database Spec](architecture/database-spec.md)
- [Event Card Schema](architecture/event-card-schema.md)
- [Scoring Engine Spec](architecture/scoring-engine-spec.md)

**For Analysts:**
- [Analyst Workflow](operations/analyst-workflow.md)
- [Performance Tracking](operations/performance-tracking.md)
- [Methodology](research/methodology.md)

---

## Documentation Principles

1. **Layered** — Organized by concern (Product → Architecture → Operations)
2. **Versioned** — Benchmarks and specs tied to releases
3. **Practical** — Examples and runnable commands
4. **Evolving** — Updated with each release

---

**Need help?** Start with [Quick Start](operations/quickstart.md) or explore by layer above.
