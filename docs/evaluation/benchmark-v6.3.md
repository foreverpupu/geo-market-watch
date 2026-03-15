# Geo Market Watch v6.3 Benchmark

## Release Overview

**Version:** v6.3  
**Release Date:** 2026-03-15  
**Codename:** Analyst Review  

## What's New

### 1. Analyst Review Workflow
- Submit reviews with decisions: approve, monitor, reject, needs_revision
- Confidence levels: low, medium, high
- Review notes and audit trail
- Batch review capabilities

### 2. Idea Lifecycle Management
- Track full lifecycle from creation to closure
- Invalidation tracking with reasons
- Update history
- Terminal state management

### 3. Status Rules Engine
- Validated state transitions
- Prevents invalid operations
- Clear terminal states
- Transition audit trail

### 4. CLI Tools
- `review_trade_ideas.py` - Submit reviews
- `approve_trade_idea.py` - Quick approval
- `invalidate_trade_idea.py` - Invalidate ideas
- `list_active_ideas.py` - List and filter ideas

### 5. Database Extensions
- `idea_reviews` table
- `idea_lifecycle` table
- Extended `trade_ideas` with analyst fields
- Full indexing for performance

## Architecture

```
┌─────────────────────────────────────────┐
│           CLI Scripts Layer             │
│  review_trade_ideas.py                  │
│  approve_trade_idea.py                  │
│  invalidate_trade_idea.py               │
│  list_active_ideas.py                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Engine Layer                  │
│  idea_review_engine.py  ← Reviews       │
│  lifecycle_engine.py    ← Lifecycle     │
│  status_rules.py        ← Validation    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│           Database Layer                │
│  trade_ideas (extended)                 │
│  idea_reviews (new)                     │
│  idea_lifecycle (new)                   │
└─────────────────────────────────────────┘
```

## Performance Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Review submission | <100ms | ✓ |
| Status transition | <50ms | ✓ |
| List active ideas | <200ms | ✓ |
| Lifecycle history | <100ms | ✓ |

## Test Coverage

### Unit Tests
- [x] Status rule validation
- [x] Review submission
- [x] Lifecycle events
- [x] State transitions
- [x] CLI argument parsing

### Integration Tests
- [x] End-to-end review workflow
- [x] Invalidation flow
- [x] Update flow
- [x] Batch operations
- [x] Database constraints

### Manual Tests
- [x] CLI usability
- [x] Error messages
- [x] Documentation accuracy
- [x] Example files

### Review Workflow Validation
- [x] reject without notes fails
- [x] needs_revision without notes fails
- [x] approve without notes succeeds
- [x] monitor without notes succeeds

### Dashboard Ordering Validation
- [x] approved ideas appear before pending/rejected/invalidated ideas
- [x] high-conviction approved ideas appear above medium/low-conviction ideas
- [x] ordering is stable and deterministic

## Migration Guide

### From v6.2 to v6.3

1. **Database Migration** (automatic)
   ```bash
   # New tables created automatically on first use
   # Existing trade_ideas get default values:
   #   analyst_status = 'pending_review'
   #   approval_status = 'unreviewed'
   ```

2. **Update Scripts**
   ```bash
   # New scripts available:
   scripts/review_trade_ideas.py
   scripts/approve_trade_idea.py
   scripts/invalidate_trade_idea.py
   scripts/list_active_ideas.py
   ```

3. **Workflow Changes**
   - All existing ideas start as `pending_review`
   - Analysts must review and approve before tracking
   - Invalidation requires explicit reason

## Known Limitations

1. **No Email Notifications** - Reviews require manual checking
2. **No Web UI** - CLI only for now
3. **Single Reviewer** - No multi-analyst consensus
4. **No Auto-Invalidation** - Manual invalidation only

## Future Enhancements (v6.4+)

- [ ] Web UI for reviews
- [ ] Email/Slack notifications
- [ ] Multi-analyst consensus
- [ ] Auto-invalidation rules
- [ ] Performance analytics
- [ ] Reviewer leaderboards
- [ ] ML-based approval suggestions

## Compliance Notes

- All reviews are logged with timestamp and reviewer ID
- Lifecycle events create audit trail
- Status changes are validated and recorded
- Database supports compliance reporting

## Documentation

- `docs/analyst-workflow.md` - Workflow guide
- `docs/idea-lifecycle-spec.md` - Technical spec
- `docs/analyst-review-guidelines.md` - Review criteria
- `examples/analyst-review.example.json` - Example review
- `examples/idea-lifecycle.example.md` - Example lifecycle

## Verification Checklist

- [x] Database schema updated
- [x] All scripts executable
- [x] Documentation complete
- [x] Examples provided
- [x] Tests passing
- [x] Benchmark metrics met
- [x] Migration tested
- [x] CLI help works
- [x] Review notes enforced for reject/needs_revision
- [x] Dashboard prioritization implemented

## Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Developer | OpenClaw | 2026-03-15 | ✓ |
| Reviewer | Amy | TBD | Pending |
| QA | Auto | 2026-03-15 | ✓ |
