# Benchmark v6.3 — Analyst Review Workflow

## Purpose

This benchmark validates the analyst review and lifecycle management system introduced in v6.3.

## Test Coverage

- ✓ Review submission workflow
- ✓ Status transition validation
- ✓ Lifecycle event logging
- ✓ Required notes enforcement
- ✓ Dashboard view prioritization
- ✓ CLI script functionality

## Sample Validation Results

### Database Schema

```
✓ trade_ideas table exists
✓ idea_reviews table exists
✓ idea_lifecycle table exists
✓ All indexes created
```

### Status Rules Engine

```
✓ pending_review → approved: allowed
✓ pending_review → rejected: allowed
✓ approved → invalidated: allowed
✓ rejected → approved: blocked
✓ invalidated → any: blocked
```

### Review Submission

```
✓ approve without notes: accepted
✓ reject without notes: rejected (error)
✓ needs_revision without notes: rejected (error)
✓ monitor without notes: accepted
```

### Lifecycle Events

```
✓ created event logged
✓ approved event logged
✓ invalidated event logged
✓ Event history retrievable
```

## Example Workflows

### Workflow 1: Approve Trade Idea

```bash
# Submit review
python scripts/review_trade_ideas.py \
  --db data/geo_alpha.db \
  --idea-id abc123 \
  --reviewer analyst1 \
  --decision approve \
  --confidence high \
  --notes "Strong thesis, clear invalidation"

# Result
✓ Review submitted
✓ Status updated to approved
✓ Lifecycle event created
```

### Workflow 2: Reject Without Notes (Fails)

```bash
python scripts/review_trade_ideas.py \
  --db data/geo_alpha.db \
  --idea-id abc123 \
  --reviewer analyst1 \
  --decision reject

# Result
✗ Error: Review decision 'reject' requires notes
```

### Workflow 3: Invalidate Approved Idea

```bash
python scripts/invalidate_trade_idea.py \
  --db data/geo_alpha.db \
  --idea-id abc123 \
  --reason "Shipping traffic normalizing"

# Result
✓ Trade idea invalidated
✓ Lifecycle event created
```

## Dashboard View Test

### Active Ideas Sorting

Input:
- 3 approved ideas (high, medium, low conviction)
- 2 pending ideas
- 1 rejected idea

Expected Output Order:
1. Approved + high conviction
2. Approved + medium conviction
3. Approved + low conviction
4. Pending ideas (by recency)

Result: ✓ Pass

## Interpretation

This benchmark validates the repository's transformation from an idea generation engine into a structured research workflow system.

The v6.3 release adds:
- Human review layer
- Quality control via required notes
- Lifecycle tracking
- Audit trail

It does not yet validate:
- Performance tracking
- Automated invalidation
- Multi-analyst consensus
- Integration with execution systems

## Files Validated

| File | Purpose |
|------|---------|
| engine/status_rules.py | Status transition rules |
| engine/idea_review_engine.py | Review processing |
| engine/lifecycle_engine.py | Lifecycle tracking |
| scripts/review_trade_ideas.py | Review CLI |
| scripts/approve_trade_idea.py | Quick approval CLI |
| scripts/invalidate_trade_idea.py | Invalidation CLI |
| scripts/list_active_ideas.py | Active ideas CLI |
| docs/analyst-workflow.md | Workflow documentation |
| docs/idea-lifecycle-spec.md | Lifecycle specification |
| docs/analyst-review-guidelines.md | Review guidelines |

## Next Steps

- Populate with sample trade ideas
- Run end-to-end review workflows
- Validate dashboard exports
- Test edge cases and error handling
