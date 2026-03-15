# Evaluation Report Template

**Version:** vX.Y  
**Date:** YYYY-MM-DD  
**Evaluator:** Name

---

## 1. Version Summary

### Release Highlights
- Major features added
- Architecture changes
- Breaking changes (if any)

### Scope
What was evaluated in this version:
- [ ] Event normalization
- [ ] Signal scoring
- [ ] Escalation logic
- [ ] Trade idea generation
- [ ] Performance tracking
- [ ] Other: ___

---

## 2. Benchmark Coverage

| Category | Cases | Pass | Fail | Pass Rate |
|----------|-------|------|------|-----------|
| Shipping Disruption | 1 | 1 | 0 | 100% |
| Sanctions | 1 | 1 | 0 | 100% |
| Commodity Shock | 1 | 1 | 0 | 100% |
| Military Escalation | 1 | 1 | 0 | 100% |
| Election Shock | 1 | 1 | 0 | 100% |
| **Total** | **5** | **5** | **0** | **100%** |

### Coverage Gap Analysis
Categories not yet covered:
- [ ] Cross-market exposure mapping
- [ ] Supply chain disruption
- [ ] Energy infrastructure
- [ ] Financial crisis contagion
- [ ] Trade policy changes

---

## 3. Schema Pass Rate

| Component | Tests | Pass | Fail | Rate |
|-----------|-------|------|------|------|
| Event Card | 50 | 50 | 0 | 100% |
| Watchlist Item | 30 | 30 | 0 | 100% |
| Analysis Output | 20 | 20 | 0 | 100% |
| **Overall** | **100** | **100** | **0** | **100%** |

---

## 4. Pipeline Pass Rate

| Stage | Tests | Pass | Fail | Rate |
|-------|-------|------|------|------|
| Normalization | 10 | 10 | 0 | 100% |
| Dedupe | 5 | 5 | 0 | 100% |
| Scoring | 15 | 15 | 0 | 100% |
| Escalation | 10 | 10 | 0 | 100% |
| Output Generation | 10 | 10 | 0 | 100% |
| **Overall** | **50** | **50** | **0** | **100%** |

---

## 5. Escalation Precision

### True Positives (Correctly escalated)
- Case 001: Shipping disruption → Full analysis ✅
- Case 003: Oil shock → Full analysis ✅
- Case 005: Election → Full analysis ✅

### True Negatives (Correctly monitored)
- Case 004: Fog of war → Monitor ✅

### False Positives (Over-escalation)
- None observed

### False Negatives (Under-escalation)
- None observed

**Precision:** 100%  
**Recall:** 100%

---

## 6. Trigger Quality Observations

### Strengths
- Clear sector identification
- Appropriate watchlist construction
- Valid invalidation conditions

### Weaknesses
- (Placeholder for actual observations)

### Recommendations
- (Placeholder for improvements)

---

## 7. Analyst Override Rate

In production use (if applicable):
- Total escalations: X
- Analyst overrides: Y
- Override rate: Z%

Common override reasons:
1. (Placeholder)
2. (Placeholder)

---

## 8. Known Limitations

### Current Version
1. Limited to 5 benchmark cases
2. No real-time data integration
3. Manual price entry for performance tracking
4. Single-user local database

### Systemic Limitations
1. No transaction cost modeling
2. No position sizing logic
3. No multi-asset portfolio view

---

## 9. Next Iteration Priorities

### P0 (Critical)
- [ ] Expand benchmark to 10 cases
- [ ] Add cross-market exposure case
- [ ] Improve fog-of-war detection

### P1 (Important)
- [ ] Add supply chain disruption case
- [ ] Add energy infrastructure case
- [ ] Automate benchmark runner

### P2 (Nice to have)
- [ ] Performance regression testing
- [ ] Multi-version comparison
- [ ] Benchmark visualization

---

## 10. Conclusion

**Overall Assessment:** (Placeholder)

**Recommendation:** (Placeholder)

**Confidence Level:** High / Medium / Low

---

## Appendix: Raw Data

(Link to detailed test outputs, logs, etc.)
