# Analyst Workflow — Geo Market Watch v6.3

## Overview

Starting in v6.3, Geo Market Watch supports a full research workflow with analyst review and lifecycle management for trade ideas.

## Workflow Diagram

```
Event Detected
     ↓
Sector Exposure Generated
     ↓
Company Exposure Generated
     ↓
Trade Idea Generated (status: pending_review)
     ↓
Analyst Review
     ↓
┌─────────────┬─────────────┬─────────────┐
│   Approve   │   Reject    │   Monitor   │
└─────────────┴─────────────┴─────────────┘
     ↓              ↓              ↓
  Approved      Rejected      Pending
     ↓
Lifecycle Tracking
     ↓
Invalidation / Closure
```

## Review States

### Pending Review
- Initial state for all generated trade ideas
- Awaiting analyst decision
- Visible in pending dashboard

### Approved
- Analyst has approved the idea
- Idea is active and tradeable
- Tracked in active ideas list

### Rejected
- Analyst has rejected the idea
- Requires review notes explaining why
- No further transitions allowed

### Invalidated
- Approved idea no longer valid
- Conditions have changed
- Requires invalidation reason

### Closed
- Idea has been closed out
- Position exited or thesis complete
- Requires closure reason

## Review Decisions

| Decision | Result | Notes Required |
|----------|--------|----------------|
| approve | Status → approved | Optional |
| reject | Status → rejected | **Required** |
| monitor | Status stays pending | Optional |
| needs_revision | Status stays pending | **Required** |

## CLI Commands

### Submit Review

```bash
python scripts/review_trade_ideas.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --reviewer analyst1 \
  --decision approve \
  --confidence medium \
  --notes "Energy price risk justified"
```

### Quick Approve

```bash
python scripts/approve_trade_idea.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --reviewer analyst1
```

### Invalidate Idea

```bash
python scripts/invalidate_trade_idea.py \
  --db data/geo_alpha.db \
  --idea-id TRADE_ID \
  --reason "Shipping traffic normalizing"
```

### List Active Ideas

```bash
python scripts/list_active_ideas.py --db data/geo_alpha.db
```

## Dashboard Prioritization

Active ideas are sorted by:

1. **Approval status** — approved first
2. **Conviction** — high before medium before low
3. **Activity** — active before other statuses
4. **Recency** — newest first

This ensures the most decision-relevant ideas appear at the top.

## Review Quality Guidelines

### Required Notes

Review decisions `reject` and `needs_revision` **require notes**. This ensures:
- Feedback for system improvement
- Audit trail for decisions
- Learning for future idea generation

### Optional Notes

Decisions `approve` and `monitor` may include notes but are not required.

## Lifecycle Events

All status changes are logged:
- created
- approved
- rejected
- invalidated
- updated
- closed

View lifecycle history via database query or future dashboard.

## Database Tables

- **trade_ideas** — idea records with analyst_status
- **idea_reviews** — review decisions
- **idea_lifecycle** — lifecycle event log

## Integration with Exposure Engine

The analyst workflow sits on top of the v6.2 Exposure Engine:

1. Exposure Engine generates ideas
2. Ideas enter pending_review state
3. Analysts review via CLI
4. Approved ideas flow to active monitoring
5. Lifecycle engine tracks changes

## Future Enhancements

- Web dashboard for review
- Batch review capabilities
- Review assignment
- Performance tracking
- Automated invalidation triggers
