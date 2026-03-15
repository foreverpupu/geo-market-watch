# Geo Market Watch — Code Structure

## Architecture Overview

```
geo-market-watch/
├── engine/          # Business logic (reusable components)
├── scripts/         # CLI entry points (orchestration)
├── tests/           # Test suites
└── docs/            # Documentation
```

---

## Engine Layer (`engine/`)

**Responsibility:** Core business logic, reusable components

**Design Principle:** Engine modules should be importable and testable independently of CLI scripts.

### Module Organization

| Module | Responsibility | Key Functions |
|--------|----------------|---------------|
| `intake_normalizer.py` | Event normalization | `normalize_event()`, `validate_event()` |
| `dedupe_memory.py` | Duplicate detection | `check_duplicate()`, `add_to_memory()` |
| `scoring_engine.py` | Signal scoring | `compute_score()`, `get_score_band()` |
| `trigger_engine.py` | Escalation logic | `should_escalate()`, `get_trigger_reason()` |
| `agent_loop.py` | Orchestration | `run_agent_loop()`, `process_event()` |
| `notifier.py` | Output generation | `generate_notification()`, `format_output()` |
| `lifecycle_engine.py` | Idea lifecycle | `record_event()`, `invalidate_idea()` |
| `performance_engine.py` | Performance tracking | `start_tracking()`, `close_tracking()` |
| `exposure_engine.py` | Market exposure | `map_to_sectors()`, `map_to_companies()` |
| `idea_review_engine.py` | Analyst review | `submit_review()`, `get_pending_reviews()` |
| `dashboard_views.py` | Data views | `get_active_ideas()`, `get_performance_summary()` |
| `export_layer.py` | Data export | `export_to_json()`, `export_to_csv()` |
| `database.py` | Database operations | `connect_db()`, `execute_query()` |
| `database_models.py` | Schema definitions | Table schemas, validation |
| `status_rules.py` | State machine | `validate_transition()`, `get_allowed_states()` |

### Engine Design Principles

1. **Pure Functions Where Possible** — Minimize side effects
2. **Explicit Dependencies** — Pass dependencies as parameters
3. **Return Values** — Return data, don't print
4. **Error Handling** — Raise exceptions, don't exit
5. **Testable** — Each function testable in isolation

---

## Scripts Layer (`scripts/`)

**Responsibility:** CLI entry points, user-facing orchestration

**Design Principle:** Scripts handle argument parsing, I/O, and call engine functions. They should be thin wrappers.

### Script Categories

#### Core Workflow
| Script | Purpose | Calls Engine |
|--------|---------|--------------|
| `run_agent_loop.py` | Main processing loop | `agent_loop.run_agent_loop()` |
| `init_database.py` | Database initialization | `database.init_db()` |
| `seed_database.py` | Sample data loading | `database.seed_data()` |

#### Analyst Workflow
| Script | Purpose | Calls Engine |
|--------|---------|--------------|
| `review_trade_ideas.py` | Submit reviews | `idea_review_engine.submit_review()` |
| `approve_trade_idea.py` | Quick approval | `idea_review_engine.submit_review()` |
| `invalidate_trade_idea.py` | Invalidate ideas | `lifecycle_engine.invalidate_idea()` |
| `list_active_ideas.py` | List ideas | `dashboard_views.get_active_ideas()` |

#### Performance Tracking
| Script | Purpose | Calls Engine |
|--------|---------|--------------|
| `start_idea_tracking.py` | Start tracking | `performance_engine.start_tracking()` |
| `close_trade_idea.py` | Close tracking | `performance_engine.close_tracking()` |
| `update_idea_price_reference.py` | Update prices | `performance_engine.update_reference()` |
| `list_tracked_ideas.py` | List tracked | `performance_engine.list_tracked()` |

#### Data Operations
| Script | Purpose | Calls Engine |
|--------|---------|--------------|
| `query_database.py` | Query events | `database.query()`, `dashboard_views.*` |
| `export_dashboard_data.py` | Export data | `export_layer.export_dashboard_data()` |
| `ingest_artifacts.py` | Import data | `artifact_ingest.ingest()` |

#### Benchmarking
| Script | Purpose | Calls Engine |
|--------|---------|--------------|
| `run_benchmark.py` | Run benchmarks | Multiple engine modules |

### Script Design Principles

1. **Argument Parsing** — Use `argparse` with clear help text
2. **Input Validation** — Validate CLI arguments
3. **Error Messages** — User-friendly error messages
4. **Exit Codes** — 0 for success, 1 for error
5. **Thin Wrappers** — Delegate to engine, don't implement logic

---

## Data Contracts

### Between Engine Modules

```python
# Event object (normalized)
event = {
    "event_id": str,
    "headline": str,
    "summary": str,
    "region": str,
    "category": str,
    "severity": str,
    "timestamp": str (ISO 8601)
}

# Score result
score_result = {
    "value": float (0-10),
    "band": str ("low"/"medium"/"high"/"critical"),
    "reasoning": str
}

# Escalation decision
escalation = {
    "decision": str ("monitor"/"full_analysis"),
    "rationale": str
}
```

### Between Scripts and Engine

Scripts pass primitive types and receive data structures:

```python
# Script calls engine
event = engine.intake_normalizer.normalize_event(raw_input)
score = engine.scoring_engine.compute_score(event)
should_escalate = engine.trigger_engine.should_escalate(score)
```

---

## Testing Strategy

### Engine Tests
- Unit tests for each engine function
- Mock external dependencies
- Test edge cases and error conditions

### Script Tests
- Integration tests for CLI workflows
- Test argument parsing
- Test exit codes

### Pipeline Tests
- End-to-end workflow tests
- Use benchmark cases

---

## Migration Guidelines

### When to Add to Engine
- Logic needs to be reused across scripts
- Logic needs to be tested independently
- Logic represents core business rule

### When to Keep in Scripts
- CLI-specific argument handling
- File I/O operations
- User interaction
- Orchestration logic

### Refactoring Checklist
- [ ] Move business logic to engine
- [ ] Keep CLI handling in scripts
- [ ] Add tests for engine functions
- [ ] Update script to call engine
- [ ] Verify script still works
- [ ] Update documentation

---

## Current State

**v6.4 Status:**
- ✅ Engine modules well-separated
- ✅ Scripts are thin wrappers
- ✅ Clear data contracts
- ✅ Testable architecture

**Future Improvements:**
- Add more comprehensive engine tests
- Standardize error handling across scripts
- Add logging configuration

---

## Example: Adding a New Feature

1. **Implement logic in engine:**
   ```python
   # engine/new_feature.py
   def process_data(data):
       # Business logic here
       return result
   ```

2. **Create CLI script:**
   ```python
   # scripts/run_new_feature.py
   import argparse
   from engine.new_feature import process_data
   
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--input", required=True)
       args = parser.parse_args()
       
       result = process_data(args.input)
       print(result)
   
   if __name__ == "__main__":
       main()
   ```

3. **Add tests:**
   ```python
   # tests/test_new_feature.py
   from engine.new_feature import process_data
   
   def test_process_data():
       result = process_data("test")
       assert result is not None
   ```

---

**Summary:** Engine = business logic, Scripts = CLI entry points. Keep them separate for maintainability and testability.
