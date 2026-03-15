# Idea Lifecycle Specification — Geo Market Watch v6.3

## Lifecycle States

### State Diagram

```
                    ┌─────────────┐
                    │   created   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
        ┌─────────┐  ┌──────────┐  ┌─────────┐
        │approved │  │ rejected │  │ pending │
        └────┬────┘  └──────────┘  └────┬────┘
             │                           │
        ┌────┴────┐                      │
        ↓         ↓                      ↓
  ┌──────────┐ ┌────────┐          ┌──────────┐
  │invalidated│ │ closed │          │ approved │
  └──────────┘ └────────┘          └──────────┘
```

## State Definitions

### created
- Initial state when trade idea is generated
- Automatic transition to pending_review

### pending_review
- Awaiting analyst decision
- Can transition to: approved, rejected

### approved
- Analyst has approved the idea
- Can transition to: invalidated, closed

### rejected
- Analyst has rejected the idea
- Terminal state — no further transitions

### invalidated
- Approved idea no longer valid
- Terminal state — no further transitions

### closed
- Idea has been closed out
- Terminal state — no further transitions

## Allowed Transitions

| From | To | Allowed |
|------|-----|---------|
| pending_review | approved | ✓ |
| pending_review | rejected | ✓ |
| pending_review | invalidated | ✓ |
| pending_review | closed | ✓ |
| approved | invalidated | ✓ |
| approved | closed | ✓ |
| approved | updated | ✓ |
| rejected | approved | ✗ |
| rejected | any | ✗ |
| invalidated | any | ✗ |
| closed | any | ✗ |

## Lifecycle Events

### Event Types

| Event | Description |
|-------|-------------|
| created | Trade idea generated |
| approved | Analyst approved |
| rejected | Analyst rejected |
| invalidated | Conditions changed |
| updated | Idea updated |
| closed | Position closed |

### Event Structure

```json
{
  "lifecycle_id": "uuid",
  "trade_idea_id": "trade-idea-uuid",
  "event_type": "approved",
  "event_reason": "Energy price risk justified",
  "created_at": "2026-03-15T10:00:00"
}
```

## Database Schema

### trade_ideas Table

```sql
CREATE TABLE trade_ideas (
    trade_idea_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    company_name TEXT NOT NULL,
    ticker TEXT NOT NULL,
    sector TEXT,
    idea_type TEXT,
    direction TEXT,
    conviction TEXT,
    thesis TEXT,
    invalidation_condition TEXT,
    status TEXT DEFAULT 'active',
    analyst_status TEXT DEFAULT 'pending_review',
    approval_status TEXT DEFAULT 'unreviewed',
    last_reviewed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### idea_lifecycle Table

```sql
CREATE TABLE idea_lifecycle (
    lifecycle_id TEXT PRIMARY KEY,
    trade_idea_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_reason TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (trade_idea_id) REFERENCES trade_ideas(trade_idea_id)
);
```

## Status Rules Engine

The `engine/status_rules.py` module enforces transition rules:

```python
from engine.status_rules import validate_status_transition

is_valid, error = validate_status_transition(
    old_status="pending_review",
    new_status="approved"
)
```

## Invalidation Conditions

Examples of valid invalidation reasons:

- "Shipping traffic normalizes"
- "Insurance premiums fall back"
- "Retaliation threats do not materialize"
- "Sulfur exports remain uninterrupted"
- "Fertilizer input prices stabilize"

## Closure Reasons

Examples of valid closure reasons:

- "Position exited at target"
- "Thesis complete"
- "Time horizon expired"
- "Risk limit reached"

## Implementation Notes

- All status changes are atomic (transaction)
- Lifecycle events are immutable
- Terminal states cannot be exited
- Review notes required for negative outcomes
