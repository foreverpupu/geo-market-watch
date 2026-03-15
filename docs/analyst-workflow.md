# Analyst Workflow Guide

## Overview

The Geo Market Watch v6.3 analyst workflow transforms automatically generated trade ideas into a reviewable research process. This guide explains how analysts interact with the system.

## Workflow Stages

```
Event Detection
      ↓
Sector Exposure Analysis
      ↓
Company Exposure Mapping
      ↓
Trade Idea Generation
      ↓
┌─────────────────┐
│  PENDING REVIEW │ ← Analyst review required
└─────────────────┘
      ↓
   ┌────┴────┐
   ↓         ↓
APPROVED   REJECTED
   ↓
┌────┴────┐
↓         ↓
ACTIVE   INVALIDATED/CLOSED
```

## Review Decisions

When reviewing a trade idea, analysts can choose from four decisions:

| Decision | Description | Status Change | Notes Required |
|----------|-------------|---------------|----------------|
| **approve** | Idea passes review, ready for tracking | → approved | Optional |
| **monitor** | Idea has potential but needs watching | → pending_review | Optional |
| **reject** | Idea doesn't meet criteria | → rejected | **Required** |
| **needs_revision** | Thesis needs more work | → pending_review | **Required** |

**Note:** Review notes are mandatory for `reject` and `needs_revision` decisions to ensure feedback quality and audit trail completeness.

### Confidence Levels

- **low** - High uncertainty, speculative
- **medium** - Reasonable confidence, some risks
- **high** - Strong conviction, clear catalyst

## CLI Commands

### Review an Idea

```bash
python scripts/review_trade_ideas.py \
    --db data/geo_alpha.db \
    --idea-id TRADE_ID \
    --reviewer analyst_name \
    --decision approve \
    --confidence high \
    --notes "Strong thesis, clear risk/reward"
```

### Quick Approve

```bash
python scripts/approve_trade_idea.py \
    --db data/geo_alpha.db \
    --idea-id TRADE_ID \
    --reviewer amy \
    --confidence high \
    --notes "Energy price risk justified"
```

### Invalidate an Idea

When the thesis no longer holds:

```bash
python scripts/invalidate_trade_idea.py \
    --db data/geo_alpha.db \
    --idea-id TRADE_ID \
    --reason "Shipping traffic normalized, disruption risk faded"
```

### List Active Ideas

```bash
# All active ideas
python scripts/list_active_ideas.py --db data/geo_alpha.db

# Pending review
python scripts/list_active_ideas.py --db data/geo_alpha.db --status pending_review

# Approved ideas
python scripts/list_active_ideas.py --db data/geo_alpha.db --status approved

# Statistics
python scripts/list_active_ideas.py --db data/geo_alpha.db --stats

# Lifecycle history
python scripts/list_active_ideas.py --db data/geo_alpha.db --history TRADE_ID
```

## Review Guidelines

### Approve When:
- Clear geopolitical catalyst identified
- Risk/reward is asymmetric
- Invalidation conditions are specific
- Conviction level matches thesis strength

### Reject When:
- Thesis is too vague or generic
- Risk/reward is not favorable
- No clear catalyst or timeline
- Better opportunities exist

### Monitor When:
- Event is developing but not confirmed
- Need more data on impact magnitude
- Waiting for price action confirmation

### Needs Revision When:
- Good concept but thesis unclear
- Missing key risk factors
- Invalidation conditions too broad

## Status Transitions

### Allowed Transitions

```
pending_review → approved
pending_review → rejected
pending_review → invalidated

approved → invalidated
approved → closed
approved → updated
```

### Terminal States (No Further Changes)

- **rejected** - Final decision
- **invalidated** - Thesis failed
- **closed** - Idea completed

## Invalidation Examples

Common reasons to invalidate an approved idea:

| Scenario | Invalidation Reason |
|----------|---------------------|
| Shipping disruption | "Shipping traffic normalized" |
| Supply shortage fears | "Fertilizer supply remained stable" |
| Retaliation threat | "Retaliation threat faded without action" |
| Sanctions risk | "Sanctions scope narrower than expected" |
| Military escalation | "De-escalation achieved via diplomacy" |

## Best Practices

1. **Review promptly** - Ideas are time-sensitive
2. **Document reasoning** - Notes help future analysis
3. **Be specific** - Vague invalidation conditions are useless
4. **Update as needed** - Market conditions change
5. **Track your decisions** - Learn from outcomes

## Dashboard Prioritization

The dashboard (`list_active_ideas.py`) surfaces ideas in priority order:

1. **Approved ideas first** - Status: `approved` > `pending_review` > others
2. **Highest conviction first** - Within each status: `high` > `medium` > `low`
3. **Most recent first** - Within same status + conviction: newest first

This ensures analysts see the most actionable ideas at the top.

## Integration with Research Process

The analyst workflow connects to your broader research:

1. **Morning review** - Check pending ideas from overnight events
2. **Event-driven** - Review ideas triggered by new developments
3. **Weekly audit** - Review statistics, identify patterns
4. **Post-mortem** - Analyze invalidated ideas for model improvement
