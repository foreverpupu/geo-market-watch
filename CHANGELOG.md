# Changelog

All notable changes to **Geo Market Watch** will be documented in this file.

The project evolves through iterative improvements in:
- source authentication
- anti-hype filtering
- fact / interpretation / scenario separation
- fog-of-war handling
- watchlist construction discipline
- trigger and invalidation design

---

## [v5.2.1] - 2026-03-14

### Added
- Added bilingual compatibility labels for key output sections to reduce encoding-related ambiguity in external tools:
 - `[已确认事实 / Confirmed Facts]`
 - `[市场解读 / Market Interpretation]`
 - `[情景推演 / Scenario Analysis]`
- Added README-style validation guidance for manual inspection after packaging.
- Added clearer compatibility wording for disputed facts and missing data labels in public-facing outputs.

### Changed
- Improved output template resilience for copy/paste and cross-platform display.
- Refined user-facing wording around contested facts and data lag handling.
- Made key structural labels more robust for external sharing, screenshots, and reposting.

### Why it matters
This release focuses on packaging reliability and readability across different tools, editors, and display environments, without changing the core analytical workflow.

---

## [v5.2] - 2026-03-14

### Added
- Added **Fog of War Rule**:
 - when a material fact remains disputed across credible sources, explicitly state that it remains contested (`仍存在争议`)
 - do not collapse conflicting reports into a false certainty
- Added stronger handling for disputed damage reports, early conflict claims, and incomplete first-wave reporting.

### Changed
- Strengthened fact-layer discipline in the `Confirmed Facts` section.
- Improved guidance for situations where early official, media, and secondary-source reporting diverge.
- Clarified that unresolved disputes should remain visible rather than being silently harmonized.

### Why it matters
Geopolitical events often emerge under incomplete, conflicting, and politically distorted information conditions. This release improves analytical discipline during fast-moving "fog of war" situations.

---

## [v5.1] - 2026-03-14

### Added
- Added **source-level tags** inside the confirmed-facts section, including:
 - `[官方]`
 - `[通讯社]`
 - `[公司文件]`
 - `[交易所/ETF发行方]`
 - `[官方机构/航运通告]`
- Added clearer separation between:
 - confirmed facts
 - market interpretation
 - scenario analysis
- Added more explicit guidance for handling user-provided low-trust, thin, broken, or emotional links.

### Changed
- Refined **Tier 1 / Tier 2** definitions for stronger execution stability.
- Improved anti-hype filtering so that strong tone alone does not automatically disqualify a source if it still provides:
 - verifiable variables
 - explicit boundaries
 - source support
 - fact / interpretation separation
- Strengthened handling of official rhetoric, threats, and political language so they are not automatically treated as confirmed market impact.
- Improved output structure with clearer source anchoring and more disciplined evidence separation.

### Why it matters
This release makes the workflow more trustworthy and more usable for sharing, discussion, and investment research communication.

---

## [v5.0] - 2026-03-14

### Added
- Introduced **Source Authentication & Anti-Hype Filter**.
- Added source tiering logic:
 - Tier 1: factual anchors
 - Tier 2: structural analysis
 - emotional amplifiers / low-trust noise
- Added **Market Exposure Translation** logic to map geopolitical rhetoric into:
 - export volumes
 - infrastructure bottlenecks
 - vessel classes
 - pipeline dependencies
 - revenue exposure
 - backup routes
- Added stronger requirements for public-data fallback when freight, insurance, or logistics data is unavailable.

### Changed
- Reworked the workflow from "news summary" into a more disciplined event-driven market mapping process.
- Upgraded invalidation logic from optional guidance into a core requirement.
- Improved asymmetrical market-depth handling across US / A-share / Hong Kong markets.
- Refined watchlist construction rules toward more direct and node-specific proxies.

### Why it matters
This was the major turning point where Geo Market Watch evolved from a structured summary tool into a more research-oriented, source-aware market workflow.
