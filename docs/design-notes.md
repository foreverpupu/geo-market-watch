# Design Notes

## Purpose

This document explains the **design philosophy** behind Geo Market Watch.

While `README.md` explains what the project does, and `CHANGELOG.md` records what changed, this file answers a different question:

**Why was the workflow designed this way?**

Geo Market Watch is not just a prompt or a summary template. 
It is a deliberately structured research workflow for turning geopolitical news into disciplined market observation.

The design evolved around one core problem:

> Geopolitical news is noisy, emotionally distorted, operationally incomplete, and often poorly mapped into actual market exposure.

The project exists to reduce that gap.

---

## The core problem

Most geopolitical-news workflows fail in one of four ways:

1. **They summarize headlines but do not map them into assets.**
2. **They mix confirmed facts, interpretation, and speculation into one layer.**
3. **They overreact to rhetoric, tone, or viral narratives.**
4. **They produce watchlists without clear invalidation logic.**

This creates an illusion of clarity while actually increasing analytical risk.

Geo Market Watch was designed to solve those four problems directly.

---

## Design philosophy

The framework follows a few non-negotiable design principles.

## 1. Separate fact from interpretation
This is the single most important design choice.

Geopolitical reporting often blurs:

- what has happened
- what may happen
- what officials claim
- what commentators infer
- what the market is pricing

If those layers are merged too early, the output becomes unstable and misleading.

That is why the framework forces three explicit layers:

- **Confirmed Facts**
- **Market Interpretation**
- **Scenario Analysis**

This is not a formatting preference. 
It is the core mechanism that prevents analytical contamination.

---

## 2. Use source hierarchy as a control system
The project is built on the idea that **not all sources should enter the same layer of analysis**.

A strong workflow should know:

- which sources can anchor facts
- which sources can help explain structure
- which sources should be downranked or ignored

This led to the Tier 1 / Tier 2 / low-trust distinction.

### Why this matters
In geopolitical events, the error is often not "the model can't reason." 
The error is that the model reasons on top of contaminated inputs.

The source hierarchy is a form of **input risk control**.

It exists to prevent:
- official rhetoric from becoming "market facts"
- emotional headlines from driving interpretation
- high-tone commentary from leaking into the fact layer

---

## 3. Reward variables, not drama
Many sources are emotionally loud but analytically empty.

The framework therefore prefers:

- measurable exposure
- physical bottlenecks
- routing constraints
- export shares
- infrastructure nodes
- observable market signals

instead of:
- dramatic adjectives
- vague escalation narratives
- abstract "this changes everything" claims
- unsupported certainty

This is why the project emphasizes **physical bottlenecks** and **market exposure translation**.

The goal is to move from:

> "This sounds serious"

to:

> "Which node is affected, by how much, and how does that map into listed assets?"

---

## 4. Build testable watchlists
A watchlist without invalidation logic is not research. It is storytelling.

The framework requires every name to include:

- why it belongs
- a concrete trigger signal
- a concrete invalidation condition

This is not optional. It is mandatory.

### Why this matters
Without invalidation conditions, the user has no exit discipline.

The framework exists to prevent:
- holding a position after the original thesis is broken
- confusing "the event is still ongoing" with "the trade still works"
- narrative attachment instead of evidence-based position management

---

## 5. Preserve uncertainty visibly
In fast-moving geopolitical situations, key facts often remain disputed for hours or days.

The framework does not force false certainty.

If credible sources disagree, the dispute should remain visible.

This led to the **Fog of War Rule**:

- mark contested facts explicitly
- do not collapse disputes into single certainties
- state what evidence would resolve the dispute

This is especially important in the first 12–48 hours after major events.

---

## 6. Design for automation, not just conversation
The project was built with two use cases in mind:

1. **Interactive mode**: user provides links, receives structured output
2. **Scheduled mode**: system scans, filters, and surfaces only high-signal events

This is why the framework includes:
- a **Discovery Mode** with strict scoring thresholds
- a **Scout Prompt** with hard execution limits
- clear escalation rules for when to upgrade to full analysis

The goal is to prevent:
- alert fatigue from low-signal events
- wasted compute on weak or old news
- forced output when nothing actionable has occurred

---

## Why this design works

The framework is not perfect, but it is **robust**.

It survives:
- emotional source inputs
- incomplete early reporting
- conflicting claims
- paywalled or missing data
- model drift across versions

It survives because the design is not just a prompt.
It is a **structured workflow with built-in quality controls**.

---

## For maintainers

If you modify this framework, ask yourself:

- Does this change preserve the fact / interpretation / scenario separation?
- Does it strengthen or weaken source discipline?
- Does it make watchlists more or less testable?
- Does it increase or decrease visible uncertainty?
- Does it help or hurt automation safety?

If a change weakens any of those five, it should be reconsidered.

---

## Summary

Geo Market Watch exists because:

> Geopolitical news is noisy, but market observation must be disciplined.

The design is the discipline.

Use it. Test it. Improve it. But do not dilute it.
