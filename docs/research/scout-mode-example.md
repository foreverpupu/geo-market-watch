# Scout Mode Example

Scout Mode is a lightweight monitoring workflow designed to detect early geopolitical signals.

It runs a simplified pipeline before triggering full analysis.

---

# Input

News headline:

> "Houthi attacks force major shipping lines to avoid Red Sea"

Source:

https://www.reuters.com/world/middle-east/red-sea-shipping

---

# Step 1 — Event Classification

Detected Category:

- ✓ Maritime disruption 
- ✓ Conflict escalation

Confidence: Medium

---

# Step 2 — Market Exposure Check

Potentially affected sectors:

- Container shipping
- Oil tanker routes
- Freight rates

---

# Step 3 — Signal Strength

Indicators:

| Indicator | Status |
|----------|-------|
| Trade route disruption | Yes |
| Insurance premium spike | Unknown |
| Naval intervention | Pending |

Signal Score:

**6 / 10**

---

# Step 4 — Escalation Decision

If score ≥7 → Full Analysis Mode

Current result:

Scout monitoring continues.

---

# Output Card

**EVENT CARD**

| Field | Value |
|-------|-------|
| **Event Title** | Red Sea shipping disruption |
| **Date** | 2024-01-15 |
| **Region** | Middle East / Red Sea |
| **Category** | Maritime disruption, Conflict escalation |

**Source:**
Reuters - https://www.reuters.com/world/middle-east/red-sea-shipping

**Event Summary:**
Houthi attacks force major shipping lines to avoid Red Sea routes, causing significant trade disruption.

**Market Exposure:**
- Container shipping
- Oil tanker routes
- Freight rates

**Signal Indicators:**

| Indicator | Status |
|-----------|--------|
| Trade route disruption | Yes |
| Insurance premium spike | Unknown |
| Naval intervention | Pending |

**Signal Strength:** 6 / 10

**Monitoring Window:** 24 hours

---

# Event Card Format

Standardized output format for Scout Mode:

```
EVENT CARD

Event Title    [Descriptive name]
Date           [YYYY-MM-DD]
Region         [Geographic location]
Category       [Event type tags]

Source         [URL or reference]

Event Summary  [2-3 sentence description]

Market Exposure
• [Sector 1]
• [Sector 2]
• [Sector 3]

Signal Indicators
| Indicator | Status |
|-----------|--------|
| [Metric 1] | [Yes/No/Unknown] |
| [Metric 2] | [Yes/No/Unknown] |

Signal Strength [0-10 score]

Monitoring Window [Time to next check]
```

---

# Rules

**Do not:**

- speculate
- predict prices
- produce trading advice

**Scout Mode only detects signals.**
