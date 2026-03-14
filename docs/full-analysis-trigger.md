# Full Analysis Trigger

This document defines when Scout Mode should escalate to Full Analysis Mode.

---

# Trigger Conditions

Full Analysis is triggered when any of the following conditions are met.

## Signal Score Threshold

**Condition:** Signal score ≥ 7

When the Scout Agent assigns a score of 7 or higher, automatic escalation occurs.

## Explicit Escalation Triggers

**Physical Disruption**

- Confirmed export halt
- Major route blockage
- Infrastructure destruction

**Policy Changes**

- New sanctions announced
- Export restrictions imposed
- Trade policy reversal

**Market Indicators**

- Insurance premium spike (>50%)
- Freight rate surge (>30%)
- Commodity price gap opens

**Conflict Escalation**

- Military action expands
- New actors enter conflict
- Regional allies activated

---

# Escalation Process

When triggered, the following occurs:

1. **Event Freezing**
   - Lock event details
   - Preserve source links
   - Record trigger timestamp

2. **Context Gathering**
   - Collect related news
   - Identify key actors
   - Map affected regions

3. **Full Analysis Launch**
   - Run SKILL.md methodology
   - Generate 9-section report
   - Create structured watchlist

4. **Output Delivery**
   - Human-readable report
   - JSON structured output
   - Alert notifications

---

# No-Escalation Rules

Full Analysis is **not** triggered when:

- Event is purely diplomatic rhetoric
- No physical supply impact detected
- Source reliability is low (Tier 3 only)
- Market has already absorbed news

These events remain in Scout monitoring.

---

# Example Escalation

**Event:** Red Sea shipping attacks

**Initial Scout Score:** 6

**Day 2 Update:**
- Insurance premiums spike 80%
- Major carrier announces indefinite suspension

**New Score:** 8

**Trigger:** Score ≥ 7 threshold met

**Action:** Escalate to Full Analysis Mode

**Output:**
- Confirmed facts section
- Market interpretation
- Scenario analysis (A/B/C)
- Structured watchlist with triggers
- Invalidation conditions

---

# Post-Analysis Return

After Full Analysis completes, events may return to Scout Mode if:

- Invalidation conditions met
- Signal strength drops below 4
- No further escalation triggers

This prevents alert fatigue from stale events.
