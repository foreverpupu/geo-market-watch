# Analyst Review Guidelines

## Purpose

This document provides guidelines for analysts reviewing automatically generated trade ideas from the Geo Market Watch system.

## Review Criteria

### 1. Thesis Quality

**Strong Thesis:**
- Clear geopolitical catalyst identified
- Specific timeline or trigger event
- Measurable impact on company/sector
- Logical causal chain

**Weak Thesis:**
- Vague references to "geopolitical risk"
- No specific timeline
- Generic impact statements
- Missing causal logic

### 2. Risk/Reward Assessment

**Favorable Risk/Reward:**
- Asymmetric payoff potential
- Limited downside if thesis fails
- Clear entry/exit points
- Position sizing guidance

**Unfavorable Risk/Reward:**
- Symmetric risk (equal upside/downside)
- Unclear exit strategy
- High downside if thesis fails
- No position sizing guidance

### 3. Invalidation Conditions

**Good Invalidation Condition:**
- Specific, measurable trigger
- Clear timeline
- Objective criteria
- Easy to monitor

**Poor Invalidation Condition:**
- Vague ("if situation improves")
- No specific metrics
- Subjective judgment required
- Hard to track

### 4. Conviction Level

Match conviction to thesis strength:

| Conviction | Criteria |
|------------|----------|
| **High** | Multiple confirming signals, clear catalyst, strong historical precedent |
| **Medium** | Some confirming signals, reasonable catalyst, limited precedent |
| **Low** | Single signal, speculative catalyst, no precedent |

## Decision Framework

### Approve If:

- [ ] Clear geopolitical catalyst
- [ ] Specific timeline
- [ ] Asymmetric risk/reward
- [ ] Measurable invalidation condition
- [ ] Matches current portfolio strategy
- [ ] Conviction level justified

### Reject If:

- [ ] Vague or generic thesis
- [ ] No clear catalyst
- [ ] Poor risk/reward
- [ ] Missing invalidation conditions
- [ ] Conflicts with portfolio strategy
- [ ] Conviction overstated

### Monitor If:

- [ ] Good concept but needs development
- [ ] Waiting for confirmation
- [ ] Event developing but not confirmed
- [ ] Need more data on magnitude

### Needs Revision If:

- [ ] Good idea but thesis unclear
- [ ] Missing key risk factors
- [ ] Invalidation too broad
- [ ] Conviction mismatched

## Sector-Specific Considerations

### Energy
- Check supply/demand balance
- Verify inventory levels
- Monitor OPEC+ policy
- Track alternative supply sources

### Shipping
- Check route alternatives
- Verify insurance costs
- Monitor port congestion
- Track fleet availability

### Defense
- Verify contract timing
- Check budget approvals
- Monitor procurement cycles
- Track competitive landscape

### Agriculture
- Check seasonal factors
- Verify inventory levels
- Monitor weather patterns
- Track substitute availability

### Semiconductors
- Check inventory levels
- Verify fab locations
- Monitor customer concentration
- Track alternative suppliers

## Common Pitfalls

### Overconfidence in System
- Don't approve just because system generated it
- Challenge the thesis independently
- Verify key assumptions

### Ignoring Base Rates
- Consider historical outcomes
- Don't overweight recent events
- Check similar past situations

### Confirmation Bias
- Actively seek disconfirming evidence
- Consider alternative scenarios
- Don't anchor on initial thesis

### Recency Bias
- Don't overweight latest news
- Consider longer time horizons
- Check if market already priced in

## Documentation Requirements

### Review Notes Should Include:

1. **Key Assumptions** - What must be true for thesis to work
2. **Risk Factors** - What could go wrong
3. **Catalyst Timeline** - When should we see confirmation
4. **Position Sizing** - How much exposure is appropriate
5. **Related Ideas** - Other ideas with similar thesis

### Example Review Note:

```
Approved: High conviction on LNG shipping disruption thesis.

Key assumptions:
- Red Sea closure persists >3 months
- LNG demand remains elevated
- Alternative routes insufficient

Risks:
- Ceasefire could resolve quickly
- New shipping capacity comes online
- Demand destruction from high prices

Timeline: Expect rate increases within 2-4 weeks.
Sizing: 2-3% position given high conviction.
Related: Also approved TRADE_002 (similar thesis on container shipping).
```

## Review Frequency

### Daily
- Check new pending reviews from overnight events
- Review invalidated ideas for patterns

### Weekly
- Analyze approval/rejection rates
- Review reviewer activity
- Identify systematic issues

### Monthly
- Post-mortem on closed/invalidated ideas
- Update review guidelines based on learnings
- Calibrate conviction levels

## Performance Tracking

Track your review decisions:

| Metric | Target |
|--------|--------|
| Approval rate | 30-50% |
| Avg time to review | <24 hours |
| Invalidation rate | <20% of approved |
| Revision requests | <10% |

Use these metrics to calibrate your review standards.
