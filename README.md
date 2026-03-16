# News Pipeline Agents

Geopolitical news analysis pipeline with multi-agent orchestration.

## Architecture / The Engine

`geo-market-watch` is a local-first, deterministic, auditable intelligence workflow for turning geopolitical developments into structured market decisions.

### Core Pipeline

> **Raw Event → Normalization → Scoring → Trigger → Review → Performance Tracking**

This pipeline reflects a deliberate shift away from black-box prediction and toward an auditable workflow. The goal is not merely to produce an output, but to preserve the full judgment trail behind it. Events are normalized, scored, escalated, reviewed, and tracked through an explicit process. Language models are not autonomous decision-makers in this system; they operate within a structured workflow that retains human oversight at critical points.

### Key Design Principles

- **Local-first**: data, state, and research artifacts remain inspectable and under operator control.
- **Deterministic where it matters**: core pipeline stages are designed for reproducible evaluation, testing, and benchmarking.
- **Auditable by default**: every important judgment should be traceable, inspectable, and reviewable.
- **Human-in-the-loop**: analyst review remains part of the decision process for material actions.
- **Composable**: the package is designed so individual layers can be used independently without forcing the full workflow.

### Typed Model Architecture

Strongly typed dataclass models provide unified contracts across the workflow. They improve testability, make intermediate states easier to inspect, and give the system a clearer reasoning surface. They also establish the communication protocol for future multi-agent workflows, where agents must exchange normalized events, score outputs, trigger states, and review artifacts without relying on ad hoc prompt glue.

Example model flow:

`RawIntakeItem` → `NormalizedEvent` → `ScoreResult` → `TriggerResult` → `NotificationArtifact`

### v7.0 Preview

The next major version is expected to introduce higher-order risk controls, including **Source Confidence**, **Fog of War**, and **Mandatory Invalidation**. These extend the same core principle: intelligence workflows should make uncertainty, evidence quality, and thesis expiry explicit rather than implicit.

Full architecture: `docs/architecture/institutional-framework.md`

## Quick Start / How to Run

The CLI is the only supported execution model for routine usage.

### 1. Install the package

```bash
pip install -e .
```

### 2. Initialize the database

```bash
gmw-init-db --db data/geo_alpha.db
```

### 3. Run the main workflow

```bash
gmw-agent --input data/intake.json
```

This processes intake through normalization, scoring, triggering, and downstream review logic.

### 4. Query results

```bash
gmw-query --stats
```

## Run Tests

```bash
pytest -m unit        # Fast isolated tests
pytest -m integration # Multi-module tests
pytest -m smoke       # Lightweight checks
pytest                # All tests
```

## Smoke Test

```bash
python scripts/smoke_run.py \
  --provider openai \
  --model gpt-4o-mini \
  --news-id demo-001 \
  --news-content "Red Sea shipping disruptions escalated."
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design & module map
- [Runbook](docs/RUNBOOK.md) - Development workflow
- [PR Checklist](docs/PR_CHECKLIST.md) - Submission checklist

## Project Structure

```
agents/          # Core agent implementations
scripts/         # CLI and utility scripts
tests/           # Test suite
docs/            # Documentation
```

## Key Design

- **State Ownership**: Orchestrator owns state, agents return updates
- **View Isolation**: Agents see minimal context (sensitive data isolated)
- **Error Boundaries**: Agent failures don't crash pipeline
- **Provider Agnostic**: Works with OpenAI, Anthropic, or custom LLMs
