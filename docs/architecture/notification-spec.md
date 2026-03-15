# Notification Specification

This document specifies the notification formats for Geo Market Watch v5.5.

---

## Overview

The notifier generates human-readable markdown notifications for two cases:

1. **Monitor Events** — Continue watching, no escalation
2. **Full Analysis Handoff** — Escalate to deep analysis

---

## Monitor Notification

Generated when:
- `band` = "monitor" (score 4-6)
- `trigger_full_analysis` = false

### Format

```markdown
# Geo Market Watch Alert

**Status:** Monitoring

**Event:** {event_title}

**Region:** {region}

**Category:** {category}

**Score:** {score}

**Band:** {band}

**Trigger Full Analysis:** no

**Summary:**
{summary}

**Next Action:**
Continue monitoring. Recheck in 24 hours.
```

### Example

```markdown
# Geo Market Watch Alert

**Status:** Monitoring

**Event:** Red Sea shipping disruption

**Region:** Middle East

**Category:** Maritime disruption

**Score:** 5

**Band:** monitor

**Trigger Full Analysis:** no

**Summary:**
Major container lines reroute vessels due to security risks in the Red Sea.

**Next Action:**
Continue monitoring. Recheck in 24 hours.
```

---

## Full Analysis Handoff

Generated when:
- `trigger_full_analysis` = true (any band)

### Format

```markdown
# Geo Market Watch Alert

**Status:** Escalate to Full Analysis

**Event:** {event_title}

**Region:** {region}

**Category:** {category}

**Score:** {score}

**Band:** {band}

**Trigger Full Analysis:** yes

**Reasons:**
- {reason_1}
- {reason_2}
...

**Summary:**
{summary}

**Next Action:**
Send this event into Full Analysis Mode.
```

### Example

```markdown
# Geo Market Watch Alert

**Status:** Escalate to Full Analysis

**Event:** Russia expands oil export restrictions

**Region:** Russia / Global Energy

**Category:** Sanctions / policy change

**Score:** 7

**Band:** full_analysis

**Trigger Full Analysis:** yes

**Reasons:**
- score_threshold
- major_sanctions_escalation

**Summary:**
Russia expands restrictions affecting energy exports.

**Next Action:**
Send this event into Full Analysis Mode.
```

---

## File Naming

### Monitor Notifications
```
monitor_{band}_{event_key}.md
```

Example: `monitor_monitor_abc123def456.md`

### Full Analysis Notifications
```
full_analysis_{event_key}.md
```

Example: `full_analysis_def456abc123.md`

---

## Implementation

See: `engine/notifier.py`

Key functions:
- `render_monitor_notification(event)` → str
- `render_full_analysis_notification(event)` → str
- `render_notification(event)` → str (auto-selects type)
- `write_notification(event, output_dir)` → filepath

---

## Validation

Notifications are valid when:

- [x] Status is clearly marked (Monitoring vs Escalate)
- [x] Event metadata is present (title, region, category)
- [x] Score and band are shown
- [x] Trigger decision is explicit (yes/no)
- [x] Handoff includes reasons
- [x] Next action is specified
- [x] Format is valid markdown

---

## Future Enhancements

Potential v5.6+ additions:

- HTML email format
- JSON API payload
- Slack/Discord webhook format
- Dashboard widget format
- Multi-language support

Current v5.5 scope: Markdown files only.
