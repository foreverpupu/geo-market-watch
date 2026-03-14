# Database Query Output Example

This file shows example output from querying the Geo Alpha Database.

---

## List All Events

```
============================================================
Events (5 found)
============================================================
  [a1b2c3d4...] Red Sea shipping disruption              (Score:  5, Band: monitor      ) → Full Analysis
  [e5f6g7h8...] Russia expands oil export restrictions   (Score:  8, Band: full_analysis) → Full Analysis
  [i9j0k1l2...] Panama Canal drought restrictions        (Score:  5, Band: monitor      ) → Full Analysis
  [m3n4o5p6...] Taiwan military drills escalation        (Score:  2, Band: noise        ) → Full Analysis
  [q7r8s9t0...] Niger uranium export disruption          (Score:  7, Band: full_analysis) → Full Analysis
```

---

## Filter by Region: Middle East

```
============================================================
Events (2 found)
============================================================
  [a1b2c3d4...] Red Sea shipping disruption              (Score:  5, Band: monitor      ) → Full Analysis
  [q7r8s9t0...] Iran sanctions enforcement increase       (Score:  6, Band: monitor      ) → Full Analysis
```

---

## Filter by Band: full_analysis

```
============================================================
Events (3 found)
============================================================
  [e5f6g7h8...] Russia expands oil export restrictions   (Score:  8, Band: full_analysis) → Full Analysis
  [q7r8s9t0...] Niger uranium export disruption          (Score:  7, Band: full_analysis) → Full Analysis
  [a1b2c3d4...] Red Sea shipping disruption              (Score:  5, Band: monitor      ) → Full Analysis
```

---

## Database Statistics

```
============================================================
Geo Alpha Database Statistics
============================================================
Total events: 5
Full Analysis: 3
Monitor: 2
Notifications: 0

Regions: Middle East, Eastern Europe, Central America, East Asia, Africa
Categories: Maritime disruption, Energy policy, Infrastructure disruption, Conflict escalation, Commodity supply disruption
```

---

## JSON Output Example

```json
{
  "total_events": 5,
  "full_analysis_events": 3,
  "monitor_events": 2,
  "total_notifications": 0,
  "regions": [
    "Middle East",
    "Eastern Europe",
    "Central America",
    "East Asia",
    "Africa"
  ],
  "categories": [
    "Maritime disruption",
    "Energy policy",
    "Infrastructure disruption",
    "Conflict escalation",
    "Commodity supply disruption"
  ]
}
```

---

## Event Detail (JSON)

```json
{
  "event_id": "a1b2c3d4e5f67890",
  "event_key": "GMW-2024-001",
  "event_title": "Red Sea shipping disruption",
  "date_detected": "2024-01-12",
  "region": "Middle East",
  "category": "Maritime disruption",
  "summary": "Major container lines reroute vessels due to security risks in the Red Sea.",
  "score": 5,
  "band": "monitor",
  "trigger_full_analysis": 1,
  "status": "active",
  "created_at": "2026-03-15T05:30:00",
  "updated_at": "2026-03-15T05:30:00"
}
```

---

## Notes

- Event IDs are truncated in display (first 8 chars)
- Scores range from 0-10
- Bands: noise, monitor, full_analysis, major_shock
- Trigger status shows escalation decision
