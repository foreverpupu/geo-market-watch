# Geo Market Watch Architecture

This document describes the high-level system architecture of Geo Market Watch
v6.

The architecture is designed to transform geopolitical events into structured
market intelligence signals.

---

# System Overview

The Geo Market Watch system consists of six logical layers.

```mermaid
flowchart TB
    subgraph Input["Input Layer"]
        A1["News Articles"]
        A2["Government / Policy Updates"]
        A3["Shipping / Commodity Signals"]
        A4["User-Provided Links"]
    end

    subgraph Intake["Event Intake"]
        B1["Source Collection"]
        B2["Deduplication"]
        B3["Event Normalization"]
    end

    subgraph Scout["Scout & Escalation"]
        C1["Scout Agent"]
        C2["Escalation Engine"]
    end

    subgraph Verify["Verification Layer"]
        D1["Source Tiering"]
        D2["Contradiction Detection"]
        D3["Fog-of-War Handling"]
    end

    subgraph Mapping["Market Mapping"]
        E1["Propagation Graph"]
        E2["Sector / Asset Translation"]
        E3["Physical Node Mapping"]
    end

    subgraph Output["Output Layer"]
        F1["Watchlist Generation"]
        F2["Trigger Signals"]
        F3["Invalidation Conditions"]
        F4["Structured Analysis Output"]
    end

    subgraph Memory["Memory & Review"]
        G1["Historical Storage"]
        G2["Outcome Review"]
        G3["Signal Quality Feedback"]
    end

    subgraph Delivery["Delivery / Integration"]
        H1["Reports"]
        H2["JSON / API"]
        H3["Alerts / Dashboards"]
    end

    Input --> Intake
    Intake --> Scout
    Scout --> Verify
    Verify --> Mapping
    Mapping --> Output
    Output --> Delivery
    Output --> Memory
    Memory --> Scout
    Memory --> Verify
    Memory --> Mapping
```

Each layer performs a specialized function in the intelligence pipeline.

---

# Layer 1 — Event Intake

The Event Intake Layer collects raw inputs from multiple sources.

Possible sources include:

- news articles
- government announcements
- sanction lists
- commodity market reports
- shipping updates
- social media signals

The purpose is to normalize incoming information into a consistent structure.

Example Event Object:
```
event_id
timestamp
location
actors
event_type
source
confidence
raw_input
```

---

# Layer 2 — Scout Agent

The Scout Agent performs rapid scanning and determines whether an event
should be escalated for deeper analysis.

Responsibilities:

- summarize the event
- estimate credibility
- identify potential market domains
- assign escalation score

Output example:
```
event_summary
confidence_level
market_domains
escalation_score
recommendation
```

---

# Layer 3 — Verification Layer

This layer evaluates the credibility of the event.

Key tasks:

- compare multiple sources
- detect contradictions
- evaluate source tiers
- determine confidence level

If the information environment is unstable, the system activates
**Fog-of-War mode**.

---

# Layer 4 — Market Propagation Graph

This layer maps geopolitical events to economic and market consequences.

Propagation nodes include:

- geography
- commodities
- logistics infrastructure
- supply chains
- industry sectors
- financial instruments

Example propagation chain:
```
Sanction on metal exports
↓
Global supply tightening
↓
Commodity price increase
↓
Mining company benefit
```

---

# Layer 5 — Watchlist Engine

The Watchlist Engine converts propagation insights into structured
observation targets.

Each watchlist item includes:

- ticker
- asset name
- thesis
- trigger signal
- invalidation condition
- time horizon
- confidence level

---

# Layer 6 — Memory & Review

The final layer stores historical analyses and outcomes.

Recorded information includes:

- event data
- propagation logic
- watchlists
- triggers
- invalidations
- later outcomes

This enables retrospective evaluation and model improvement.

---

# Agent Collaboration Model

The system relies on multiple specialized agents.

```
Scout Agent
↓
Verification Agent
↓
Mapping Agent
↓
Watchlist Agent
```

Each agent focuses on a specific analytical responsibility.

---

# Structured Output

All deep analysis results follow a standardized structure.

Required sections:

- Confirmed Facts
- Market Interpretation
- Scenario Analysis
- Watchlist
- Trigger Signals
- Invalidation Conditions

Additionally, the system can produce machine-readable JSON outputs
for integration with automation tools.

---

# Integration Layer

Geo Market Watch does not implement scheduling internally.

Instead it integrates with external automation platforms such as:

- workflow automation tools
- agent orchestration frameworks
- notification systems

These tools handle:

- scheduling
- data ingestion
- alert delivery
