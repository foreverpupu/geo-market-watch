# Validation Checklist

## Purpose

This checklist is used to verify that **Geo Market Watch** still behaves as intended after:
- prompt edits
- packaging changes
- repository restructuring
- copy/paste into external tools
- cross-platform display
- version upgrades

The goal is not only to confirm that the Skill still loads, but also that its **analytical discipline** remains intact.

A valid build should preserve:
- source tiering
- anti-hype filtering
- fact / interpretation / scenario separation
- fog-of-war handling
- data fallback behavior
- watchlist trigger / invalidation discipline
- risk warning output

---

## Validation layers

Validation should happen at three levels:
1. **File integrity**
2. **Instruction integrity**
3. **Behavior integrity**

A Skill can pass file checks but still fail behavior checks.  
All three layers matter.

---

# 1. File Integrity Checklist

These checks confirm that the package structure and key files are present and readable.

## Required files

Confirm that the package contains at least:
- `SKILL.md`
- `agents/openai.yaml`

Recommended additional files:
- `README.md`
- `CHANGELOG.md`
- `docs/methodology.md`
- `docs/source-tiering.md`
- `docs/validation-checklist.md`
- `examples/example-inputs.md`
- `examples/example-output.md`

If `SKILL.md` or `agents/openai.yaml` is missing, the package should be treated as invalid.

---

## Encoding and readability

Open `SKILL.md` and confirm the key labels display correctly.

Check for these exact phrases:
- `[已确认事实 / Confirmed Facts]`
- `[市场解读 / Market Interpretation]`
- `[情景推演 / Scenario Analysis]`

If these appear corrupted, replaced by garbled characters, or visibly broken, the file may have encoding problems.

Also scan for obvious mojibake or suspicious characters such as:
- `Ã`
- `â`
- `ð`
- `å`
- `æ`
- replacement diamonds
- question-mark boxes
- broken CJK characters

A small isolated artifact may be tolerable in a non-critical comment, but widespread corruption should fail validation.

---

## YAML frontmatter

At the top of `SKILL.md`, confirm the frontmatter is present and valid:

```yaml
---
name: geo-market-watch-v5-2
description: ...
---
```

Check that:
- opening --- exists
- closing --- exists
- name exists
- description exists
- name remains lowercase and hyphenated
- description is lowercase as required by the skill validator

If the frontmatter is malformed, validation should fail.

## Structural presence

Search SKILL.md for these critical sections:
- ## Core behavior
- ## Source authentication and anti-hype filter
- ## Workflow
- ## Scenario framework
- ## Market coverage and asymmetry
- ## Web verification and data fallback
- ## Output structure
- ## Watchlist construction rules
- ## Trigger and invalidation rules

If one or more of these sections are missing, the build should be reviewed manually.

## Reference linkage

Confirm that SKILL.md still correctly references any external instruction files, especially if the workflow points to them.

Typical examples to verify:
- references/output-template.md
- any linked docs under references/
- any linked files under docs/ if used

If the main workflow references a file that does not exist, validation should fail.

# 2. Instruction Integrity Checklist

These checks confirm that the core methodology has not been lost during editing.

## Core logic presence

Search for the following concepts and confirm they are still explicitly present:
- Tier 1
- Tier 2
- Fog of War Rule
- 数据滞后/缺失
- Invalidation conditions are mandatory
- （未强行补足）
- Risk Warning
- risk warning

If any of these are missing, the current build may no longer match the intended workflow.

## Fact / interpretation / scenario separation

Confirm that the output structure still separates:
- Confirmed Facts
- Market Interpretation
- Scenario Analysis

A build should fail conceptual validation if these layers are merged or blurred together.

The build should also clearly distinguish:
- what is confirmed
- what is interpreted
- what is conditional / scenario-based

## Anti-hype discipline

Confirm that the instructions still contain explicit rules for:
- downranking emotional amplifiers
- not treating rhetoric as market fact
- re-anchoring analysis on independently verified facts if the input source is weak
- avoiding tone mirroring when the source is sensational

If this is missing, the workflow is more likely to drift into noisy or hype-driven output.

## Fog-of-war handling

Confirm that the instructions explicitly say contested facts should remain contested.

The build should include logic equivalent to:
- when credible sources disagree on a material fact, state that it remains contested
- do not collapse disputed claims into false certainty
- where useful, summarize competing claims briefly
- where useful, state what evidence would resolve the dispute

If this logic is absent, conflict-period behavior becomes much less reliable.

## Data fallback discipline

Confirm that the instructions still explicitly require:
- writing 数据滞后/缺失 when key public data is unavailable
- avoiding fabricated precision
- using fallback public proxies instead

Recommended proxy types include:
- related shipping or tanker equities relative performance
- sector ETF relative strength
- official route closure or reopening announcements
- issuer-reported ETF holdings
- company filings or management commentary
- major benchmark commodity moves

If this section disappears, the workflow is more vulnerable to hallucinated logistics, insurance, or throughput details.

## Watchlist discipline

Confirm that the instructions still explicitly require:
- direct mapping over weak thematic storytelling
- trigger signals
- invalidation conditions
- quality over quantity when watchlist names are insufficient
- hedge vs beneficiary labeling when relevant

If the Skill can generate lists without invalidation logic, analytical quality has degraded.

## Output completeness discipline

Confirm that the workflow and the output template are logically aligned.

The build should produce all required sections:
- Event snapshot
- Confirmed facts
- Market interpretation
- Scenario analysis
- Key indicators to watch
- Three-market watchlist
- Aggressive / Balanced / Defensive summaries
- Short commentary
- Risk warning

If the workflow says "end with short commentary" but the output template requires a final Risk Warning, that mismatch should be treated as a bug and corrected.

