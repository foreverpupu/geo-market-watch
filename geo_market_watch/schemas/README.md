# Geo Market Watch Schemas

This directory contains the core JSON Schemas for Geo Market Watch v6.

These schemas define the structured data contract for the system so that
events, analyses, and watchlists can be produced consistently across agents,
workflows, and integrations.

---

## Why schemas exist

Geo Market Watch began as a structured prompt and analysis framework.
As the project evolves toward a multi-agent intelligence system, it needs a
stable machine-readable contract.

The schemas in this directory help the project:

- normalize inputs from different sources
- enforce consistent output structure
- reduce format drift across agents
- support automation workflows
- support validation and regression testing
- make downstream integrations easier

---

## Schema files

### `event-object.json`

Defines the normalized event object used as the canonical input to the
analysis pipeline.

This schema is designed to represent a geopolitical or macro-relevant event
after source collection and normalization.

Typical fields include:

- event ID
- timestamps
- event type
- status
- source tier
- confidence
- geographies
- actors
- sources
- contradictions
- market domains

Use this schema whenever raw inputs such as links, articles, feed items, or
manual notes are converted into a structured event representation.

---

### `watchlist-item.json`

Defines the structured output for a single watchlist item.

This is one of the most important schemas in the project because it translates
geopolitical analysis into a market observation target.

Typical fields include:

- originating event ID
- ticker or asset
- market
- directional bias
- thesis
- physical mapping node
- trigger signals
- invalidation conditions
- time horizon
- confidence

Use this schema whenever an event is mapped to a tradable asset, basket,
sector, or monitoring target.

---

### `analysis-output.json`

Defines the top-level structured output for a deep analysis run.

It combines:

- event object
- confirmed facts
- market interpretation
- scenario analysis
- watchlist items
- risk flags
- propagation chain
- next monitoring points
- metadata

Use this schema as the main machine-readable analysis artifact for storage,
APIs, workflow handoffs, dashboards, and audits.

---

## Relationship between schemas

The three schemas are designed to work together.

### Flow

```
Raw input 
→ event-object.json 
→ analysis process 
→ analysis-output.json 
→ embedded watchlist-item.json
```

### In plain language

- **event-object.json** defines what happened
- **watchlist-item.json** defines what to monitor or trade
- **analysis-output.json** defines the full analytical conclusion

---

## Validation philosophy

The schemas are intentionally strict on the fields that matter most to the
Geo Market Watch methodology.

Examples:

- events must have status, confidence, actors, geographies, and sources
- watchlist items must have trigger and invalidation logic
- deep analysis outputs must include confirmed facts, interpretation,
  scenario analysis, and watchlist content

At the same time, the schemas leave room for future extension through
optional metadata and descriptive fields.

---

## Versioning guidance

When changing any schema:

1. Update the schema version in project documentation.
2. Revalidate all example JSON files.
3. Check whether downstream tools or agents depend on the old contract.
4. Document breaking changes clearly in the changelog.

Recommended convention:

- additive non-breaking field additions → minor version bump
- required field changes or enum changes → major version bump

---

## Example files

Example payloads are provided in:

`examples/schema-examples/`

These sample files are intended to:

- demonstrate expected structure
- support schema validation tests
- help contributors understand intended usage

Current examples:

- `event-object.sample.json`
- `watchlist-item.sample.json`
- `analysis-output.sample.json`

---

## Recommended next step

The next engineering step is to add automated validation tests.

Suggested structure:

- `tests/schema_validation/`
- a lightweight validation script
- CI checks against all sample payloads

This ensures schema evolution remains safe and predictable.
