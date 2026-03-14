---
name: geo-market-watch
description: analyze one or more geopolitical news links and convert them into a chinese market watchlist across us stocks, a-shares, and hong kong stocks. use when the user provides news links about wars, strikes, sanctions, chokepoints, commodity disruptions, shipping shocks, export controls, or other geopolitical events and wants a fixed table, watchlist names, trigger signals, scenario analysis, and short investment commentary rather than generic summarization.
---

Turn geopolitical news links into a reusable three-market investment map.

## Core behavior
- Treat one or more news links as the required starting input.
- If links are missing, explicitly state that full-workflow confidence is reduced, ask for links, and do not pretend the same level of verification was possible.
- Write the final answer in Chinese by default.
- Default goal: transform geopolitical news into a practical investment watchlist, not a generic summary.
- Always separate and label these three layers in the final answer:
  1. [已确认事实 / Confirmed Facts]
  2. [市场解读 / Market Interpretation]
  3. [情景推演 / Scenario Analysis]

## Source authentication and anti-hype filter
Before interpreting the event, classify all user-provided links and web findings into these source tiers:

### Tier 1: ground-truth / factual anchors
Use for [已确认事实 / Confirmed Facts] only.
Typical Tier 1 sources include:
- official government, regulator, military, ministry, or agency statements
- top-tier wire services and primary reporting confirming concrete facts
- public company filings, exchange notices, ETF issuer pages, official route or port authority notices
- official institution data and documented metrics

Important:
- Official rhetoric, threats, adjectives, and strategic messaging are not automatically ground-truth market facts.
- Report them as statements, but do not treat them as confirmed market impact unless independently verified.
- Tier 1 anchors concrete facts only, not interpretations, forecasts, threats, or rhetoric.

### Tier 2: structural analysis / variable interpretation
Use for [市场解读 / Market Interpretation], variable identification, and system mapping.
Typical Tier 2 sources include:
- domain specialists
- reputable industry analysts
- expert threads
- structural explainers that identify infrastructure dependencies, bottlenecks, alternatives, and transmission paths

### Emotional amplifiers / low-trust noise
Actively downrank or ignore sources that:
- use extreme rhetoric without boundary conditions
- make absolute claims without evidence
- confuse commentary with reporting
- rely on viral tone, certainty theater, or unverified extrapolation

Do not downrank a source for strong tone alone if it still provides:
- verifiable variables
- explicit boundaries
- source support
- clear separation between fact and interpretation

If the user-provided link itself is emotional, low-trust, broken, thin, or incomplete:
- explicitly say so
- re-anchor the analysis on independently verified public facts
- preserve the same output structure
- do not mirror the source’s tone

## Market exposure translation
Translate political and military developments into market-relevant variables.
Prefer concrete, quantifiable, and physical mapping, such as:
- export volumes
- share of regional or global supply
- revenue exposure
- specific vessel classes
- terminal capacity
- pipeline dependencies
- backup routes
- refining or processing bottlenecks

## Workflow
Follow these steps in order:
1. Open and understand all user-provided links.
2. Apply the Source Authentication and Anti-Hype Filter.
3. Identify the core event, date, geography, affected assets, and any physical bottlenecks or supply-chain choke points.
4. Verify freshness on the web for the event itself and all time-sensitive market facts.
5. Briefly assess the macro regime in no more than 2 to 3 sentences, focusing only on rate direction, inflation backdrop, and growth sensitivity.
6. Build a scenario tree and name the current base case.
7. Trace the transmission path: event -> commodities / logistics / policy / sentiment -> sectors -> watchlist.
8. Build three style buckets: aggressive, balanced, defensive.
9. For each chosen security, provide why it belongs, one concrete trigger signal, and one concrete invalidation condition.
10. End by formatting the output strictly according to the 9 sections defined in [references/output-template.md](references/output-template.md), concluding with the Short Commentary and Risk Warning.

## Scenario framework
Use this default progression unless a better event-specific framing is clearly superior:
- Scenario A: geopolitical shock, but no confirmed direct damage to critical infrastructure; the market mainly prices risk premium.
- Scenario B: confirmed damage to key commodity, logistics, or production infrastructure; the market shifts toward direct supply-shock pricing.
- Scenario C: prolonged disruption, strategic-route closure, regional escalation, or broad policy spillover; the market shifts toward wider inflation and risk-off repricing.

## Market coverage and asymmetry
- Keep US stocks / ETFs, A-shares, and Hong Kong stocks in scope by default.
- Allocate more depth to the markets with the cleanest transmission path. Do not force equal length across all three markets if impact is clearly asymmetric.

## Web verification and data fallback
Always verify the latest public facts.
If key financial or logistics data is paywalled, delayed, unavailable, or disputed:
- explicitly state: 数据滞后/缺失
- do not fabricate precision
- use alternative public proxies instead

Acceptable public fallback proxies include:
- related shipping or tanker equities relative performance
- sector ETF relative strength
- official route closure or reopening announcements
- issuer-reported ETF holdings
- company filings or management commentary
- major benchmark commodity moves

## Output format
Always follow the exact structure in [references/output-template.md](references/output-template.md).

## Watchlist construction rules
Use [references/watchlist-rules.md](references/watchlist-rules.md) and apply these rules:
- Prefer direct mapping names over fashionable storytelling proxies.
- If the disruption targets a specific node, prefer node-specific proxies when available.
- Target 5 names in each summary when the mapping is clean. Quality overrides count.
- If fewer than 5 high-quality names exist, return only 3 to 4 and explicitly note: （未强行补足）.
- If a popular name is not a clean beneficiary, say so directly.
- If a name functions mainly as a hedge rather than a beneficiary, label it clearly.

## Trigger and invalidation rules
Trigger signals must be specific, observable, near-term, publicly verifiable, and linked to the event.
Invalidation conditions are mandatory. Each name must include at least one specific invalidation condition.
Avoid vague phrases such as:
- sentiment improves
- trend remains strong
- market feels calmer

## Commentary style
- Be concise, structured, and analytical.
- Prefer tables and lists first, then 2 to 4 short paragraphs of commentary.
- Use exact dates when they reduce ambiguity.
- Do not give absolute trading instructions.
- Make uncertainty visible.
- Do not present scenario assumptions as confirmed facts.

## References
- Use [references/output-template.md](references/output-template.md) for the exact section order and headings.
- Use [references/watchlist-rules.md](references/watchlist-rules.md) for basket logic and naming discipline.
- Use [references/sample-prompts.md](references/sample-prompts.md) for example requests and expected behavior.
