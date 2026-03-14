# Source Tiering

## Purpose

Geo Market Watch depends heavily on source quality.

Geopolitical market analysis fails most often not because the event is misunderstood, but because:
- rhetoric is mistaken for fact
- commentary is mistaken for reporting
- emotional amplification is mistaken for signal
- early disputed claims are treated as settled reality

This document defines how sources should be classified and used inside the workflow.

The goal is simple:
- protect the **Confirmed Facts** layer from contamination
- preserve useful structural analysis
- suppress low-quality noise without suppressing legitimate expert insight

---

## Source hierarchy overview

Geo Market Watch uses three broad source categories:
1. **Tier 1 — Ground-truth / factual anchors**
2. **Tier 2 — Structural analysis / variable interpretation**
3. **Low-trust or emotional amplifiers**

These categories are not moral judgments.  
They are functional roles in the workflow.

A source can be:
- excellent for confirmed facts
- weak for market interpretation

or:
- weak for direct fact anchoring
- excellent for identifying structural variables

The purpose of tiering is to decide:
- what can enter the **Confirmed Facts** section
- what belongs in **Market Interpretation**
- what should be downranked or ignored

---

## Tier 1 — Ground-truth / factual anchors

## Definition

Tier 1 sources are the highest-confidence public anchors for **confirmed facts**.

Use Tier 1 sources for statements such as:
- what happened
- when it happened
- where it happened
- what was officially announced
- what is documented in filings or official notices
- what a benchmark or official metric currently shows

Tier 1 sources are allowed in:
- `Confirmed Facts`
- time-sensitive fact verification
- evidence checks against lower-tier claims

## Typical Tier 1 source types

### Official institutions

Examples:
- governments
- ministries
- regulators
- military statements
- customs authorities
- energy ministries
- central banks
- official sanctions bodies
- port authorities
- route or canal authorities

### Top-tier wire services and primary reporting

Examples:
- Reuters
- AP
- other equivalent primary wire-style reporting when confirming concrete facts

### Public company and issuer materials

Examples:
- company filings
- stock exchange notices
- official investor relations pages
- ETF issuer pages
- fund holdings pages
- public presentations when factual and attributable

### Official institution data

Examples:
- agency datasets
- official reported production figures
- public institution metrics
- exchange-traded instrument documentation
- port or route authority updates

---

## What Tier 1 is good for

Tier 1 is good for anchoring:
- exact dates
- confirmed announcements
- confirmed operational status
- current benchmark facts
- named entities and exposures
- official closures or reopenings
- documented holdings or filings

Examples:
- "The canal authority announced a temporary closure."
- "The ETF issuer page lists XOM as a top holding."
- "A government ministry announced export restrictions."
- "Reuters reported that a strike was carried out on a named facility."

---

## What Tier 1 is NOT automatically good for

Tier 1 does **not** automatically convert every statement into a confirmed market fact.

This is especially important in geopolitical situations.

### Official rhetoric is not automatically a fact of market impact

Examples of statements that should be reported carefully:
- threats
- warnings
- retaliation language
- victory claims
- strategic boasting
- emotionally charged adjectives

These may be politically important, but they do not automatically prove:
- physical damage
- lasting disruption
- throughput loss
- export interruption
- market-wide consequences

### Wire-service interpretation paragraphs are not always "pure fact"

Even strong wire reporting may contain:
- analyst interpretation
- scenario framing
- probability language
- estimated significance

These elements can still be valuable, but they should not be mechanically treated as ground truth.

### Interviews and executive commentary

These can be useful, but often mix:
- factual disclosure
- opinion
- spin
- forward-looking guidance

Use carefully.

---

## Tier 1 rule

> Tier 1 anchors **concrete facts**, not interpretation, forecasts, rhetoric, or certainty theater.

If a statement is:
- predictive
- interpretive
- rhetorical
- unverified
- politically strategic

it should not enter the `Confirmed Facts` layer as a hard fact unless independently validated.

---

## Tier 2 — Structural analysis / variable interpretation

## Definition

Tier 2 sources are used for:
- structural explanation
- variable identification
- bottleneck mapping
- market interpretation
- transmission-path logic
- alternative-route analysis
- system dependency discussion

Tier 2 sources belong primarily in:
- `Market Interpretation`
- scenario design
- watchlist logic
- infrastructure context
- second-order impact reasoning

Tier 2 sources are not normally sufficient by themselves for the `Confirmed Facts` section.

---

## Typical Tier 2 source types

### Domain specialists

Examples:
- energy analysts
- shipping specialists
- sanctions experts
- regional geopolitical researchers
- infrastructure historians
- commodity market specialists

### Reputable industry analysis

Examples:
- sector analysts
- specialist commentary
- structural explainers
- market mapping writeups
- domain-informed research threads

### Expert threads and commentary

This includes:
- high-signal threads on X / Twitter
- specialist explainers
- technical market commentators
- infrastructure-focused researchers

These can be highly valuable when they provide:
- specific variables
- physical system understanding
- credible references
- clear separation between fact and interpretation

---

## What Tier 2 is good for

Tier 2 is especially useful for answering:
- why this event matters
- which physical bottlenecks are critical
- whether backup routes exist
- which listed securities map most directly to the shock
- whether the market is pricing risk premium or direct supply shock
- which second-order sectors are exposed

