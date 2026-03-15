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

### 1. Separate fact from interpretation
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

### 2. Use source hierarchy as a control system
The project is built on the idea that **not all sources should enter the same layer of analysis**.

A strong workflow should know:

- which sources can anchor facts
- which sources can help explain structure
- which sources should be downranked or ignored

This led to the Tier 1 / Tier 2 / low-trust distinction.

#### Why this matters
In geopolitical events, the error is often not "the model can't reason." 
The error is that the model reasons on top of contaminated inputs.

The source hierarchy is a form of **input risk control**.

It exists to prevent:
- official rhetoric from becoming "market facts"
- emotional headlines from driving interpretation
- high-tone commentary from leaking into the fact layer

---

### 3. Reward variables, not drama
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

### 4. Preserve uncertainty when uncertainty is real
Large language models tend to be rewarded for smoothness and decisiveness.

That is useful in many tasks, but dangerous in early-stage geopolitical events.

In these situations:
- facilities may or may not be damaged
- throughput may or may not be interrupted
- official narratives may conflict
- satellite confirmation may lag
- shipping behavior may reflect fear before facts are settled

A bad system collapses that ambiguity into false certainty.

Geo Market Watch was explicitly designed to do the opposite:
- keep contested facts contested
- make uncertainty visible
- separate unresolved claims from confirmed facts

This principle eventually became formalized as the **Fog of War Rule**.

---

### 5. A watchlist is only useful if it can fail
Many generated watchlists look plausible because they tell a coherent story.

But without:
- trigger signals
- invalidation conditions
- quality control on name selection

they are not disciplined research outputs.

This is why the project eventually made invalidation **mandatory**.

The key idea is simple:

> A useful market mapping must say not only why a name belongs, but also what would break the logic.

This keeps the output closer to research discipline and farther from narrative accumulation.

---

### 6. Design for automation, not just conversation
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

## Why the project evolved in stages

The framework did not begin in its current form. 
Its current structure is the result of repeated attempts to solve specific failure modes.

### Stage 1: From "news summary" to "market mapping"
The earliest version of the project focused mainly on:

- reading links
- identifying the event
- producing a market-oriented summary

This was useful, but not robust.

The weakness was that summary alone does not create a repeatable investment framework.

That led to the addition of:

- fixed output structure
- three-market mapping
- grouped watchlists
- trigger signals

This shift marked the transition from "summary tool" to "watchlist framework."

---

### Stage 2: From watchlist generation to research discipline
Once watchlists became central, new problems emerged:

- weak thematic names were being included
- direct and indirect beneficiaries were not separated clearly enough
- invalidation logic was often too vague
- scenario thinking was underdeveloped

This led to:
- more disciplined watchlist construction
- node-specific targeting
- stronger physical bottleneck logic
- mandatory invalidation conditions

This stage moved the framework toward **structured event research**.

---

### Stage 3: From structure to source integrity
The next major issue was not output formatting, but source contamination.

Even with a strong output structure, the workflow could still drift if the input stream included:

- emotional articles
- low-trust commentary
- viral narratives
- unverified extrapolation
- rhetoric disguised as confirmed fact

This led to one of the most important architectural upgrades:

- **Source Authentication**
- **Anti-Hype Filter**
- **Tier 1 / Tier 2 separation**
- **source-level tags in confirmed facts**

This stage was critical because it moved the project upstream:
from "better formatting" to **better evidence handling**.

---

### Stage 4: Formalizing uncertainty with Fog of War
The next recurring failure mode appeared during fast-moving conflict events.

In those cases:
- early reports conflicted
- damages were unclear
- throughput effects were disputed
- political narratives competed before technical evidence stabilized

The model needed a way to avoid premature closure.

That led to the integration of the **Fog of War Rule**:
- contested facts remain contested
- disagreement is surfaced explicitly
- uncertainty is preserved until resolved

This was one of the most important methodological upgrades in the entire project.

---

### Stage 5: Reliability, compatibility, and repository maturity
Once the methodology had matured, another layer of work became important:

- packaging stability
- documentation clarity
- encoding compatibility
- output-template consistency
- repository structure
- validation checklists

This led to:
- bilingual label compatibility
- output-template synchronization
- stronger validation docs
- examples
- repository-facing documentation

This stage moved the project from "strong internal workflow" toward "shareable public framework."

---

## Why three markets?

The project uses a default three-market structure:

- US stocks / ETFs
- A-shares
- Hong Kong stocks

This is not cosmetic. 
It exists because geopolitical shocks often travel through different listed expressions in different markets.

### Why not only US markets?
Because some of the cleanest public-market mappings for Asian energy, shipping, or gold exposure may sit in Hong Kong or mainland China-linked equities.

