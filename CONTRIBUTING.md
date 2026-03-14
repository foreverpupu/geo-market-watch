# Contributing to Geo Market Watch

Thank you for your interest in contributing to Geo Market Watch.

This project aims to build a structured framework that converts geopolitical
events into actionable market observation signals. Contributions are welcome
from developers, researchers, analysts, and domain experts.

Before contributing, please read the guidelines below to ensure consistency
with the project's methodology and engineering standards.

---

# Project Philosophy

Geo Market Watch is designed around three core principles:

1. **Structured intelligence over narrative commentary**
2. **Event-driven analysis**
3. **Explicit trigger and invalidation logic**

The repository prioritizes:

- reproducible analytical structure
- machine-readable outputs
- clear separation between facts and interpretation
- long-term maintainability

Contributors should preserve these principles when proposing changes.

---

# Types of Contributions

We welcome several categories of contributions.

## 1. Documentation improvements

Examples:

- clarifying methodology explanations
- improving architecture documentation
- expanding the roadmap
- improving examples

Relevant directories:

```
docs/
README.md
```

---

## 2. Schema improvements

The project relies on JSON schemas for structured data contracts.

Schemas are located in:

```
schemas/
```

Current schemas:

- `event-object.json`
- `watchlist-item.json`
- `analysis-output.json`

Possible improvements:

- new optional fields
- better enum definitions
- validation tightening
- schema documentation

**Important:** 
Breaking schema changes should be discussed in an issue before submitting a PR.

---

## 3. Example data improvements

Example payloads demonstrate how schemas are intended to be used.

Location:

```
examples/schema-examples/
```

Examples include:

- event objects
- watchlist items
- full analysis outputs

Example contributions:

- additional scenario cases
- fog-of-war examples
- multi-event examples
- commodity supply disruption cases

---

## 4. Tooling and engineering improvements

Engineering contributions may include:

- validation tooling
- CI improvements
- testing scripts
- workflow automation
- schema validation utilities

Relevant directories:

```
tests/
.github/workflows/
```

---

## 5. Methodology improvements

Changes to the analytical framework should be approached carefully.

Relevant files:

```
SKILL.md
docs/methodology.md
```

Potential contributions:

- improved scenario frameworks
- better propagation logic
- improved trigger design patterns

Major methodological changes should always be discussed in an issue first.

---

# Development Setup

Clone the repository:

```bash
git clone https://github.com/<your-org>/geo-market-watch.git
cd geo-market-watch
```

Install validation dependencies:

```bash
pip install -r tests/schema_validation/requirements.txt
```

Run schema validation:

```bash
python tests/schema_validation/validate_examples.py
```

All validations should pass before submitting a pull request.

---

# Schema Validation

The repository includes automated validation to ensure example data matches
the JSON schema definitions.

Validation checks:
- schema structure integrity
- example JSON correctness
- cross-file `$ref` resolution

Validation script:

```
tests/schema_validation/validate_examples.py
```

Validation must pass locally and in CI.

---

# Pull Request Guidelines

When submitting a PR:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run schema validation
5. Submit a pull request

Branch naming suggestions:

```
feature/<topic>
docs/<topic>
schema/<topic>
tooling/<topic>
```

Example:

```
feature/add-commodity-shock-example
schema/add-policy-node-type
docs/improve-propagation-logic
```

---

# Commit Message Guidelines

Use clear commit messages describing the change.

Recommended format:

```
type: short description
```

Examples:

```
docs: clarify propagation mapping example
schema: add optional commodity_flow node type
tests: add additional validation example
ci: add schema validation workflow
```

Common types:
- `docs`
- `schema`
- `tests`
- `ci`
- `tooling`
- `chore`

---

# Review Expectations

Pull requests will be reviewed based on:
- alignment with project philosophy
- schema consistency
- documentation clarity
- backward compatibility
- engineering quality

Contributors may be asked to revise proposals before merging.

---

# Reporting Issues

If you encounter problems or have improvement ideas, please open an issue.

**Suggested issue categories:**
- schema discussion
- methodology improvement
- tooling bug
- documentation clarification
- feature proposal

**When possible, include:**
- example input
- expected behavior
- current behavior

---

# Code of Conduct

Please maintain a professional and constructive tone when interacting
with other contributors.

Respect different perspectives and focus discussions on improving
the project.

---

# Acknowledgment

Every contribution—whether documentation, schema design, or tooling—helps
improve the robustness of the Geo Market Watch framework.

Thank you for helping build a structured geopolitical intelligence system.
