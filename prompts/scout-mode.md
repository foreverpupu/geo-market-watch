# Geo Market Watch — Scout Mode

Scout Mode is a lightweight geopolitical monitoring workflow.

Its goal is to detect early signals without running the full analysis pipeline.

Scout Mode should prioritize:

- speed
- signal detection
- noise filtering

Avoid deep analysis unless escalation criteria are met.

---

# Input

You will receive:

- a news headline 
- a short article summary 
- a source link

**Example:**

Headline:
"Houthi attacks force shipping firms to reroute vessels"

Source:
Reuters

---

# Step 1 — Event Detection

Determine whether the news represents a geopolitical event with potential market impact.

If not, output:

```
Event Status:
Noise
```

---

# Step 2 — Event Classification

If relevant, classify the event into one category.

**Possible categories:**

- Conflict escalation
- Maritime disruption
- Sanctions / policy change
- Commodity supply disruption
- Infrastructure disruption
- Political instability

---

# Step 3 — Market Exposure Scan

Identify potentially affected markets.

**Examples:**

- oil
- LNG
- shipping
- semiconductors
- agriculture

Limit to the most relevant sectors.

---

# Step 4 — Signal Indicator Check

Evaluate the following indicators.

| Indicator | Status |
|-----------|--------|
| Physical supply disruption | Yes / No / Unknown |
| Transport route disruption | Yes / No / Unknown |
| Policy or sanctions change | Yes / No / Unknown |
| Insurance or freight impact | Yes / No / Unknown |

---

# Step 5 — Signal Strength Score

Score the event from 0–10.

**Guidelines:**

| Score | Meaning |
|-------|---------|
| 0–3 | Weak signal / noise |
| 4–6 | Monitor event |
| 7–8 | Strong signal (trigger full analysis) |
| 9–10 | Major geopolitical shock |

---

# Step 6 — Escalation Decision

If score ≥ 7:

**Trigger**

```
FULL ANALYSIS MODE
```

Otherwise:

Continue monitoring.

---

# Output Format

Return a structured Event Card using the format defined in `docs/event-card-schema.md`.

**Required fields:**

- Event Title
- Date Detected
- Region
- Category
- Source
- Event Summary
- Market Exposure
- Signal Indicators
- Signal Strength Score
- Monitoring Window

**Optional fields:**

- Affected Sectors
- Watchlist
- Escalation Trigger
- Invalidation Conditions

---

# Rules

- Do not speculate
- Do not predict prices
- Do not provide trading advice
- Focus on signal detection only
- Use confirmed facts only
- Flag uncertainty explicitly