Examples:
- explaining why a terminal matters more than a field
- showing how VLCC berths constrain exports
- comparing direct beneficiaries vs weak thematic proxies
- identifying whether gold is a hedge or a direct beneficiary
- mapping route disruption into tanker equities or insurers

---

## Tier 2 rule

> Tier 2 informs interpretation, not hard fact anchoring.

Tier 2 should help answer:
- what matters
- what to watch next
- what the market may be pricing
- which names map cleanly

But it should not replace Tier 1 for factual confirmation.

---

## Low-trust / emotional amplifiers

## Definition

These are sources that may generate attention, but do not reliably improve analysis quality.

They often exhibit one or more of the following:
- extreme rhetoric
- certainty without evidence
- viral emotional framing
- collapse narratives without metrics
- commentary disguised as reporting
- selective quoting
- exaggerated causal claims
- no distinction between fact and interpretation

These sources should be:
- downranked
- filtered
- ignored when better evidence exists

---

## Typical warning signs

### Tone-first, evidence-later

Examples:
- "historic collapse"
- "systemic implosion"
- "apocalyptic supply shock"
- "guaranteed oil spike"
- "everything changes now"

without:
- numbers
- boundaries
- timelines
- verifiable sources
- invalidation conditions

### False certainty

Examples:
- absolute claims about damage
- absolute claims about market direction
- absolute claims about strategic outcomes
- definitive claims during early fog-of-war conditions

### Commentary pretending to be reporting

Signs include:
- no attribution
- vague "sources say" phrasing without specificity
- no timestamps
- no source chain
- no way to verify

### Narrative inflation

This happens when a source:
- overgeneralizes from a small fact
- jumps from event to "inevitable global shock"
- presents a speculative tail-risk scenario as base case

---

## Important nuance: strong tone does not automatically mean low quality

A source should **not** be downranked for tone alone if it still provides:
- verifiable variables
- explicit boundaries
- source support
- uncertainty visibility
- fact / interpretation separation

Some experts write forcefully but still provide excellent structural value.

The workflow must filter **hype**, not merely strong style.

---

## How to classify edge cases

## Case 1: Official statement with aggressive rhetoric

Example:
- "We will respond decisively"
- "This attack failed"
- "The facility was unharmed"

Classification:
- Tier 1 for the fact that the statement was made
- **not automatically Tier 1** for the implied market impact or physical result

Use:
- report the statement as a statement
- wait for independent confirmation before upgrading to fact

## Case 2: Reuters article with factual reporting plus interpretation

Classification:
- factual elements can be Tier 1
- interpretive elements belong in Tier 2-style usage

Use:
- separate concrete reporting from analysis paragraphs

## Case 3: Expert thread with excellent infrastructure detail

Classification:
- Tier 2

Use:
- structural mapping
- bottleneck explanation
- scenario interpretation

Do not use it alone to confirm hard facts if those facts are still disputed.

## Case 4: User-provided emotional article

Classification:
- low-trust / emotional unless independently supported

Use:
- say explicitly that the source is emotional, thin, broken, or low-trust
- re-anchor the analysis on independently verified public facts

---

## Fog of War handling

When credible sources disagree on a material fact, the workflow should not force resolution too early.

Examples of disputed facts:
- damage extent
- throughput impairment
- export interruption
- operational downtime
- route access
- recovery timeline

Rule:
- mark the issue as contested
- do not collapse the dispute into a single certainty
- where useful, briefly summarize the competing claims
- state what kind of evidence would resolve the dispute

This is especially important in the first 12–48 hours after major geopolitical events.

---

## How source tiers map into output sections

## Confirmed Facts

Use:
- Tier 1 only

Include:
- concrete facts
- exact dates
- official notices
- documented metrics
- source-level tags

Do not include:
- speculative interpretation
- unofficial extrapolation
- unresolved projection
- emotional language

## Market Interpretation

Use:
- Tier 2 plus fresh verified context
- macro framing
- transmission-path explanation
- infrastructure mapping
- risk-premium vs supply-shock logic

This section can reference Tier 1 facts, but its analytical content is interpretive.

## Scenario Analysis

Use:
- conditional reasoning
- escalation pathways
- uncertainty
- structural dependencies
- market consequence logic

This section should remain explicitly conditional.

---

## Practical checklist for source usage

Before using a source, ask:

### 1. What role is this source playing?
- fact anchor
- structural explainer
- sentiment amplifier
- market mapper

### 2. Can I verify the key claim publicly?
If not:
- do not present it as settled fact
- downgrade confidence
- look for a better anchor

### 3. Is this statement concrete or rhetorical?
If rhetorical:
- report it as rhetoric
- do not convert it into physical impact automatically

### 4. Is the source giving me variables or just emotion?
Variables improve the workflow.  
Emotion without variables usually does not.

### 5. Does this belong in facts, interpretation, or scenarios?
Never mix these casually.

---

## Recommended default behavior

When in doubt:
- prefer Tier 1 for facts
- use Tier 2 for structure and variables
- downrank emotional amplification
- preserve uncertainty
- avoid pretending to know what is not yet knowable

This discipline is more important than sounding certain.

---

## Summary

The source-tiering framework exists to protect analytical integrity.

Its purpose is to ensure that Geo Market Watch does not become:
- a news rewriter
- a hype amplifier
- a certainty generator under uncertainty

Instead, it should function as:
- a disciplined event-research workflow
- a structured market-mapping tool
- a source-aware system that distinguishes fact, interpretation, and scenario
