# Geo Market Watch v6 Roadmap
## Toward an LLM-Native Geopolitical Market Intelligence System

Geo Market Watch started as a structured prompt framework that converts
geopolitical news into structured market watchlists.

Version 6 aims to evolve the project into a **complete intelligence workflow**
capable of continuously monitoring geopolitical events and translating them
into market-relevant signals.

The goal is not simply better summaries, but a system that can:

- discover events earlier
- evaluate credibility
- map geopolitical shocks to market propagation paths
- generate structured watchlists
- track triggers and invalidation signals
- learn from historical outcomes

---

# Vision

Geo Market Watch v6 becomes an **LLM-native geopolitical market intelligence
orchestration framework**.

Instead of a single analysis prompt, the system evolves into a multi-stage
pipeline:

```
Event Discovery
↓
Verification
↓
Market Propagation Mapping
↓
Watchlist Generation
↓
Trigger Monitoring
↓
Review & Learning
```

The system's mission is:

> Translate complex geopolitical disturbances into structured market
> observation signals earlier and more reliably.

---

# Core Design Principles

## 1. Event-Driven Architecture

The system revolves around **events**, not articles.

Each input becomes a structured **Event Object** containing:

- timestamp
- geography
- actors
- event category
- source tier
- confidence level

This ensures every analysis stage operates on a consistent data model.

---

## 2. Separation of Responsibilities

v6 separates different analytical responsibilities into specialized agents.

| Agent | Responsibility |
|-------|---------------|
| Scout Agent | Broad scanning and escalation decisions |
| Verification Agent | Source credibility and Fog-of-War handling |
| Mapping Agent | Translating events into market propagation chains |
| Watch Agent | Generating watchlists and trigger signals |

This improves reliability and modularity.

---

## 3. Structured Outputs

All analysis results must follow a structured output contract.

Required sections:

- Confirmed Facts
- Market Interpretation
- Scenario Analysis
- Watchlist
- Trigger Signals
- Invalidation Conditions

In addition to human-readable reports, v6 introduces **machine-readable
JSON outputs**.

---

## 4. Fog-of-War Awareness

Geopolitical information is often incomplete or contradictory.

v6 introduces a **Fog-of-War mode** that activates when:

- conflicting sources appear
- only low-tier sources exist
- casualty/damage numbers differ significantly
- key details remain unverified

In this mode the system reduces certainty and focuses on monitoring signals.

---

# System Capabilities

v6 introduces several new capabilities.

## 1. Continuous Event Discovery

Instead of relying only on manual inputs, the system can periodically scan
news feeds and policy updates.

Example inputs include:

- geopolitical news
- sanctions announcements
- shipping disruptions
- commodity supply interruptions
- military escalation signals

---

## 2. Escalation Engine

Not every headline deserves deep analysis.

The escalation engine evaluates whether an event is worth further analysis
based on factors such as:

- involvement of chokepoints (ports, canals, pipelines)
- potential supply chain disruptions
- commodity exposure
- state actor involvement
- sanction or trade policy changes

---

## 3. Market Propagation Mapping

v6 models how geopolitical shocks propagate through the global economy.

Example propagation chain:

```
Red Sea attacks
↓
Shipping route diversion
↓
Longer transit times
↓
Container shortages
↓
Freight rate increases
```

This mapping layer transforms narrative news into structured market logic.

---

## 4. Watchlist Generation

The system converts propagation analysis into **structured watchlists**.

Each watchlist entry contains:

- ticker
- market
- thesis
- physical node mapping
- trigger signal
- invalidation condition
- confidence level

---

## 5. Trigger Monitoring

Triggers define observable signals that confirm the thesis.

Examples include:

- freight insurance costs rising
- port throughput declines
- official sanction announcements
- production stoppages

---

## 6. Historical Review

v6 records past analyses and evaluates outcomes.

This allows the system to track:

- trigger accuracy
- escalation accuracy
- scenario outcomes

Over time this creates a feedback loop that improves signal quality.

---

# Development Phases

## Phase 1 — Framework Hardening

Focus on strengthening the analysis framework.

Key work:

- documentation cleanup
- schema definition
- validation tests
- example cases
- structured output contract

---

## Phase 2 — Multi-Agent Workflow

Introduce specialized analysis agents.

Components:

- scout agent
- verification agent
- mapping agent
- watchlist agent

Automation platforms can orchestrate these agents.

---

## Phase 3 — Intelligence System

Transform the framework into a full intelligence platform.

New capabilities:

- event memory
- propagation graph
- signal scoring
- monitoring dashboard
- automated alert routing

---

# Long-Term Goal

The long-term goal of Geo Market Watch is to become a **structured geopolitical
intelligence layer for financial markets**.

Rather than replacing human analysis, the system augments it by:

- filtering noise
- identifying early signals
- structuring complex events into actionable observations
