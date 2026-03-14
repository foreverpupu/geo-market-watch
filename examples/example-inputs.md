# Example Inputs

This file collects representative prompts and input patterns for **Geo Market Watch**.

The examples are designed to test whether the Skill can correctly handle:
- source authentication
- fact / interpretation / scenario separation
- fog-of-war conditions
- data fallback behavior
- three-market watchlist construction
- trigger and invalidation discipline

---

## How to use these examples

Each example contains:
- an input pattern
- a suggested prompt
- what the test is designed to validate

You can use:
- real links
- placeholder links
- mixed-quality inputs
- multi-link bundles

The goal is not only to see whether the Skill responds, but whether it responds **with the intended discipline**.

---

# Example 1 — Single geopolitical news link

## Input pattern
- one link
- one event
- one primary market shock

## Suggested prompt
Analyze this geopolitical news link and generate a Chinese market watchlist across US stocks, A-shares, and Hong Kong stocks. Separate confirmed facts, market interpretation, and scenario analysis, then provide aggressive, balanced, and defensive watchlists with trigger signals and invalidation conditions.

## What this validates
- basic workflow integrity
- fixed output structure
- three-market coverage
- presence of trigger / invalidation conditions

---

# Example 2 — Multiple links on the same event

## Input pattern
- 2 to 4 links
- same event
- different angles or publishers

## Suggested prompt
Synthesize the following links into one Chinese event-driven market framework. Identify the base case scenario, list confirmed facts, explain the transmission path, and generate a three-market watchlist with aggressive, balanced, and defensive summaries.

## What this validates
- multi-source synthesis
- fact deduplication
- scenario-tree discipline
- consistency across multiple inputs

---

# Example 3 — Low-trust or emotional source input

## Input pattern
- one emotional or sensational article
- possibly mixed with one stronger source

## Suggested prompt
Use these links to build a structured geopolitical market watchlist. If any source is emotional, low-trust, thin, or incomplete, explicitly say so and re-anchor the analysis on independently verified facts.

## What this validates
- anti-hype filtering
- source authentication behavior
- ability to reject tone mirroring
- re-anchoring on higher-quality evidence

---

# Example 4 — Fog-of-war event

## Input pattern
- early breaking event
- conflicting early reports
- damage or closure status unclear

## Suggested prompt
Analyze these links as a fog-of-war situation. Separate what is confirmed from what remains contested, and do not collapse disputed claims into certainty. Then build a Chinese three-market watchlist with scenario analysis and clear invalidation conditions.

## What this validates
- Fog of War Rule
- contested-fact handling
- discipline under uncertainty
- scenario escalation logic

---

# Example 5 — Shipping or chokepoint disruption

## Input pattern
- route disruption
- chokepoint closure risk
- shipping and insurance implications

## Suggested prompt
Analyze these shipping-related geopolitical links and map the event into oil, shipping, logistics, gold, and defense transmission paths. If freight or insurance data is unavailable, explicitly note 数据滞后/缺失 and use public fallback proxies.

## What this validates
- logistics mapping
- data fallback behavior
- handling of missing high-frequency market data
- node-specific market translation

---

# Example 6 — Energy infrastructure strike

## Input pattern
- strike on a terminal, refinery, pipeline, or export node
- possible oil / gas transmission impact

## Suggested prompt
Use these links to assess whether the market is pricing risk premium or direct supply shock. Focus on physical infrastructure, export exposure, and transport bottlenecks, then produce a Chinese three-market watchlist with triggers and invalidation conditions.

## What this validates
- physical bottleneck mapping
- Scenario A vs B distinction
- energy-linked market exposure translation
- direct vs indirect beneficiary selection

---

# Example 7 — Sanctions or export controls

## Input pattern
- sanctions
- export restrictions
- trade controls
- critical mineral restrictions

## Suggested prompt
Analyze these sanctions or export-control links and map them into a Chinese three-market watchlist. Focus on direct beneficiaries, weak thematic proxies, and policy spillover. Keep the output structured and scenario-based.

## What this validates
- policy verification
- direct vs indirect mapping discipline
- cross-market asymmetry
- proxy quality control

---

# Example 8 — Narrow event with limited clean mappings

## Input pattern
- event with only a few direct listed beneficiaries
- many tempting but weak second-order names

## Suggested prompt
Analyze these links and generate aggressive, balanced, and defensive watchlists. Only include direct, liquid, high-quality names. If there are not enough clean names, return fewer and explicitly note （未强行补足）.

## What this validates
- non-padding rule
- watchlist quality discipline
- direct mapping preference
- ability to resist weak thematic expansion

---

# Example 9 — Macro-sensitive geopolitical shock

## Input pattern
- geopolitical event
- inflation-sensitive market backdrop
- possible growth / rate implications

## Suggested prompt
Analyze these links and briefly assess the macro regime in no more than 2 to 3 sentences. Then explain how the current macro backdrop changes the market impact of this geopolitical shock before generating the three-market watchlist.

## What this validates
- macro regime integration
- concise macro framing
- event transmission under different market backdrops
- discipline against turning the output into a macro essay

---

# Example 10 — Asymmetric market mapping

## Input pattern
- event clearly maps more cleanly into one market than the others

## Suggested prompt
Analyze these links and keep US stocks, A-shares, and Hong Kong stocks in scope by default, but allocate more depth to the markets with the cleanest transmission path. Do not force equal detail if the mapping is clearly asymmetric.

## What this validates
- asymmetry rule
- regional market prioritization
- avoidance of forced equal-length coverage
- cleaner market-specific outputs

---

# Short-form test prompts

Use these when you want a faster smoke test.

## Prompt A
Analyze this geopolitical news link and generate a Chinese three-market watchlist with confirmed facts, market interpretation, scenario analysis, and trigger/invalidation rules.

## Prompt B
Synthesize these links into a Chinese market watchlist. Handle source quality carefully and preserve contested facts if the event is still under fog-of-war conditions.

## Prompt C
Analyze these links with anti-hype filtering. If key logistics or insurance data is unavailable, write 数据滞后/缺失 and use public fallback proxies.

## Prompt D
Generate aggressive, balanced, and defensive watchlists from these links. Prefer direct mapping names and avoid weak thematic padding.

---

# Recommended test matrix

To validate the Skill thoroughly, test with at least one input from each category:
- single-link basic event
- multi-link synthesis
- fog-of-war contested event
- shipping/chokepoint disruption
- sanctions/export-control case
- narrow thematic case with limited listed mappings
- asymmetric market-impact case

---

# Notes for maintainers

When testing new versions of the Skill:
- keep at least one real-world example per major event type
- include at least one weak or emotional source case
- include at least one early-dispute / fog-of-war case
- include at least one case where public data is incomplete
- verify that watchlists still include invalidation conditions

A version is not fully validated until both:
- structural output remains correct
- behavioral discipline remains intact
