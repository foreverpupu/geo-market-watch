# Minimal Agent Architecture

This document describes the v5.5 minimal agent loop architecture.

---

## Overview

Geo Market Watch v5.5 introduces the first **end-to-end runnable agent loop**.

This is intentionally a **minimal local workflow**, not a production platform.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT                                                      │
│  Raw intake items (JSON)                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NODE 1: Intake Normalizer                                  │
│  • Load raw items                                            │
│  • Convert to Event Card format                              │
│  • Generate event keys for deduplication                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NODE 2: Deduplication Memory                               │
│  • Load seen event keys                                      │
│  • Split new vs duplicate events                             │
│  • Mark new events as seen                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NODE 3: Scoring & Trigger                                  │
│  • Compute signal score (0-10)                               │
│  • Determine signal band                                     │
│  • Evaluate trigger conditions                               │
│  • Decide: monitor vs full analysis                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NODE 4: Notify / Handoff                                   │
│  • Render monitor notification (markdown)                    │
│  • OR render full analysis handoff (markdown)                │
│  • Write to output directory                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT                                                     │
│  • Updated dedupe memory                                     │
│  • Notification files (monitor_*.md / full_analysis_*.md)   │
│  • Run summary                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### Single Process
- No queues
- No async/await
- No multi-threading
- Linear execution flow

### Zero External Dependencies
- No API calls
- No database connections
- No cloud services
- File-based only

### Deterministic
- Same input → same output
- Reproducible runs
- Testable components

### Minimal Scope
- Intentionally narrow
- Validates the loop, not the platform
- Foundation for future expansion

---

## What This Is NOT

❌ **Live RSS/news ingestion platform**  
❌ **Production scheduler**  
❌ **Event database product**  
❌ **Multi-agent system**  
❌ **Hosted intelligence engine**

This is a **local runnable workflow** that proves the concept before building the platform.

---

## File Structure

```
engine/
├── intake_normalizer.py    # Node 1
├── dedupe_memory.py        # Node 2
├── scoring_engine.py       # Node 3 (v5.4)
├── trigger_engine.py       # Node 3 (v5.4)
├── notifier.py             # Node 4
└── agent_loop.py           # Orchestrator

scripts/
└── run_agent_loop.py       # CLI entry point

data/
├── intake-sample.json      # Sample input
└── dedupe-memory.json      # Deduplication state

outputs/                    # Generated notifications
├── monitor_*.md
└── full_analysis_*.md
```

---

## Usage

```bash
python scripts/run_agent_loop.py \
  --input data/intake-sample.json \
  --memory data/dedupe-memory.json \
  --output outputs/
```

---

## Future Expansion

This minimal architecture provides the foundation for:

- **v5.6**: Live news ingestion (RSS, APIs)
- **v5.7**: Fuzzy deduplication (similarity matching)
- **v5.8**: Database persistence (PostgreSQL, SQLite)
- **v6.0**: Scheduled execution (cron, scheduler)
- **v6.5**: Multi-agent orchestration
- **v7.0**: Hosted platform

Each expansion builds upon the proven v5.5 loop.

---

## Validation

The architecture is validated when:

- [x] All 4 nodes execute in sequence
- [x] Duplicates are correctly filtered
- [x] New events receive exactly one notification
- [x] Monitor and handoff paths both work
- [x] Output is deterministic and reproducible

Run: `python scripts/run_agent_loop.py --input data/intake-sample.json --memory data/dedupe-memory.json --output outputs/`
