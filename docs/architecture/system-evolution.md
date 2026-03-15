# Geo Market Watch — System Evolution Architecture

## v5 → v7 Roadmap

```
┌─────────────────────────────────────────┐
│      GEO MARKET WATCH SYSTEM            │
│        Evolution Architecture           │
└─────────────────────────────────────────┘
```

---

## v5 Series — Monitoring Foundation

### v5.3 — Scout Mode + Event Cards
Convert news signals into structured event objects

```
News Signals → ┌──────────────┐ → Event Cards
               │ Scout Engine │
               └──────────────┘
                      ↓
                 Event Schema
```

### v5.4 — Signal Scoring Engine
Deterministic geopolitical signal scoring

```
Event Cards → ┌─────────────────┐ → Signal Score
              │ Scoring Engine  │
              └─────────────────┘
```

### v5.5 — Minimal Monitoring Agent
Automated monitoring loop

```
News Intake
    ↓
Event Dedupe
    ↓
Score + Trigger
    ↓
Notify / Full Analysis
```

---

## v6 Series — Intelligence Platform

### v6.0 — Geo Alpha Database
Persistent geopolitical event memory

```
Events → ┌───────────────┐ → Historical Dataset
         │ Event Database│
         └───────────────┘
```

### v6.1 — Dashboard Export Layer
Data outputs for monitoring dashboards

```
Database
    ↓
Dashboard Export Layer
    ↓
JSON / CSV Snapshots
```

### v6.2 — Geo Alpha Exposure Engine
Event → Market mapping

```
Event
    ↓
Sector Exposure
    ↓
Company Exposure
    ↓
Trade Idea
```

### v6.3 — Analyst Review Workflow
Human-in-the-loop research system

```
Trade Idea
    ↓
Analyst Review
    ↓
Approve / Reject
    ↓
Lifecycle Tracking
```

### v6.4 — Idea Performance Tracking
Paper alpha evaluation

```
Approved Idea
    ↓
Price Tracking
    ↓
Return Calculation
    ↓
Outcome Classification
```

---

## v7 Series — Multi-Agent Intelligence Layer

### v7.0 — Multi-Agent Monitoring System

```
┌─────────────┐
│  News Agent │
└─────────────┘
      ↓
┌─────────────┐
│ Event Agent │
└─────────────┘
      ↓
┌─────────────┐
│  Risk Agent │
└─────────────┘
      ↓
┌─────────────┐
│ Alpha Agent │
└─────────────┘
```

### v7.1 — Global Risk Map

```
Geopolitical Events
    ↓
Regional Risk Scores
    ↓
Global Risk Map
```

### v7.2 — Alpha Pattern Mining

```
Historical Events
    ↓
Pattern Detection
    ↓
Alpha Signal Discovery
```

### v7.3 — Strategy Layer

```
Geo Signals
    ↓
Strategy Templates
    ↓
Trade Frameworks
```

---

## Final System Form

```
News Signals
    ↓
Monitoring Agents
    ↓
Event Database
    ↓
Exposure Engine
    ↓
Trade Ideas
    ↓
Analyst Workflow
    ↓
Performance Tracking
```

---

## Current Status

**v6.4 — Performance-Aware Research Platform**

✅ Monitoring Foundation (v5)  
✅ Intelligence Platform (v6)  
🔄 Multi-Agent Intelligence (v7) — In Planning

---

## Design Principles

1. **Local-First** — All data stored locally, no cloud dependencies
2. **Deterministic** — Same inputs produce same outputs
3. **Modular** — Each layer can be used independently
4. **Auditable** — Full history and lineage tracking
5. **Paper-First** — Research evaluation before live trading
