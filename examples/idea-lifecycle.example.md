# Example: Trade Idea Lifecycle

## Trade Idea

- **ID:** idea-6f2g3h4i-5j6k-7l8m-9n0o-1p2q3r4s5t6u
- **Company:** Flex LNG Ltd
- **Ticker:** FLNG
- **Sector:** Energy - LNG Shipping
- **Direction:** Long
- **Conviction:** High
- **Thesis:** Red Sea shipping disruption forces LNG carriers to reroute around Africa, increasing voyage duration and tightening vessel supply. Spot rates expected to rise 30-50%.

## Lifecycle Events

### 1. Created
- **Date:** 2026-03-10T08:15:00+00:00
- **Event:** System generated trade idea from Red Sea shipping event
- **Status:** pending_review

### 2. First Review - Monitor
- **Date:** 2026-03-10T10:30:00+00:00
- **Reviewer:** analyst1
- **Decision:** monitor
- **Notes:** "Good concept but need to verify actual rate movements. Monitor Baltic Dry Index and LNG carrier fixtures for confirmation."
- **Status:** pending_review (unchanged)

### 3. Second Review - Approve
- **Date:** 2026-03-12T14:30:00+00:00
- **Reviewer:** amy
- **Decision:** approve
- **Confidence:** high
- **Notes:** "Confirmed: LNG carrier spot rates up 25% since event. Multiple fixtures reported at premium. Thesis validated."
- **Status:** approved

### 4. Update
- **Date:** 2026-03-14T09:00:00+00:00
- **Event:** Updated conviction from medium to high based on new fixture data
- **Reason:** "Additional fixtures confirm sustained rate pressure"

### 5. Invalidation
- **Date:** 2026-03-20T16:45:00+00:00
- **Event:** Ceasefire agreement reached
- **Reason:** "Red Sea ceasefire agreement signed. Shipping routes expected to normalize within 2 weeks. Disruption thesis no longer valid."
- **Status:** invalidated

## Final Outcome

- **Total Return:** +12% (from approval to invalidation)
- **Holding Period:** 8 days
- **Review Count:** 2
- **Final Status:** invalidated (correctly)

## Lessons Learned

1. Initial monitor decision was correct - waiting for confirmation improved entry
2. High conviction justified given multiple confirming signals
3. Invalidation was timely - captured most of the move
4. Clear invalidation condition made exit decision easy

## Audit Trail

```sql
SELECT * FROM idea_lifecycle WHERE trade_idea_id = 'idea-6f2g3h4i...';

lifecycle_id | event_type   | event_reason
-------------|--------------|-------------------------------------------
lc-001       | created      | System generated from Red Sea event
lc-002       | updated      | Review by analyst1: monitor
lc-003       | approved     | Review by amy: approve - High conviction...
lc-004       | updated      | Updated conviction from medium to high...
lc-005       | invalidated  | Red Sea ceasefire agreement signed...
```