### Why not only A-shares / Hong Kong?
Because the US market often offers:
- the cleanest ETF baskets
- the most liquid global commodity exposures
- broader hedging and sector expression

The point is not equal treatment. 
The point is **coverage with asymmetry**.

That is why the framework says:
- keep all three markets in scope by default
- allocate more depth where the transmission path is cleanest

---

## Why output structure matters

The structured output format is not just for presentation quality.

Each section performs a control function.

### Event snapshot
Prevents the analysis from jumping straight into asset opinions without defining the event.

### Confirmed facts
Protects the evidence layer from narrative contamination.

### Market interpretation
Creates a separate space for actual analytical reasoning.

### Scenario analysis
Prevents the model from presenting one path as inevitable.

### Key indicators
Turns abstract interpretation into observable follow-up items.

### Three-market watchlist
Forces the event-to-asset mapping to become concrete.

### Group summaries
Improves usability for fast readers and discussion contexts.

### Short commentary
Allows synthesis and prioritization.

### Risk warning
Preserves humility, boundaries, and explicit non-advisory framing.

In short:

> The structure is a risk-control device, not just a formatting template.

---

## Why the project uses trigger signals and invalidation conditions

The project requires both because each solves a different problem.

### Trigger signals answer:
- What would confirm that this mapping is becoming more relevant?

### Invalidation conditions answer:
- What would break this thesis?

Without trigger signals, the watchlist becomes vague. 
Without invalidation conditions, the watchlist becomes sticky and self-justifying.

Together, they make the output testable.

---

## Why data fallback is explicit

Geopolitical event analysis often reaches for data that is:

- too specialized
- delayed
- paywalled
- unavailable publicly

Examples include:
- war-risk insurance premiums
- spot freight
- certain logistics quotes
- niche infrastructure throughput estimates

Many models react badly to these gaps. 
They either:
- fabricate precision
- overstate stale information
- imply real-time access that does not exist

Geo Market Watch treats this explicitly.

When the data is unavailable, the workflow must:
- say `数据滞后/缺失`
- avoid fake precision
- use public fallback proxies instead

This is not a cosmetic warning. 
It is a design defense against hallucinated market detail.

---

## Why anti-hype matters beyond tone

The anti-hype filter is not about punishing strong writing style.

A source may sound intense and still be useful.

What matters is whether it provides:
- variables
- evidence
- boundaries
- separable fact and interpretation

So the filter is not:
- "ignore dramatic tone"

It is:
- "ignore unsupported certainty and emotional amplification"

This distinction is important because many good experts write forcefully. 
The framework is designed to filter hype, not personality.

---

## Why the repository includes documentation beyond the skill itself

The project includes:

- methodology notes
- source-tiering guidance
- validation checklist
- examples
- scheduled monitoring guidance
- changelog and design notes

This was intentional.

The Skill itself tells the model what to do. 
The repository docs tell humans:

- why it was designed this way
- how to validate it
- how to use it safely
- how to extend it without breaking its logic

In other words:

> `SKILL.md` is the control surface for the model. 
> `docs/` is the control surface for the human maintainer.

---

## Why the project is not positioned as a trading engine

Geo Market Watch is deliberately positioned as a:

- research workflow
- event-monitoring framework
- market-mapping tool

and **not** as:
- an automated trading system
- a signal engine
- investment advice
- a profit promise

This is both a practical and philosophical choice.

Practically:
- public information can be delayed
- conflict facts can remain unresolved
- mapping quality depends on context
- outputs still require judgment

Philosophically:
- the value of the framework is discipline, not certainty
- the framework is designed to reduce analytical sloppiness, not eliminate risk

---

## What "good use" looks like

The framework is being used well when it helps the user:

- identify what is actually confirmed
- understand which variable matters most
- distinguish risk premium from direct supply shock
- map the event into better watchlists
- monitor what would escalate or invalidate the thesis
- avoid reacting to emotional narratives

It is being used poorly when it is treated as:

- an oracle
- a substitute for judgment
- a one-click truth machine
- a way to produce stronger opinions than the evidence supports

---

## Future evolution

Future improvements should continue to follow the same philosophy:

- strengthen evidence quality
- preserve uncertainty honestly
- improve asset-mapping precision
- improve repository usability
- avoid marketing inflation
- keep the system useful under real-world ambiguity

A good future version should not merely sound smarter. 
It should behave more carefully.

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

## Final note

Geo Market Watch exists because geopolitical market analysis is one of the easiest places for models and humans alike to become overconfident.

This framework was designed to push in the opposite direction:

- more structure
- more evidence discipline
- more explicit uncertainty
- better mapping
- fewer false certainties

That is the design philosophy behind the project.
