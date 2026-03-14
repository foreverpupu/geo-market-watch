# Schema Validation

This directory contains the validation tooling for the Geo Market Watch v6
JSON Schemas and sample payloads.

The goal is to ensure that:

- schemas remain internally consistent
- local `$ref` references resolve correctly
- sample JSON payloads remain valid
- future schema changes do not silently break examples

---

## Files

- `validate_examples.py` — validates example JSON files against the schemas
- `requirements.txt` — Python dependencies required for validation

---

## What gets validated

The validation script checks the following files:

### Schemas
- `schemas/event-object.json`
- `schemas/watchlist-item.json`
- `schemas/analysis-output.json`

### Example payloads
- `examples/schema-examples/event-object.sample.json`
- `examples/schema-examples/watchlist-item.sample.json`
- `examples/schema-examples/analysis-output.sample.json`

---

## Prerequisites

Use Python 3.10+ recommended.

Install dependencies:

```bash
pip install -r tests/schema_validation/requirements.txt
```

---

## Run validation locally

From the repository root:

```bash
python tests/schema_validation/validate_examples.py
```

Expected output:

```
Geo Market Watch Schema Validation
========================================

Validating: examples/schema-examples/event-object.sample.json
Against:    schemas/event-object.json
[PASS]

Validating: examples/schema-examples/watchlist-item.sample.json
Against:    schemas/watchlist-item.json
[PASS]

Validating: examples/schema-examples/analysis-output.sample.json
Against:    schemas/analysis-output.json
[PASS]

========================================
Passed: 3/3
Failed: 0/3
```

---

## Failure behavior

If any example fails validation:
- the script prints the failing file
- the failing JSON path is shown
- a human-readable error message is printed
- the script exits with a non-zero exit code

This makes it suitable for CI usage.

---

## Validation philosophy

Geo Market Watch uses schemas to protect the most important structural
guarantees of the methodology.

Examples:
- event objects must include actors, geographies, sources, and confidence
- watchlist items must include trigger and invalidation logic
- analysis outputs must include confirmed facts, interpretation, scenarios,
  and watchlist content

The schemas are designed to be strict enough to catch structural drift,
while still allowing the project to evolve over time.

---

## When to run validation

Run validation whenever you change any of the following:
- files in schemas/
- files in examples/schema-examples/
- output contracts in SKILL.md
- agent output structure
- enum values or required fields

---

## Recommended contributor workflow

1. Update the schema.
2. Update example JSON files if needed.
3. Run local validation.
4. Confirm that all examples pass.
5. Document breaking changes in CHANGELOG.md if applicable.

---

## CI integration

This repository can run schema validation automatically through GitHub Actions.

Recommended workflow file:
- `.github/workflows/schema-validation.yml`

This ensures every push and pull request validates the schema examples.

---

## Future improvements

Recommended next enhancements:
- add negative/failure test cases
- validate more scenario examples
- add regression snapshots for agent outputs
- add schema version assertions
- enforce validation in pull request checks
