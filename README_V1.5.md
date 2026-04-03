# geo-market-watch Phase 0 Governance Policy V1.5

## Purpose

This document defines the Phase 0 governance policy for `geo-market-watch`.

Phase 0 is not a feature expansion phase. It is a **trustworthiness hardening phase**.

The goal is to move `geo-market-watch` from a "smart but slippery analyst" toward a **high-trust geopolitical market radar** with explicit guardrails, observable failure modes, and auditable outputs.

---

## 1. Identity and Responsibility Boundary

### System Identity
`geo-market-watch` is a **geopolitical event to market-mapping observation system** with strict evidence constraints.

It is designed to:
- extract and organize relevant geopolitical developments
- separate facts from inference
- map events to market monitoring logic
- produce high-trust observation drafts for human review and action

### Non-Goal
`geo-market-watch` is **not** an automated trading decision engine.

It must not:
- give direct buy/sell/position-sizing instructions
- present speculative logic as confirmed reality
- simulate confidence it does not actually possess

### Core Principle
**Better silence than false precision.**

If the system lacks sufficient evidence, it should downgrade, defer, or remain silent rather than generate convincing but weakly grounded output.

---

## 2. Phase 0 Objective

Phase 0 focuses on one thing:

> Build a minimum trustworthy layer before expanding intelligence, automation, or asset coverage.

This phase exists to reduce:
- fabricated precision
- fact/inference mixing
- ungrounded source claims
- careless ticker mapping
- black-box silent failures

---

## 3. Output Contract

All output must be explicitly separated into the following three layers:

### A. Confirmed
Content that is directly supported by source material.

Rules:
- must be traceable to provided context
- must not include extrapolation disguised as fact
- quoted claims from officials/media must not be upgraded into objective facts

### B. Inferred
Reasoned interpretation derived from confirmed facts.

Rules:
- must be clearly labeled as inference
- must not be written in a tone of certainty equal to confirmed facts
- should degrade or expire if not refreshed by new evidence

### C. Trade Hypothesis
Observation-oriented market logic for human monitoring.

Rules:
- must remain hypothesis, not instruction
- must include observation conditions and invalidation conditions whenever possible
- must not imply execution certainty

---

## 4. Hard Red Lines

The following are **non-negotiable intercept conditions**.

If any of these are triggered, the payload must be blocked or downgraded by the Python guard layer.

### 4.1 Number Hallucination
Intercept any output containing:
- percentages
- dollar values
- supply gaps
- casualty counts
- time estimates
- production/transport figures
- other concrete numerical claims

unless they can be validated against the provided source context.

### 4.2 Fact / Stance Collapse
Intercept any case where:
- "threatened"
- "claimed"
- "signaled"
- "reportedly considering"
- "rumored"
- "unconfirmed"

is incorrectly rewritten as a confirmed fact.

Example:
- unacceptable: "Iran has fully closed the Strait"
- acceptable only if source directly confirms closure with sufficient support

### 4.3 Unsupported Strong Assertions
Intercept unsupported use of high-certainty wording such as:
- inevitable
- certain
- fully
- comprehensive
- total
- definitive
- guaranteed

unless supported by strong and sufficient evidence.

### 4.4 Unauthorized Ticker Expansion
Intercept any ticker recommendation or mapping that is:
- outside `ticker_registry.yaml`
- not routed through an approved macro transmission path
- weakly stitched together by generic sector logic

### 4.5 Fabricated Source Authority
Intercept any case where the model claims a source that is not actually present in the provided context.

**JSON is a container, not evidence.**
A structured field like `"source": "Reuters"` is not valid unless it can be verified against the real input context.

---

## 5. Governance Model: Prompt + Code Guard

Phase 0 uses a dual-governance approach.

### 5.1 System Prompt Responsibilities (Soft Discipline)
The model is responsible for:
- following the three-layer output contract
- using restrained, institutional tone
- returning structured output in approved schema
- distinguishing confirmed facts from inference
- avoiding overconfident language

### 5.2 Python Guard Responsibilities (Hard Intercepts)
The code layer is responsible for:
- reverse source validation
- number auditing
- whitelist ticker enforcement
- schema integrity validation
- intercept logging
- final payload gating before push

### Principle
Do not rely on model obedience for critical trust decisions.

Prompt shapes behavior.  
Code enforces law.

---

## 6. Auditability and Observability

Phase 0 must not produce black-box silence.

A blocked payload must leave behind a machine-readable and human-readable trail.

### Required Artifact
`Guard_Trace.log`

This log should record at minimum:
- timestamp
- event identifier if available
- intercept rule triggered
- affected sentence/field if available
- source validation result
- hallucination classification
- retry / drop decision

### Hallucination Classification
Every intercepted issue should be classified where possible as:

#### Type A  --  Pure Hallucination
The number / source / claim does not exist in the provided context.

Examples:
- fabricated numerical value
- fabricated source attribution
- fabricated event detail

#### Type B  --  Logic Stretch
A number or fact exists in source material, but the model incorrectly attaches it to:
- the wrong conclusion
- the wrong ticker
- the wrong market implication
- the wrong confidence level

### Why This Matters
Without audit traces, Phase 0 risks becoming a silent black box:
- no push sent
- no clear reason
- no improvement path