# 3. Behavior Integrity Checklist

These checks validate actual output behavior, not just file content.

Use at least one real geopolitical news link and test the Skill.

A good validation case should contain one or more of the following:
- incomplete early reporting
- market-sensitive exposure
- possible logistics implications
- possible conflict between facts and rhetoric
- unclear infrastructure damage
- possible need for fallback data

## Behavior test A: basic structured output

**Prompt**
Provide one geopolitical news link and ask for a structured three-market watchlist.

**Pass criteria**
The output should include:
- Event snapshot
- Confirmed facts
- Market interpretation
- Scenario analysis
- Key indicators
- Three-market watchlist
- Aggressive / Balanced / Defensive summaries
- Short commentary
- Risk warning

If major sections are missing, behavior validation fails.

## Behavior test B: fact-layer discipline

**Prompt**
Use a link containing political rhetoric or strong public statements.

**Pass criteria**
The output should:
- report the statement as a statement
- avoid converting rhetoric directly into confirmed market impact
- keep the fact layer anchored to concrete evidence

**Example failure**
A statement like:
"A leader threatened closure of a route"
gets rewritten as:
"The route is effectively closed"
without independent confirmation.

## Behavior test C: fog-of-war discipline

**Prompt**
Use an event where early reporting conflicts across credible sources.

**Pass criteria**
The output should:
- explicitly indicate that the fact remains contested
- avoid forcing certainty
- separate disputed facts from confirmed facts
- keep scenario logic conditional

**Example failure**
One early damage claim is chosen as truth without acknowledging credible disagreement.

## Behavior test D: data fallback discipline

**Prompt**
Use an event where freight, insurance, or specialized logistics data is unlikely to be fully public.

**Pass criteria**
The output should:
- explicitly write 数据滞后/缺失 if necessary
- avoid fake precision
- use reasonable public proxies instead

**Example failure**
The model invents exact freight or insurance numbers without public sourcing.

## Behavior test E: watchlist discipline

**Prompt**
Use a narrow event where only a few strong market mappings exist.

**Pass criteria**
The output should:
- avoid padding weak names
- return fewer names if necessary
- explicitly note （未强行补足） when relevant
- provide triggers and invalidation conditions for every listed name

**Example failure**
Weak thematic names are added only to fill list length.

## Behavior test F: asymmetry discipline

**Prompt**
Use an event that maps much more clearly to one market than the others.

**Pass criteria**
The output should:
- still keep three-market scope by default
- allocate more depth to the market with the cleanest transmission path
- avoid artificial equal-length treatment

**Example failure**
Each market gets identical treatment even when the mapping is obviously asymmetric.

## Behavior test G: risk warning presence

**Prompt**
Use any real event link and request the full structured output.

**Pass criteria**
The output should end with a distinct Risk Warning section or equivalent final risk note.

The risk warning should remind the reader that:
- this is a research workflow, not investment advice
- data may be incomplete or lagged
- contested facts may remain unresolved
- outputs should be reviewed critically

**Example failure**
The response ends after short commentary and omits the final risk-warning layer entirely.

# Quick acceptance checklist

Use this fast checklist when you only have 1 minute.

A build is likely usable if all of the following are true:
- SKILL.md exists
- agents/openai.yaml exists
- no major encoding corruption is visible
- YAML frontmatter is valid
- Tier 1, Tier 2, and Fog of War Rule are present
- 数据滞后/缺失 is present
- confirmed facts / interpretation / scenarios remain separated
- invalidation conditions are still mandatory
- risk warning is still required
- at least one real test output behaves as expected

# Red flags that should trigger rework

Treat the build as degraded if you observe any of the following:
- garbled encoding in key labels
- malformed YAML frontmatter
- missing fact / interpretation / scenario split
- loss of anti-hype rules
- disappearance of fog-of-war handling
- disappearance of data fallback logic
- outputs with no invalidation conditions
- outputs that treat rhetoric as hard fact
- outputs that fabricate unavailable logistics precision
- outputs that pad watchlists with weak names mechanically
- outputs that omit the final risk warning
- broken references between SKILL.md and template files

# Recommended test cases

Use a mix of the following when validating future versions:

## Case type 1: energy infrastructure strike
Good for testing:
- physical node mapping
- supply-shock logic
- oil / shipping / gold / defense spillover

## Case type 2: shipping route disruption
Good for testing:
- route status
- tanker proxies
- fallback data logic
- logistics spillover

## Case type 3: sanctions or export controls
Good for testing:
- policy verification
- direct vs indirect beneficiaries
- cross-market asymmetry

## Case type 4: contested early conflict reporting
Good for testing:
- fog-of-war handling
- fact-layer discipline
- source tiering

## Case type 5: narrow thematic event
Good for testing:
- watchlist quality control
- non-padding rule
- direct mapping discipline

## Case type 6: sensational low-trust source
Good for testing:
- anti-hype filtering
- re-anchoring on higher-quality facts
- refusal to mirror exaggerated tone

# Maintenance guidance

After each meaningful update:
- run the file integrity checks
- run at least one real-world behavior test
- verify that contested facts remain visible
- verify that invalidation conditions still appear consistently
- verify that the final risk warning still appears
- record the update in CHANGELOG.md

Do not assume a structurally valid file is behaviorally valid.

# Summary

A valid Geo Market Watch build should not only load correctly.
It should still behave like a disciplined geopolitical market workflow.

That means it should:
- respect source hierarchy
- preserve uncertainty when uncertainty is real
- refuse to fabricate unavailable precision
- maintain explicit watchlist discipline
- keep risk warnings visible
- remain useful for repeatable market observation

Passing validation means the Skill still behaves like a research tool, not a hype amplifier.
