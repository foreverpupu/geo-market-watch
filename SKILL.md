---
name: geo-market-watch
description: analyze geopolitical market shocks from either user-provided links or proactive web discovery, then convert them into a chinese market watchlist across us stocks, a-shares, and hong kong stocks. use when the user provides news links about wars, strikes, sanctions, chokepoints, commodity disruptions, shipping shocks, export controls, or other geopolitical events, or when chatgpt is asked to monitor, scan, surface, triage, or periodically discover important geopolitical developments that may matter for markets and then produce a fixed table, watchlist names, trigger signals, scenario analysis, and short investment commentary rather than generic summarization.
---

Turn geopolitical developments into a reusable three-market investment map.

## Core behavior
- Support two input modes:
  1. **Link mode**: the user provides one or more news links.
  2. **Discovery mode**: ChatGPT is explicitly asked to monitor, scan, triage, or periodically surface important geopolitical events for market relevance.
- In Link mode, open and assess the user links first.
- In Discovery mode, do not wait for user-provided links. Search the web, identify candidate events, rank them, and only then run the full market-watch workflow on the highest-priority event(s).
- Write the final answer in Chinese by default.
- When mentioning important entities in Chinese output, use bilingual naming on first mention: 中文名（English name） for places, people, institutions, ports, straits, companies, commodities infrastructure, and securities when helpful for disambiguation.
- Default goal: transform geopolitical developments into a practical investment watchlist, not a generic summary.
- Always separate and label these three layers in the final answer:
  1. [已确认事实 / Confirmed Facts]
  2. [市场解读 / Market Interpretation]
  3. [情景推演 / Scenario Analysis]

## Discovery mode rules
Use [references/discovery-rules.md](references/discovery-rules.md).

In Discovery mode, first decide whether an event is important enough to escalate into the full workflow. Prefer events that are:
- fresh
- cross-verified
- physically consequential
- tied to identifiable commodities, logistics, export controls, infrastructure, sanctions, mobilization, or strategic chokepoints
- likely to change risk premium, supply expectations, or sector leadership within days to weeks

If no event clears the threshold:
- explicitly say that no item currently warrants a full watchlist refresh
- still provide a short monitor list of 3 to 5 developing situations and what would make them actionable
- do not force a full 9-section report for weak signals

If several events clear the threshold:
- rank them by market relevance first, not media volume
- either
  - produce one full report for the top event and a short ranked monitor list for the rest, or
  - produce a compact multi-event dashboard only if the user explicitly asks for a sweep

### Scheduled Monitoring / Scout Prompt
For automated scheduled monitoring (e.g., daily morning scan), use the Scout Prompt in [agents/scout-prompt.txt](agents/scout-prompt.txt) or see [docs/scheduled-monitoring.md](docs/scheduled-monitoring.md).

The Scout Prompt is designed for:
- **Strict execution limits**: max 3 web_search calls, 5-minute timeout
- **Focused scanning**: only Reuters, Bloomberg, and mainstream financial sources
- **Four main tracks**: energy disruption, shipping crisis, metal sanctions, East Asia supply chain
- **Dual-mode output**: either upgrade recommendation card OR monitoring watchlist
- **Bilingual naming**: 中文名（English name） for key entities

Use Scout Prompt for cron jobs, ChatGPT Tasks, Make.com, Coze, or other automation platforms.

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
1. Determine whether the request is Link mode or Discovery mode.
2. In Link mode, open and understand all user-provided links.
3. In Discovery mode, scan for candidate events, score them with [references/discovery-rules.md](references/discovery-rules.md), and select the best escalation target.
4. Apply the Source Authentication and Anti-Hype Filter.
5. Identify the core event, date, geography, affected assets, and any physical bottlenecks or supply-chain choke points.
6. Verify freshness on the web for the event itself and all time-sensitive market facts.
7. Briefly assess the macro regime in no more than 2 to 3 sentences, focusing only on rate direction, inflation backdrop, and growth sensitivity.
8. Build a scenario tree and name the current base case.
9. Trace the transmission path: event -> commodities / logistics / policy / sentiment -> sectors -> watchlist.
10. Build three style buckets: aggressive, balanced, defensive.
11. For each chosen security, provide why it belongs, one concrete trigger signal, and one concrete invalidation condition.
12. End by formatting the output strictly according to the 9 sections defined in [references/output-template.md](references/output-template.md), concluding with the Short Commentary and Risk Warning.

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
- Keep entity naming consistent after first mention. After 中文名（English name） appears once, later references may use the Chinese short form if there is no ambiguity.
- Make uncertainty visible.
- Do not give absolute trading instructions.
- Do not present scenario assumptions as confirmed facts.

## References
- Use [references/output-template.md](references/output-template.md) for the exact section order and headings.
- Use [references/watchlist-rules.md](references/watchlist-rules.md) for basket logic and naming discipline.
- Use [references/discovery-rules.md](references/discovery-rules.md) for proactive scanning, event scoring, and escalation thresholds.
- Use [references/sample-prompts.md](references/sample-prompts.md) for example requests and expected behavior.
- Use [docs/scheduled-monitoring.md](docs/scheduled-monitoring.md) for automated scheduled monitoring setup and Scout Prompt configuration.
