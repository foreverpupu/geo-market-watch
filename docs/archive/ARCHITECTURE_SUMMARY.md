# Geo Market Watch v6.4 — Architecture Documentation

## Two Architecture Views

### 1. System Evolution Architecture
**File:** `docs/system-evolution-architecture.md`

**Purpose:** Shows version-by-version evolution from v5 to v7

**Format:** Timeline with ASCII diagrams

**Best for:** Understanding release roadmap and feature progression

```
v5 Monitoring Foundation
  Scout → Score → Agent

v6 Intelligence Platform  
  Database → Exposure → Workflow → Performance

v7 Multi-Agent Intelligence
  Risk Map → Pattern Mining → Strategy Layer
```

---

### 2. Institutional System Architecture
**File:** `docs/institutional-system-architecture.md`

**Purpose:** Four-layer framework for enterprise understanding

**Format:** Layered architecture with data flows

**Best for:** Technical documentation and institutional presentations

```
┌─────────────────────────────────────────┐
│           DATA LAYER                    │
│   Raw Signals → Structured Memory       │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│           AGENT LAYER                   │
│   Monitoring Loop → Escalation          │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│        INTELLIGENCE LAYER               │
│   Event → Exposure → Alpha Logic        │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│          RESEARCH LAYER                 │
│   Review → Lifecycle → Performance      │
└─────────────────────────────────────────┘
```

---

## When to Use Each

| Use Case | Recommended Doc |
|----------|-----------------|
| Release planning | System Evolution |
| Technical overview | Institutional Architecture |
| Investor presentation | Institutional Architecture |
| Developer onboarding | Both |
| Feature comparison | System Evolution |
| Integration planning | Institutional Architecture |

---

## Current Implementation Status

| Layer | Component | Status | Version |
|-------|-----------|--------|---------|
| **Data** | Raw Signal Intake | ✅ | v5.3 |
| **Data** | Event Database | ✅ | v6.0 |
| **Data** | Export Layer | ✅ | v6.1 |
| **Agent** | Scout Engine | ✅ | v5.3 |
| **Agent** | Scoring Engine | ✅ | v5.4 |
| **Agent** | Monitoring Agent | ✅ | v5.5 |
| **Intelligence** | Exposure Engine | ✅ | v6.2 |
| **Intelligence** | Trade Idea Engine | ✅ | v6.2 |
| **Research** | Analyst Review | ✅ | v6.3 |
| **Research** | Performance Tracking | ✅ | v6.4 |

---

## README Integration

Both architecture documents are linked from README.md:

```markdown
**Detailed Architecture:** 
[docs/system-evolution-architecture.md](docs/system-evolution-architecture.md) | 
[Institutional Four-Layer View](docs/institutional-system-architecture.md)
```

---

**v6.4 Architecture Documentation Complete** ✅
