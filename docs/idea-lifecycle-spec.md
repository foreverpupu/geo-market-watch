# Idea Lifecycle Specification

## Overview

This document defines the lifecycle management system for trade ideas in Geo Market Watch v6.3.

## Lifecycle States

### Analyst Status

| Status | Description | Terminal |
|--------|-------------|----------|
| `pending_review` | Awaiting analyst review | No |
| `approved` | Passed review, active tracking | No |
| `rejected` | Failed review | Yes |
| `invalidated` | Thesis no longer valid | Yes |
| `closed` | Idea completed or expired | Yes |

### Approval Status

| Status | Description |
|--------|-------------|
| `unreviewed` | No review submitted |
| `approved` | Review approved the idea |
| `rejected` | Review rejected the idea |

## Lifecycle Events

Events are recorded in the `idea_lifecycle` table:

| Event Type | Trigger | Description |
|------------|---------|-------------|
| `created` | Auto | Trade idea generated |
| `approved` | Review | Analyst approved the idea |
| `rejected` | Review | Analyst rejected the idea |
| `invalidated` | Manual | Thesis invalidated |
| `updated` | Manual | Idea details updated |
| `closed` | Manual | Idea closed |

## State Transition Rules

### Analyst Status Transitions

```
                    ┌─────────────┐
                    │   CREATED   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
         ┌─────────│   PENDING   │◄────────┐
         │         │   REVIEW    │         │
         │         └──────┬──────┘         │
         │                │                │
         ▼                ▼                │
   ┌─────────┐      ┌─────────┐           │
   │REJECTED │      │APPROVED │───────────┘
   │(terminal)│     └────┬────┘ (monitor)
   └─────────┘           │
                         ▼
              ┌───────────────────┐
              │                   │
              ▼                   ▼
        ┌──────────┐        ┌─────────┐
        │INVALIDATED│       │ CLOSED  │
        │(terminal)│        │(terminal)│
        └──────────┘        └─────────┘
```

### Valid Transitions

| From | To | Allowed |
|------|-----|---------|
| pending_review | approved | ✓ |
| pending_review | rejected | ✓ |
| pending_review | invalidated | ✓ |
| approved | invalidated | ✓ |
| approved | closed | ✓ |
| approved | updated | ✓ |
| rejected | approved | ✗ |
| invalidated | approved | ✗ |
| closed | approved | ✗ |

### Approval Status Transitions

| From | To | Allowed |
|------|-----|---------|
| unreviewed | approved | ✓ |
| unreviewed | rejected | ✓ |
| approved | rejected | ✓ (revoke) |
| rejected | approved | ✓ (reconsider) |

## Data Model

### Trade Ideas Table

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
    updated_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
```

### Idea Reviews Table

```sql
CREATE TABLE idea_reviews (
    review_id TEXT PRIMARY KEY,
    trade_idea_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    review_decision TEXT NOT NULL,  -- approve, monitor, reject, needs_revision
    confidence TEXT,                -- low, medium, high
    review_notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (trade_idea_id) REFERENCES trade_ideas(trade_idea_id)
);
```

### Idea Lifecycle Table

```sql
CREATE TABLE idea_lifecycle (
    lifecycle_id TEXT PRIMARY KEY,
    trade_idea_id TEXT NOT NULL,
    event_type TEXT NOT NULL,       -- created, approved, rejected, invalidated, updated, closed
    event_reason TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (trade_idea_id) REFERENCES trade_ideas(trade_idea_id)
);
```

## API Functions

### Lifecycle Engine

```python
# Record a lifecycle event
record_lifecycle_event(db_path, trade_idea_id, event_type, reason)

# Invalidate an approved idea
invalidate_trade_idea(db_path, trade_idea_id, reason)

# Close an idea
close_trade_idea(db_path, trade_idea_id, reason)

# Update idea details
update_trade_idea(db_path, trade_idea_id, update_reason, **updates)

# Get lifecycle history
get_lifecycle_history(db_path, trade_idea_id)

# Get all active ideas
get_active_ideas(db_path)

# Get ideas by status
get_ideas_by_status(db_path, status)
```

### Review Engine

```python
# Submit a review
submit_review(db_path, trade_idea_id, reviewer, decision, confidence, notes)

# Get reviews for an idea
get_reviews_for_idea(db_path, trade_idea_id)

# Get pending reviews
get_pending_reviews(db_path)

# Get review statistics
get_review_statistics(db_path)

# Batch review multiple ideas
batch_review(db_path, reviewer, reviews)

# Get reviewer activity
get_reviewer_activity(db_path, reviewer)
```

## Invalidation Conditions

When creating a trade idea, specify clear invalidation conditions:

| Idea Type | Example Invalidation Condition |
|-----------|-------------------------------|
| Long energy | "Oil prices drop below $70/bbl" |
| Short shipping | "Baltic Dry Index normalizes below 1500" |
| Long defense | "Ceasefire agreement signed" |
| Short airline | "Flight cancellations drop below 5%" |
| Long fertilizer | "Urea prices stabilize below $400/ton" |

## Audit Trail

Every state change is recorded:

1. **Review submitted** → Record in `idea_reviews`
2. **Status changed** → Update `trade_ideas.analyst_status`
3. **Lifecycle event** → Record in `idea_lifecycle`

This creates a complete audit trail for compliance and analysis.

## Reporting

### Statistics Available

- Ideas by status
- Reviews by decision type
- Reviewer activity
- Average time to review
- Invalidation reasons
- Approval rates by sector

### Example Queries

```sql
-- Approval rate
SELECT 
    approval_status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM trade_ideas
GROUP BY approval_status;

-- Invalidation reasons
SELECT 
    event_reason,
    COUNT(*) as count
FROM idea_lifecycle
WHERE event_type = 'invalidated'
GROUP BY event_reason
ORDER BY count DESC;

-- Reviewer activity
SELECT 
    reviewer,
    review_decision,
    COUNT(*) as count
FROM idea_reviews
GROUP BY reviewer, review_decision;
```
