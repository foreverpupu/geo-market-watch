# Geo Market Watch — Institutional System Architecture

## Four-Layer Framework

```
┌──────────────────────────────────────────────────────────────────────────────┐
│           GEO MARKET WATCH — SYSTEM ARCHITECTURE                             │
│              Institutional Four-Layer Framework                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Layer 1 — Data Layer
**Raw Signals → Structured Memory → Exports**

```
External News / Feeds / Analyst Inputs
           │
           ▼
    ┌──────────────────────┐
    │   Raw Signal Inputs  │
    │  headlines / summaries│
    │  links / manual notes │
    └──────────────────────┘
           │
           ▼
    ┌──────────────────────┐
    │   Normalized Events  │
    │    event cards       │
    │   structured signals │
    └──────────────────────┘
           │
           ▼
    ┌──────────────────────┐
    │  Geo Alpha Database  │
    │       events         │
    │       sources        │
    │      indicators      │
    │        flags         │
    │    notifications     │
    │      watchlists      │
    └──────────────────────┘
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
┌─────────┐ ┌──────────┐ ┌──────────────────┐
│ Event   │ │ Export   │ │ Snapshot Outputs │
│ Store   │ │ Layer    │ │ dashboard-ready  │
│ history │ │JSON / CSV│ │     files        │
└─────────┘ └──────────┘ └──────────────────┘
```

**Components:**
- Raw signal intake
- Event normalization
- Persistent database
- Export layer

---

## Layer 2 — Agent Layer
**Monitoring Loop → Detection → Escalation**

```
    ┌──────────────────────┐
    │   News Intake Agent  │
    │  scan / collect / load│
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │     Dedupe Agent     │
    │    event identity    │
    │   duplicate filtering │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │    Scoring Agent     │
    │   deterministic score │
    │     signal banding    │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │    Trigger Agent     │
    │  full-analysis rules  │
    │  escalation decision  │
    └──────────────────────┘
              │
       ┌──────┴──────┐
       ▼             ▼
┌─────────────────┐ ┌────────────────────┐
│ Monitoring      │ │ Full Analysis Path │
│ Output          │ │ escalation handoff │
│ watch / notify  │ │                    │
└─────────────────┘ └────────────────────┘
```

**Future v7 Extension:**
```
News Agent → Event Agent → Risk Agent → Alpha Agent
```

---

## Layer 3 — Intelligence Layer
**Event Understanding → Exposure Mapping → Alpha Logic**

```
    ┌──────────────────────┐
    │  Event Understanding │
    │    confirmed facts   │
    │   scenario framing   │
    │  market transmission │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │    Exposure Engine   │
    │    event → sector    │
    │   sector → company   │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │   Trade Idea Engine  │
    │   thesis generation  │
    │  invalidation logic  │
    │  conviction mapping  │
    └──────────────────────┘
```

**Components:**
- Event understanding
- Sector exposure mapping
- Company exposure mapping
- Trade idea generation

---

## Layer 4 — Research Layer
**Human Review → Lifecycle → Performance Evaluation**

```
    ┌──────────────────────┐
    │   Analyst Review     │
    │   approve / reject   │
    │   monitor / revise   │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │   Lifecycle Engine   │
    │   status tracking    │
    │   invalidation rules │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Performance Tracking │
    │  entry / close refs  │
    │   return calculation │
    │  outcome classification│
    └──────────────────────┘
```

**Components:**
- Analyst review workflow
- Lifecycle management
- Paper performance tracking
- Outcome evaluation

---

## Cross-Cutting Concerns

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPPORTING SYSTEMS                       │
├─────────────────────────────────────────────────────────────┤
│  Audit Trail        │  Lifecycle events, review history     │
│  Export Layer       │  JSON, CSV, dashboard snapshots       │
│  Query Interface    │  CLI tools, database queries          │
│  Validation         │  Schema validation, benchmark tests   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Summary

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INPUTS    │ →  │   AGENTS    │ →  │INTELLIGENCE │ →  │  RESEARCH   │
│             │    │             │    │             │    │             │
│ News / Feeds│    │ Monitor /   │    │ Exposure /  │    │ Review /    │
│ Analyst     │    │ Score /     │    │ Trade Ideas │    │ Track /     │
│ Manual      │    │ Trigger     │    │             │    │ Evaluate    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────┐
                    │    Geo Alpha Database   │
                    │   (Persistent Store)    │
                    └─────────────────────────┘
```

---

## Implementation Status

| Layer | Status | Version |
|-------|--------|---------|
| Data Layer | ✅ Complete | v6.0 |
| Agent Layer | ✅ Complete | v5.5 |
| Intelligence Layer | ✅ Complete | v6.2 |
| Research Layer | ✅ Complete | v6.4 |

---

## Design Principles

1. **Local-First** — All data stored locally, full ownership
2. **Deterministic** — Same inputs produce same outputs
3. **Modular** — Each layer independently usable
4. **Auditable** — Complete history and lineage
5. **Paper-First** — Research evaluation before live trading
6. **Human-in-the-Loop** — Analyst review for quality control

---

## System Value Chain

```
Raw Signals
    ↓
Agent Detection
    ↓
Structured Events
    ↓
Persistent Memory
    ↓
Exposure Mapping
    ↓
Trade Ideas
    ↓
Analyst Review
    ↓
Approved Research
    ↓
Performance Feedback
    ↓
Geo Macro Intelligence Platform
```

---

## Version Mapping

| Version | Layer | Components |
|---------|-------|------------|
| **v5** | Monitoring Foundation | Scout Mode → Scoring → Minimal Agent |
| **v6** | Intelligence + Research Platform | Database → Exposure Engine → Review Workflow → Performance Tracking |
| **v7** | Multi-Agent Intelligence Layer | Risk Map → Pattern Mining → Strategy Layer |

---

## Future Extensions (v7+)

- Multi-agent monitoring system
- Global risk mapping
- Alpha pattern mining
- Strategy layer with templates
