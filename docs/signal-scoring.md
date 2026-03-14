# Signal Scoring Framework

The signal scoring framework evaluates whether a geopolitical event is likely to impact markets.

It converts qualitative news into a **structured numerical signal**.

Signal scores range from:

- **0** → no relevance 
- **10** → major geopolitical shock

---

# Scoring Dimensions

Signals are evaluated across five dimensions.

| Dimension | Description | Weight |
|-----------|-------------|--------|
| Physical Disruption | Actual supply or production disruption | 3 |
| Transport Impact | Shipping routes, logistics, pipelines | 2 |
| Policy / Sanctions | Government or regulatory changes | 2 |
| Market Transmission | Immediate observable market effects | 2 |
| Escalation Risk | Potential for rapid deterioration | 1 |

**Maximum total score = 10**

---

# Dimension Details

## Physical Disruption

Examples:

- oil export shutdown 
- mining halt 
- pipeline sabotage 
- LNG terminal outage

**Score:**

| Score | Meaning |
|-------|---------|
| 0 | none |
| 1 | potential disruption |
| 2 | partial disruption |
| 3 | confirmed disruption |

---

## Transport Impact

Examples:

- canal restrictions 
- shipping route closures 
- tanker rerouting 
- freight insurance spike

**Score:**

| Score | Meaning |
|-------|---------|
| 0 | none |
| 1 | moderate impact |
| 2 | severe impact |

---

## Policy / Sanctions

Examples:

- export bans 
- sanctions expansion 
- tariff escalation 
- regulatory shutdown

**Score:**

| Score | Meaning |
|-------|---------|
| 0 | none |
| 1 | announced / possible |
| 2 | implemented |

---

## Market Transmission

Evidence markets are already reacting.

Examples:

- freight rate spike 
- commodity price surge 
- shipping capacity tightening

**Score:**

| Score | Meaning |
|-------|---------|
| 0 | no market reaction |
| 1 | early signals |
| 2 | confirmed market movement |

---

## Escalation Risk

Potential for rapid escalation.

Examples:

- military involvement 
- blockade threat 
- alliance intervention

**Score:**

| Score | Meaning |
|-------|---------|
| 0 | unlikely |
| 1 | possible |

---

# Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 0–3 | Noise / irrelevant event | Archive |
| 4–6 | Monitor event | Scout Mode |
| 7–8 | Market relevant event | Full Analysis |
| 9–10 | Major geopolitical shock | Full Analysis + Alert |

---

# Example

**Event:** Red Sea shipping attacks

**Evaluation:**

| Dimension | Score |
|-----------|-------|
| Physical disruption | 1 |
| Transport impact | 2 |
| Policy change | 0 |
| Market transmission | 1 |
| Escalation risk | 1 |
| **Total** | **5** |

**Interpretation:** Monitor event
