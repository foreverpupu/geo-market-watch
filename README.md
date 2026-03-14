# Geo Market Watch

Turn geopolitical news links into structured market watchlists across US stocks, A-shares, and Hong Kong stocks.

## Overview

Geo Market Watch is a research-oriented Skill for transforming geopolitical news into structured market watchlists rather than generic summaries.

It separates confirmed facts, market interpretation, and scenario analysis, then maps the event into aggressive, balanced, and defensive watchlists with trigger signals, invalidation conditions, short commentary, and risk warnings.

This project is designed for wars, strikes, sanctions, chokepoints, commodity disruptions, shipping shocks, export controls, and other geopolitical events.

## What problem does it solve?

Geopolitical news is noisy, emotional, and often mixes facts with interpretation.

This Skill helps convert messy news flow into a repeatable market research workflow by:

- separating confirmed facts from interpretation
- filtering low-trust and hype-heavy sources
- handling contested facts during fog-of-war periods
- mapping events into observable market signals
- generating structured watchlists across three markets

## Core capabilities

- Source authentication and anti-hype filtering
- Confirmed facts / market interpretation / scenario separation
- Fog of War handling for contested facts
- Macro-aware event transmission mapping
- Watchlist generation across US / A-share / Hong Kong markets
- Trigger signal and invalidation condition design
- Data fallback when key public data is delayed or unavailable

## Output structure

The Skill produces a structured report with these sections:

1. Event snapshot
2. Confirmed facts
3. Market interpretation
4. Scenario analysis
5. Key indicators to watch
6. Three-market watchlist
7. Aggressive / Balanced / Defensive summaries
8. Short commentary
9. Risk warning

## Design principles

- Facts are not interpretation
- Official rhetoric is not the same as confirmed market impact
- Contested facts must remain contested until resolved
- Data gaps must be acknowledged explicitly
- Quality of mapping matters more than filling lists mechanically

## Example use cases

- Sanctions affecting commodity exports
- Shipping disruptions in strategic chokepoints
- Strikes on energy infrastructure
- Export controls on critical minerals
- Regional escalation affecting logistics and inflation expectations

## How to use

Provide one or more geopolitical news links and ask for a structured Chinese market watchlist.

Example prompt:

> Analyze these links and generate a Chinese market watchlist across US stocks, A-shares, and Hong Kong stocks, including trigger signals, invalidation conditions, short commentary, and risk warning.

## Limitations

- This is a research workflow, not investment advice.
- It depends on public information and may face data lag.
- Some freight, insurance, and logistics data may be unavailable behind paywalls.
- During fog-of-war periods, some facts may remain contested.
- Outputs should be reviewed critically in fast-moving situations.

## Repository structure

- `SKILL.md` — main skill instructions
- `README.md` — project overview
- `examples/` — sample inputs and outputs
- `docs/` — methodology, source tiering, and validation notes
- `CHANGELOG.md` — version history
- `LICENSE.md` — custom non-commercial terms

## Versioning

This project evolves through iterative improvements in:
- source authentication
- anti-hype filtering
- fog-of-war handling
- market mapping discipline
- watchlist construction rules

See `CHANGELOG.md` for details.

## License

This repository is provided under a **Non-Commercial License**. 
You are allowed to use, view, and modify this repository for personal and non-commercial purposes. 
Commercial use, redistribution, and re-packaging are strictly prohibited.

Please see the `LICENSE.md` file for more details.
