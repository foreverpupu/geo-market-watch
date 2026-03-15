# Event Card Schema

Event Cards are structured summaries used by Geo Market Watch to track geopolitical developments during **Scout Mode** and **Full Analysis Mode**.

They standardize early signals so events can be monitored consistently over time.

---

# Event Card Structure

Each Event Card should follow the structure below.

## EVENT CARD

### Event Title
Short description of the geopolitical event.

### Date Detected
YYYY-MM-DD

### Region
Primary geographic region affected.

### Category
One of the following:

- Conflict escalation
- Maritime disruption
- Sanctions / policy change
- Commodity supply disruption
- Infrastructure disruption
- Political instability

### Source
Primary source link.

---

### Event Summary

Brief factual summary of the event.

Only include confirmed information.

Avoid speculation or interpretation.

---

### Market Exposure

Identify potentially affected markets.

Examples:

- crude oil
- LNG
- uranium
- container shipping
- semiconductor supply chain

---

### Signal Indicators

| Indicator | Status |
|-----------|--------|
| Physical supply disruption | Yes / No / Unknown |
| Transport route disruption | Yes / No / Unknown |
| Sanctions or policy shift | Yes / No / Unknown |
| Insurance or freight impact | Yes / No / Unknown |

---

### Signal Strength Score

0–10 scale.

**Guidelines:**

| Score | Meaning |
|-------|---------|
| 0–3 | Noise or minor political signal |
| 4–6 | Watch event |
| 7–8 | Market relevant event |
| 9–10 | Major geopolitical shock |

---

### Affected Sectors

Examples:

- Energy
- Shipping
- Mining
- Defense
- Agriculture

---

### Watchlist (Optional)

Potentially affected companies.

Examples:

**Shipping:**
- ZIM
- Maersk

**Energy:**
- Exxon
- Chevron

---

### Escalation Trigger

Conditions that would trigger Full Analysis Mode.

Examples:

- Confirmed export disruption
- Military escalation
- Shipping insurance spike

---

### Invalidation Conditions

Conditions that invalidate the event signal.

Examples:

- Diplomatic resolution
- Route reopening
- Policy reversal

---

### Monitoring Window

Recommended recheck interval.

Typical values:

- 6 hours
- 12 hours
- 24 hours
- 48 hours

---

# Example Event Card

**Event Title:** Red Sea shipping disruption

**Date Detected:** 2024-01-12

**Region:** Middle East

**Category:** Maritime disruption

**Source:** https://www.reuters.com/world/middle-east/red-sea-shipping

**Event Summary:** Major container lines reroute vessels due to security risks in the Red Sea.

**Market Exposure:**
- Container shipping
- Freight rates

**Signal Strength:** 6 / 10

**Monitoring Window:** 24 hours