Guard traces convert silence into diagnosable behavior.

---

## 7. State Handling: Minimum Viable State Machine

Phase 0 introduces a minimal stateful layer.

### Storage Role
Use **SQLite** as the minimum viable state store.

### Why SQLite
At this stage, SQLite is sufficient to support:
- `event_id`-based state tracking
- overwrite/update behavior
- basic historical state retention
- low operational complexity

### Notion Role
Notion is explicitly downgraded to:
- static dashboard
- weekly review surface
- presentation / archival layer

Notion is **not** the real-time system of record.

### State Principle
New information should not merely append new text.  
It should update the event object when appropriate.

---

## 8. Time Decay Policy

Inference must have an expiry mechanism.

### TTL Rule
`Inferred` content has a default TTL of **24 hours**.

If no fresh confirming evidence arrives within the TTL:
- mark inference as stale
- downgrade its visibility or confidence
- require re-evaluation before reuse

### Purpose
This prevents:
- stale narratives persisting as live logic
- yesterday's market explanation becoming today's hidden assumption
- unrefreshed inference contaminating real-time decision support

---

## 9. Asset Mapping Policy

### General Rule
Asset mapping must be conservative and registry-driven.

The model may assist with reasoning, but final asset references must obey explicit mapping rules.

### Ticker Registry
All asset references must be validated against:
- `ticker_registry.yaml`

### Macro Path Requirement
A ticker may only appear if a valid macro channel exists between:
1. the geopolitical event
2. the transmission mechanism
3. the asset category
4. the ticker itself

No free-form "sounds related" mapping.

---

## 10. Special Policy for COIN / Crypto

Crypto-related assets are explicitly treated as **non-linear**.

### Problem
Assets like `COIN` can flip roles depending on the nature of the shock.

They may behave as:
- risk-on beta
- liquidity-stress casualty
- alternative asset rail
- payment / sanction workaround narrative
- fiat distrust proxy

### Required Logic
Before generating a COIN-related observation, the system must classify the dominant transmission path.

#### Path A  --  Risk-off / Liquidity Tightening
Conflict increases:
- macro uncertainty
- liquidity stress
- risk-off sentiment

Expected implication:
- crypto-linked equities may trade down with broader risk assets

#### Path B  --  Alternative / Payment Rail / Trust Disruption
Conflict increases:
- distrust in conventional rails
- sanctions circumvention narratives
- alternative settlement narratives
- local payment disruption concerns

Expected implication:
- crypto-related assets may gain relevance as alternative channels

### Output Requirement
Any COIN-related hypothesis must include an explicit path label, for example:
- `[Path A: Risk-off Liquidity Logic]`
- `[Path B: Alternative Assets Logic]`

No unlabeled COIN narrative is allowed.

---

## 11. Phase 0 Deliverables

Phase 0 should produce the following minimum components:

1. `README_V1.5.md`
2. system prompt implementing the three-layer contract
3. `logic_gate.py` for hard intercepts
4. `ticker_registry.yaml`
5. `Guard_Trace.log`
6. minimal SQLite event store
7. small benchmark / replay set for validation

---

## 12. Definition of Done

Phase 0 is considered complete only when the following conditions are met:

### 12.1 Replay Coverage
Run at least 5 historical geopolitical scenarios through the pipeline, such as:
- Iran / Strait of Hormuz escalation
- Red Sea / shipping disruption
- Russia-Ukraine escalation window
- sanctions shock scenario
- energy supply disruption scenario

### 12.2 Hallucinated Number Interception
Guard layer catches hallucinated numeric claims with effectively full reliability in benchmark testing.

Operational target:
- **100% interception of clearly unsupported numerical hallucinations** in benchmark set

### 12.3 Reversal Handling
When a core fact reverses, the system updates state instead of silently stacking narratives.

Example:
- "closure risk" -> "partial opening"
- "escalation risk" -> "de-escalation signal"

### 12.4 Guard Trace Quality
Every blocked payload must leave a usable trace in `Guard_Trace.log`.

### 12.5 UX Shift
QQ push output should visibly evolve from:
- smooth long-form prose

toward:
- compact
- structured
- source-aware
- confidence-bounded
- observation-oriented cards

Each inference should include:
- why it exists
- what to observe
- what could invalidate it

---

## 13. Explicit Out-of-Scope Items for Phase 0

To avoid premature optimization, the following are **not** part of Phase 0:

- full PostgreSQL migration
- complex workflow orchestration
- large-scale asset universe expansion
- full UI-based approval backend
- fully automated evaluation platform
- direct trading execution logic
- broad autonomous strategy generation

These may come later.  
They are not required to validate the trust layer.

---

## 14. Development Principle

Phase 0 is a defensive architecture exercise.

The goal is not to make the model sound smarter.  
The goal is to make the system more trustworthy.

### The hierarchy is:
1. evidence over elegance
2. traceability over fluency
3. constrained usefulness over impressive verbosity
4. explicit uncertainty over false confidence

---

## 15. Final Operational Motto

**Do not let the model sound more certain than the evidence allows.**

If Phase 0 succeeds, `geo-market-watch` will stop behaving like a fluent storyteller and start behaving like a disciplined market sentry.
