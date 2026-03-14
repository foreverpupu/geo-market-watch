# Engine Module

This module contains the **first executable components** of Geo Market Watch.

**Included:**

- `scoring_engine.py` — calculates signal scores from structured event inputs
- `trigger_engine.py` — decides whether an event should escalate into Full Analysis Mode

This release introduces **deterministic execution logic** without external dependencies.

---

## ⚠️ Current Limitations

This is **not yet** a full autonomous agent system.

**What it does NOT include:**
- ❌ Automatic extraction from raw articles
- ❌ Event deduplication
- ❌ Live news ingestion pipeline
- ❌ Database persistence layer
- ❌ Multi-agent orchestration

**What it DOES include:**
- ✅ Deterministic scoring from structured inputs
- ✅ Explicit trigger rules
- ✅ Validation and error handling
- ✅ Reproducible benchmark testing

**Status:** The engine accepts pre-structured Event Card objects and converts them into scores and trigger decisions. Article parsing and automated ingestion are planned for future releases.

---

## Components

### Scoring Engine (`scoring_engine.py`)

Converts Event Card indicators into a deterministic signal score (0-10).

**What it does:**
- Reads structured Event Card data
- Validates indicator values against maximums
- Calculates total score across 5 dimensions
- Maps score to signal band (noise/monitor/full_analysis/major_shock)

**Input:**
```python
{
    "event_title": "Red Sea shipping disruption",
    "date_detected": "2024-01-12",
    "region": "Middle East",
    "category": "Maritime disruption",
    "indicators": {
        "physical_disruption": 1,    # max 3
        "transport_impact": 2,       # max 2
        "policy_sanctions": 0,       # max 2
        "market_transmission": 1,    # max 2
        "escalation_risk": 1         # max 1
    }
}
```

**Output:**
```python
{
    "event_title": "Red Sea shipping disruption",
    "score": 5,
    "band": "monitor"
}
```

---

### Trigger Engine (`trigger_engine.py`)

Decides whether Full Analysis Mode should be triggered.

**What it does:**
- Evaluates signal score against threshold (≥7)
- Checks escalation flags
- Returns trigger decision with reasons

**Input:**
```python
{
    "event_title": "Russia expands oil export restrictions",
    "score": 7,
    "flags": {
        "confirmed_supply_disruption": False,
        "strategic_transport_disruption": False,
        "major_sanctions_escalation": True,
        "military_escalation": False
    }
}
```

**Output:**
```python
{
    "event_title": "Russia expands oil export restrictions",
    "trigger_full_analysis": True,
    "reasons": ["score_threshold", "major_sanctions_escalation"]
}
```

---

## Design Principles

- **Deterministic**: Same input always produces same output
- **No external dependencies**: No APIs, no LLM calls, no database
- **Minimal**: Only implements documented framework rules
- **Validating**: Clear errors for invalid inputs

---

## Usage

```python
from scoring_engine import score_event
from trigger_engine import evaluate_trigger

# Score an event
event_card = {...}
score_result = score_event(event_card)

# Check if full analysis should trigger
trigger_data = {
    "event_title": score_result["event_title"],
    "score": score_result["score"],
    "flags": {...}
}
trigger_result = evaluate_trigger(trigger_data)
```

---

## About

This is the **first executable layer** of Geo Market Watch.

It bridges the gap between:
- **Documentation** (docs/signal-scoring.md, docs/full-analysis-trigger.md)
- **Implementation** (machine-executable Python code)

Future releases will build upon these engines to create:
- Automated event ingestion
- Database integration
- Dashboard visualization
- Alert systems
